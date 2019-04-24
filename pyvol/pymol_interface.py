
from . import identify
from . import pymol_utilities
import os
from pymol import cgo, cmd, CmdException
import shutil
import tempfile


def pocket(protein, mode=None, ligand=None, pocket_coordinate=None, residue=None, name="bp", min_rad=1.4, max_rad=3.4, lig_excl_rad=None, lig_incl_rad=None, display_mode="solid", color='marine', alpha=0.85, output_dir=None, subdivide=None, minimum_volume=200):
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

    spheres = identify.pocket(prot_file, mode=mode, lig_file=lig_file, coordinate=pocket_coordinate, min_rad=min_rad, max_rad=max_rad, lig_excl_rad=lig_excl_rad, lig_incl_rad=lig_incl_rad, subdivide=subdivide, minimum_volume=minimum_volume)

    if mode in ["specific", "largest"]:
        if not subdivide:
            print("Pocket Volume: {0} A^3".format(format(spheres[0].mesh.volume, '.2f')))
            pymol_utilities.display_spheres_object(spheres[0], name, state=1, color=color, alpha=alpha, mode=display_mode)
        else:
            print("Whole Pocket Volume: {0} A^3".format(format(spheres[0].mesh.volume, '.2f')))
            pymol_utilities.display_spheres_object(spheres[0], name, state=1, color=color, alpha=alpha, mode=display_mode)
            palette = construct_palette(max_value=(len(spheres) -1))
            for index, sps in enumerate(spheres[1:]):
                group = int(sps.g[0])
                print("Subpocket {0} Volume: {1} A^3".format(group, format(sps.mesh.volume, '.2f')))
                pymol_utilities.display_spheres_object(sps, "{0}_sp{1}".format(name, group), state=1, color=palette[index], alpha=alpha, mode=display_mode)
    else:
        palette = pymol_utilities.construct_palette(max_value=len(spheres))
        for index, s in enumerate(spheres):
            print("Pocket Volume {0}: {1} A^3".format(index, format(s.mesh.volume, '.2f')))
            pymol_utilities.display_spheres_object(s, name, state=1, color=palette[index], alpha=alpha, mode=display_mode)

    if output_dir is None:
        shutil.rmtree(out_dir)
    return
