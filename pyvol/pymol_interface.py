
from . import identify
from . import pymol_utilities
from .spheres import Spheres
from . import utilities
import os
from pymol import cgo, cmd, CmdException
import shutil
import tempfile
import time


def load_spheres(spheres_file, name=None, display_mode="solid", color='marine', alpha=0.85):
    spheres = Spheres(spheres_file=spheres_file, name=name)
    pymol_utilities.display_spheres_object(spheres, spheres.name, state=1, color=color, alpha=alpha, mode=display_mode)


def pocket(protein, mode=None, ligand=None, pocket_coordinate=None, residue=None, prefix=None, min_rad=1.4, max_rad=3.4, lig_excl_rad=None, lig_incl_rad=None, display_mode="solid", color='marine', alpha=0.85, output_dir=None, subdivide=None, minimum_volume=200, min_subpocket_rad=1.7, min_subpocket_surf_rad=1.0, max_clusters=None):
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

    if (mode is None) and ((ligand is not None) or (pocket_coordinate is not None) or (residue is not None)):
        mode = "specific"
    elif mode is None:
        mode = "largest"

    spheres = identify.pocket(prot_file, mode=mode, lig_file=lig_file, residue=residue, coordinate=pocket_coordinate, min_rad=min_rad, max_rad=max_rad, lig_excl_rad=lig_excl_rad, lig_incl_rad=lig_incl_rad, subdivide=subdivide, minimum_volume=minimum_volume, min_subpocket_rad=min_subpocket_rad, prefix=prefix, output_dir=output_dir, min_subpocket_surf_rad=min_subpocket_surf_rad, max_clusters=max_clusters)

    if mode in ["specific", "largest"]:
        if not subdivide:
            print("Pocket Volume: {0} A^3".format(format(spheres[0].mesh.volume, '.2f')))
            pymol_utilities.display_spheres_object(spheres[0], spheres[0].name, state=1, color=color, alpha=alpha, mode=display_mode)
        else:
            print("Whole Pocket Volume: {0} A^3".format(format(spheres[0].mesh.volume, '.2f')))
            pymol_utilities.display_spheres_object(spheres[0], spheres[0].name, state=1, color=color, alpha=alpha, mode=display_mode)
            palette = pymol_utilities.construct_palette(max_value=(len(spheres) -1))
            for index, sps in enumerate(spheres[1:]):
                group = int(sps.g[0])
                print("{0} volume: {1} A^3".format(sps.name, format(sps.mesh.volume, '.2f')))
                pymol_utilities.display_spheres_object(sps, sps.name, state=1, color=palette[index], alpha=alpha, mode=display_mode)
            cmd.group(spheres[0].name, "{0}*".format(spheres[0].name))
    else:
        palette = pymol_utilities.construct_palette(max_value=len(spheres))
        for index, s in enumerate(spheres):
            print("{0} volume: {1} A^3".format(s.name, format(s.mesh.volume, '.2f')))
            pymol_utilities.display_spheres_object(s, s.name, state=1, color=palette[index], alpha=alpha, mode=display_mode)

    if output_dir is None:
        shutil.rmtree(output_dir)
    return
