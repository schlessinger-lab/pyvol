
from pymol import cgo, cmd, CmdException


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
