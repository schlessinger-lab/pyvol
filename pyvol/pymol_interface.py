
from . import identify
from . import pymol_utilities
from .spheres import Spheres
from . import utilities
import logging
import os
import shutil
import tempfile
import time

main_logger = logging.getLogger("pyvol")
main_logger.setLevel("DEBUG")

stdio_handler_found = False
for handler in main_logger.handlers:
    if isinstance(handler, logging.StreamHandler):
        stdio_handler_found = True
        break
if not stdio_handler_found:
    log_out = logging.StreamHandler()
    log_out.setLevel("INFO")
    log_out.setFormatter(logging.Formatter("%(name)-12s:".ljust(25) + "\t%(levelname)-8s" + "\t%(message)s"))
    main_logger.addHandler(log_out)

logger = logging.getLogger(__name__)

try:
    from pymol import cgo, cmd, CmdException
except:
    logger.warning("PyMOL not imported")

def load_pocket(spheres_file, name=None, display_mode="solid", color='marine', alpha=0.85):
    """

    Args:
      spheres_file (str): filename
      name (str): internal display name (Default value = None)
      display_mode (str): display mode (Default value = "solid")
      color (str): PyMOL color string (Default value = 'marine')
      alpha (float): transparency value (Default value = 0.85)

    """
    spheres = Spheres(spheres_file=spheres_file, name=name)
    pymol_utilities.display_spheres_object(spheres, spheres.name, state=1, color=color, alpha=alpha, mode=display_mode)
    logger.info("Loading {0} with mode {1}".format(spheres.name, display_mode))


def pocket(protein, mode=None, ligand=None, pocket_coordinate=None, residue=None, resid=None, prefix=None, min_rad=1.4, max_rad=3.4, lig_excl_rad=None, lig_incl_rad=None, display_mode="solid", color='marine', alpha=0.85, output_dir=None, subdivide=None, minimum_volume=200, min_subpocket_rad=1.7, min_subpocket_surf_rad=1.0, max_clusters=None, excl_org=False, constrain_inputs=True, palette=None):
    """Calculates the SAS for a binding pocket and displays it

    Args:
      protein (str): PyMOL selection string for the protein
      mode (str): pocket identification mode (can be largest, all, or specific) (Default value = None)
      ligand (str): PyMOL selection string for the ligand (Default value = None)
      pocket_coordinate ([float]): 3D coordinate used for pocket specification (Default value = None)
      residue (str): PyMOL residue selection string for pocket specification (Default value = None)
      resid (str): residue identifier for pocket specification (Default value = None)
      prefix (str): identifying string for output (Default value = None)
      min_rad (float): radius for SAS calculations (Default value = 1.4)
      max_rad (float): radius used to identify the outer, bulk solvent exposed surface (Default value = 3.4)
      lig_excl_rad (float): maximum distance from a provided ligand that can be included in calculated pockets (Default value = None)
      lig_incl_rad (float): minimum distance from a provided ligand that should be included in calculated pockets when solvent border is ambiguous (Default value = None)
      display_mode (str): display mode for calculated pockets (Default value = "solid")
      color (str): PyMOL color string (Default value = 'marine')
      alpha (float): transparency value (Default value = 0.85)
      output_dir (str): filename of the directory in which to place all output; can be absolute or relative (Default value = None)
      subdivide (bool): calculate subpockets? (Default value = None)
      minimum_volume (float): minimum volume of pockets returned when running in 'all' mode (Default value = 200)
      min_subpocket_rad (float): minimum radius that identifies distinct subpockets (Default value = 1.7)
      min_subpocket_surf_rad (float): radius used to calculate subpocket surfaces (Default value = 1.0)
      max_clusters (int): maximum number of clusters (Default value = None)
      excl_org (bool): exclude non-peptide atoms from the protein selection? (Default value = False)
      constrain_inputs (bool): constrain input quantitative values to tested ranges? (Default value = True)
      palette ([str]): a list of PyMOL-accepted color strings to use when displaying multiple surfaces

    """

    timestamp = time.strftime("%H%M%S")

    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    else:
        logging.debug("Output directory set to {0}".format(output_dir))
        utilities.check_dir(output_dir)

    if excl_org:
        # protein = "({0}) and (not org)".format(protein)
        protein = "({0}) and (poly)".format(protein)

    if ligand is not None:
        protein = "({0}) and not ({1})".format(protein, ligand)

        lig_file = os.path.join(output_dir, "{0}_lig.pdb".format(timestamp))
        cmd.save(lig_file, ligand)
        logger.debug("Ligand selection: {0}".format(ligand))
    else:
        lig_file = None

    logger.debug("Final protein selection: {0}".format(protein))

    prot_atoms = cmd.count_atoms(protein)
    if prot_atoms == 0:
        logger.error("No atoms included in protein selection")
        return
    elif prot_atoms < 50:
        logger.warning("Only {0} atoms included in protein selection".format(prot_atoms))

    prot_file = os.path.join(output_dir, "{0}_{1}.pdb".format(timestamp, protein.split()[0].strip("(").strip(")")))
    cmd.save(prot_file, protein)

    residue_coordinates = None
    if residue is not None:
        residue_coordinates = cmd.get_coords(residue, 1)

    if (mode is None) and ((ligand is not None) or (pocket_coordinate is not None) or (resid is not None) or (residue_coordinates is not None)):
        mode = "specific"
    elif mode is None:
        mode = "largest"
    logger.info("Running in mode: {0}".format(mode))

    spheres = identify.pocket(prot_file, mode=mode, lig_file=lig_file, resid=resid, residue_coordinates=residue_coordinates, coordinate=pocket_coordinate, min_rad=min_rad, max_rad=max_rad, lig_excl_rad=lig_excl_rad, lig_incl_rad=lig_incl_rad, subdivide=subdivide, minimum_volume=minimum_volume, min_subpocket_rad=min_subpocket_rad, prefix=prefix, output_dir=output_dir, min_subpocket_surf_rad=min_subpocket_surf_rad, max_clusters=max_clusters, constrain_inputs=constrain_inputs)

    if mode in ["specific", "largest"]:
        if not subdivide:
            try:
                # logger.info("Pocket Volume: {0} A^3".format(format(spheres[0].mesh.volume, '.2f')))
                logger.info("Pocket Volume: {0} A^3".format(round(spheres[0].mesh.volume)))
                pymol_utilities.display_spheres_object(spheres[0], spheres[0].name, state=1, color=color, alpha=alpha, mode=display_mode)
            except:
                logger.warning("Volume not calculated for pocket")

        else:
            try:
                logger.info("Whole Pocket Volume: {0} A^3".format(round(spheres[0].mesh.volume)))
            except:
                logger.warning("Volume not calculated for the whole pocket")
            pymol_utilities.display_spheres_object(spheres[0], spheres[0].name, state=1, color=color, alpha=alpha, mode=display_mode)

            if palette is None:
                palette = pymol_utilities.construct_palette(max_value=(len(spheres) - 1))
            else:
                palette = pymol_utilities.construct_palette(color_list=palette.split(","), max_value =(len(spheres) - 1))
            for index, sps in enumerate(spheres[1:]):
                group = int(sps.g[0])
                try:
                    logger.info("{0} volume: {1} A^3".format(sps.name, round(sps.mesh.volume)))
                    pymol_utilities.display_spheres_object(sps, sps.name, state=1, color=palette[index], alpha=alpha, mode=display_mode)
                except:
                    logger.warning("Volume not calculated for pocket: {0}".format(sps.name))

            cmd.disable(spheres[0].name)

            if display_mode == "spheres":
                cmd.group("{0}_sg".format(spheres[0].name), "{0}*_g".format(spheres[0].name))
            else:
                cmd.group("{0}_g".format(spheres[0].name), "{0}*".format(spheres[0].name))

    else:
        # mode is all
        if len(spheres) == 0:
            logger.warning("No pockets found with volume > {0} A^3".format(minimum_volume))
            return
        else:
            logger.info("Pockets found: {0}".format(len(spheres)))

        palette = pymol_utilities.construct_palette(max_value=len(spheres))
        for index, s in enumerate(spheres):
            try:
                logger.info("{0} volume: {1} A^3".format(s.name, round(s.mesh.volume)))
                pymol_utilities.display_spheres_object(s, s.name, state=1, color=palette[index], alpha=alpha, mode=display_mode)
            except:
                logger.warning("Volume not calculated for pocket: {0}".format(s.name))

        name_template = "p".join(spheres[0].name.split("p")[:-1])
        if display_mode == "spheres":
            cmd.group("{0}sg".format(name_template), "{0}*_g".format(name_template))
        else:
            cmd.group("{0}g".format(name_template), "{0}*".format(name_template))

    if output_dir is None:
        shutil.rmtree(output_dir)
    return
