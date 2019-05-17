
from . import identify
from . import pymol_utilities
from .spheres import Spheres
from . import utilities
import os
from pymol import cgo, cmd, CmdException
import shutil
import tempfile
import time


def load_pocket(spheres_file, name=None, display_mode="solid", color='marine', alpha=0.85):
    spheres = Spheres(spheres_file=spheres_file, name=name)
    pymol_utilities.display_spheres_object(spheres, spheres.name, state=1, color=color, alpha=alpha, mode=display_mode)


def pocket(protein, mode=None, ligand=None, pocket_coordinate=None, residue=None, resid=None, prefix=None, min_rad=1.4, max_rad=3.4, lig_excl_rad=None, lig_incl_rad=None, display_mode="solid", color='marine', alpha=0.85, output_dir=None, subdivide=None, minimum_volume=200, min_subpocket_rad=1.7, min_subpocket_surf_rad=1.0, max_clusters=None, excl_org=False):
    """
    Calculates the SES for a binding pocket and displays it

    Parameters
    ----------
    """

    timestamp = time.strftime("%H%M%S")

    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    else:
        utilities.check_dir(output_dir)

    if excl_org:
        protein = "({0}) and (not org)".format(protein)
        
    if ligand is not None:
        protein = "({0}) and not ({1})".format(protein, ligand)
        
        lig_file = os.path.join(output_dir, "{0}_lig.pdb".format(timestamp))
        cmd.save(lig_file, ligand)
    else:
        lig_file = None
        
    prot_atoms = cmd.count_atoms(protein)
    if prot_atoms == 0:
        print("Error: no atoms included in protein selection")
        return
    elif prot_atoms < 50:
        print("Warning: only {0} atoms included in protein selection".format(prot_atoms))

    prot_file = os.path.join(output_dir, "{0}_{1}.pdb".format(timestamp, protein.split()[0].strip("(").strip(")")))
    cmd.save(prot_file, protein)

    residue_coordinates = None
    if residue is not None:
        residue_coordinates = cmd.get_coords(residue, 1)

    if (mode is None) and ((ligand is not None) or (pocket_coordinate is not None) or (resid is not None) or (residue_coordinates is not None)):
        mode = "specific"
    elif mode is None:
        mode = "largest"

    spheres = identify.pocket(prot_file, mode=mode, lig_file=lig_file, resid=resid, residue_coordinates=residue_coordinates, coordinate=pocket_coordinate, min_rad=min_rad, max_rad=max_rad, lig_excl_rad=lig_excl_rad, lig_incl_rad=lig_incl_rad, subdivide=subdivide, minimum_volume=minimum_volume, min_subpocket_rad=min_subpocket_rad, prefix=prefix, output_dir=output_dir, min_subpocket_surf_rad=min_subpocket_surf_rad, max_clusters=max_clusters)

    if mode in ["specific", "largest"]:
        if not subdivide:
            try:
                # print("Pocket Volume: {0} A^3".format(format(spheres[0].mesh.volume, '.2f')))
                print("Pocket Volume: {0} A^3".format(round(spheres[0].mesh.volume)))
                pymol_utilities.display_spheres_object(spheres[0], spheres[0].name, state=1, color=color, alpha=alpha, mode=display_mode)
            except:
                print("Volume not calculated for pocket")
            
        else:
            try:
                print("Whole Pocket Volume: {0} A^3".format(round(spheres[0].mesh.volume)))
            except:
                print("Volume not calculated for the whole pocket")
            pymol_utilities.display_spheres_object(spheres[0], spheres[0].name, state=1, color=color, alpha=alpha, mode=display_mode)
            
            palette = pymol_utilities.construct_palette(max_value=(len(spheres) -1))
            for index, sps in enumerate(spheres[1:]):
                group = int(sps.g[0])
                try:
                    print("{0} volume: {1} A^3".format(sps.name, round(sps.mesh.volume)))
                    pymol_utilities.display_spheres_object(sps, sps.name, state=1, color=palette[index], alpha=alpha, mode=display_mode)
                except:
                    print("Volume not calculated for pocket: {0}".format(sps.name))
                
            cmd.disable(spheres[0].name)
            
            if display_mode == "spheres":
                cmd.group("{0}_sg".format(spheres[0].name), "{0}*_g".format(spheres[0].name))
            else:
                cmd.group("{0}_g".format(spheres[0].name), "{0}*".format(spheres[0].name))

    else:
        palette = pymol_utilities.construct_palette(max_value=len(spheres))
        for index, s in enumerate(spheres):
            try:
                print("{0} volume: {1} A^3".format(s.name, round(s.mesh.volume)))
                pymol_utilities.display_spheres_object(s, s.name, state=1, color=palette[index], alpha=alpha, mode=display_mode)
            except:
                print("Volume not calculated for pocket: {0}".format(s.name))
                
        name_template = "p".join(spheres[0].name.split("p")[:-1])
        if display_mode == "spheres":
            cmd.group("{0}sg".format(name_template), "{0}*_g".format(name_template))
        else:
            cmd.group("{0}g".format(name_template), "{0}*".format(name_template))
            
    if output_dir is None:
        shutil.rmtree(output_dir)
    return
