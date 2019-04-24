
from . import identify
from . import utilities
import numpy as np
import os
from pymol import cgo, cmd, CmdException
import scipy
import shutil
import sys
import tempfile


def construct_palette(color_list=None, max_value=7, min_value=1):
    if color_list is None:
        color_list = ['tv_red', 'tv_orange', 'tv_yellow', 'tv_green', 'tv_blue', 'aquamarine', 'violet']
    if max_value <= len(color_list):
        return color_list
        
    colors = [cmd.get_color_tuple(x) for x in color_list]
    output_range = max_value - min_value + 1

    palette = []
    
    color_vectors = len(colors) - 1
    steps = output_range / color_vectors
    for cv in range(color_vectors):
        for x in range(steps):
            fx = float(x) / steps
            cl = [fx * colors[cv + 1][i] + (1 - fx) * colors[cv][i] for i in range(3)]
            cn = '0x%02x%02x%02x' % tuple([255 * x for x in cl])
            palette.append(cn)
    return palette
            

def display_pseudoatom_group(spheres, name, color='gray60', palette=None):
    """
    Displays a collection of pseudoatoms

    Parameters
    ----------
    spheres : Spheres
        A spheres object containing xyzr coordinates/vdw radii
    name : string
        Name for the group of pseudoatoms (with individual pseudoatoms named name.x)
    color : string
        Name of the PyMOL color to apply to the pseudoatoms
    """

    if spheres is None:
        return
    
    for index, xyzrg in enumerate(spheres.xyzrg):
        if palette is None:
            cmd.pseudoatom("{0}.{1}".format(name, index), pos=list(xyzrg[0:3]), vdw=float(xyzrg[3]), color=color)
        else:
            cmd.pseudoatom("{0}.{1}".format(name, index), pos=list(xyzrg[0:3]), vdw=float(xyzrg[3]), color=palette[int(xyzrg[4] - 1)])

    cmd.group(name, "{0}.*".format(name))
    cmd.show("spheres", name)  


def display_spheres_object(spheres, name, state=1, color='marine', alpha=0.7, mode="solid", palette=None):
    """
    Loads a mesh object into a cgo list for display in PyMOL

    Parameters
    ----------
    mesh : Trimesh
        A Trimesh object containing the triangulated mesh
    name : string
        Name for the object in PyMOL
    state : int
        State for the loaded surface (allows for multiple surfaces to be loaded in the same object)
    color : string
        Name of the PyMOL color to apply to the surface
    alpha : float
        Transparency value for the object
    mode : string
        Display a 'transparent' surface, a 'solid' surface, or a collection of pseudoatoms 'spheres'
    """

    alpha = float(alpha)
    if spheres is None:
        return

    if (mode == "mesh") or (mode == "solid"):
        if spheres.mesh is None:
            return
        else:
            if mode == "solid":
                cmd.load_cgo(mesh_to_solid_CGO(spheres.mesh, color=color, alpha=alpha), cmd.get_unused_name(name), state)
            else:
                cmd.load_cgo(mesh_to_wireframe_CGO(spheres.mesh, color=color, alpha=alpha), cmd.get_unused_name(name), state)
    elif mode == "spheres":
        display_pseudoatom_group(spheres, name, color=color, palette=None)
        
    
def mesh_to_solid_CGO(mesh, color='gray60', alpha=1.0):
    """
    Creates a solid CGO object for a mesh for display in PyMOL

    Parameters
    ----------
    mesh : Trimesh
        A Trimesh object containing the triangulated mesh
    color : string
        Name of the PyMOL color to apply to the surface
    alpha : float
        Transparency value for the object
    """
    
    cgobuffer = [cgo.BEGIN, cgo.TRIANGLES, cgo.ALPHA, alpha]
    color_values = cmd.get_color_tuple(cmd.get_color_index(color))

    for face in mesh.faces:
        for v_index in face:
            cgobuffer.append(cgo.COLOR)
            cgobuffer.extend(color_values)

            cgobuffer.append(cgo.NORMAL)
            cgobuffer.extend([mesh.vertex_normals[v_index][i] for i in range(3)])
            cgobuffer.append(cgo.VERTEX)
            cgobuffer.extend([mesh.vertices[v_index][i] for i in range(3)])
    cgobuffer.append(cgo.END)
    return cgobuffer


def mesh_to_wireframe_CGO(mesh, color='gray60', alpha=1.0):
    """
    Creates a wireframe CGO object for a mesh for display in PyMOL

    Parameters
    ----------
    mesh : Trimesh
        A Trimesh object containing the triangulated mesh
    color : string
        Name of the PyMOL color to apply to the surface
    alpha : float
        Transparency value for the object
    """

    cgobuffer = [cgo.BEGIN, cgo.LINES, cgo.ALPHA, alpha]

    cgobuffer.append(cgo.COLOR)
    cgobuffer.extend(cmd.get_color_tuple(cmd.get_color_index(color)))

    for edge in mesh.edges:
        cgobuffer.append(cgo.VERTEX)
        cgobuffer.extend(mesh.vertices[edge[0]])
        cgobuffer.append(cgo.VERTEX)
        cgobuffer.extend(mesh.vertices[edge[1]])
            
    cgobuffer.append(cgo.END)
    return cgobuffer


def pocket(protein, mode=None, ligand=None, pocket_coordinate=None, residue=None, name="bp", min_rad=1.4, max_rad=3.4, lig_excl_rad=None, lig_incl_rad=None, display_mode="solid", color='marine', alpha=0.85, output_dir=None, subdivide=None):
    """
    Calculates the SES for a binding pocket and displays it

    Parameters
    ----------
    """

    if output_dir is None:
        out_dir = tempfile.mkdtemp()
    if ligand is not None:
        protein = "({0}) and not ({1})".format(protein, ligand)
        
        lig_file = os.path.join(out_dir, "lig.pdb")
        cmd.save(lig_file, ligand)
    else:
        lig_file = None
        
    prot_atoms = cmd.count_atoms(protein)
    if prot_atoms == 0:
        print("Error: no atoms included in protein selection")
        return
    elif prot_atoms < 50:
        print("Warning: only {0} atoms included in protein selection".format(prot_atoms))

    prot_file = os.path.join(out_dir, "prot.pdb")
    cmd.save(prot_file, protein)

    if (mode is None) and ((ligand is not None) or (pocket_coordinate is not None) or (residue is not None)):
        mode = "specific"
    elif mode is None:
        mode = "largest"

    spheres = identify.pocket(prot_file, mode=mode, lig_file=lig_file, coordinate=pocket_coordinate, min_rad=min_rad, max_rad=max_rad, lig_excl_rad=lig_excl_rad, lig_incl_rad=lig_incl_rad, subdivide=subdivide)

    if mode in ["specific", "largest"]:
        if not subdivide:
            print("Pocket Volume: {0} A^3".format(format(spheres[0].mesh.volume, '.2f')))
            display_spheres_object(spheres[0], name, state=1, color=color, alpha=alpha, mode=display_mode)
        else:
            print("Whole Pocket Volume: {0} A^3".format(format(spheres[0].mesh.volume, '.2f')))
            display_spheres_object(spheres[0], name, state=1, color=color, alpha=alpha, mode=display_mode)
            palette = construct_palette(max_value=(len(spheres) -1))
            for index, sps in enumerate(spheres[1:]):
                group = int(sps.g[0])
                print("Subpocket {0} Volume: {1} A^3".format(group, format(sps.mesh.volume, '.2f')))
                display_spheres_object(sps, "{0}_sp{1}".format(name, group), state=1, color=palette[index], alpha=alpha, mode=display_mode)
    else:
        palette = construct_palette(max_value=len(spheres))
        for index, s in enumerate(spheres):
            print("Pocket Volume {0}: {1} A^3".format(index, format(s.mesh.volume, '.2f')))
            display_spheres_object(s, name, state=1, color=palette[index], alpha=alpha, mode=display_mode)

    if output_dir is None:
        shutil.rmtree(out_dir)
    return
