
""" Front facing PyMOL functions """

from . import configuration
from . import identify
from . import pymol_utilities
from .spheres import Spheres
from . import utilities
import logging
import numpy as np
import os
import shutil


logger = logging.getLogger(__name__)

try:
    from pymol import cgo, cmd, CmdException
except:
    logger.error("PyMOL not imported")


def display_pockets(pockets, **opts):
    """ Display a list of pockets

    Args:
      pockets ([Spheres]): list of spheres object to display
      opts (dict): a dictionary containing all PyVOL options (see pyvol.pymol_interface.pymol_pocket_cmdline for details)

    """

    opts["palette"] = pymol_utilities.construct_palette(color_list=opts.get("palette"), max_value=len(pockets))

    if len(pockets) == 0:
        logger.info("No pockets found to display.")

    for index, pocket in enumerate(pockets):
        logger.info("Pocket {0} ({1}) Volume: \t{2} A^3\t({3})".format(index, pocket.name, np.round(pocket.mesh.volume), opts.get("palette")[index]))
        pymol_utilities.display_spheres_object(pocket, pocket.name, state=1, color=opts.get("palette")[index], alpha=opts.get("alpha"), mode=opts.get("display_mode"))


def load_calculation_cmdline(data_dir, prefix=None, display_mode=None, palette=None, alpha=None):
    """ Loads a pocket from memory and displays it in PyMOL

    Args:
      data_dir (str): directory containing PyVOL output (by default ends in .pyvol)
      prefix (str): internal display name (Default value = None)
      display_mode (str): display mode (Default value = "solid")
      palette (str): comma-separated list of PyMOL color strings (Default value = None)
      alpha (float): transparency value (Default value = 1.0)

    """

    if not os.path.isdir(data_dir):
        if os.path.isfile(data_dir):
            data_dir = os.path.dirname(data_dir)
        else:
            logger.error("Ambiguous/unparseable data_dir input: {0}".format(data_dir))
            raise ValueError

    input_opts = {}
    if prefix is not None:
        input_opts["display_prefix"] = prefix
    if display_mode is not None:
        input_opts["display_mode"] = display_mode
    if palette is not None:
        input_opts["palette"] = palette
    if alpha is not None:
        input_opts["alpha"] = alpha


    pockets, opts = identify.load_calculation(data_dir, input_opts=input_opts)
    display_pockets(pockets, **opts)
    logger.info("Loading {0} with mode {1}".format(spheres.name, display_mode))


def pymol_pocket_cmdline(protein=None, ligand=None, prot_file=None, lig_file=None, min_rad=1.4, max_rad=3.4, constrain_radii=True, mode="largest", coordinates=None, residue=None, resid=None, lig_excl_rad=None, lig_incl_rad=None, min_volume=200, subdivide=False, max_clusters=None, min_subpocket_rad=1.7, max_subpocket_rad=3.4, min_subpocket_surf_rad=1.0, radial_sampling=0.1, inclusion_radius_buffer=1.0, min_cluster_size=50, project_dir=None, output_dir=None, prefix=None, logger_stream_level="INFO", logger_file_level="DEBUG", protein_only=False, display_mode="solid", alpha=1.0, palette=None):
    """ PyMOL-compatible command line entry point

    Args:
      protein (str): PyMOL-only PyMOL selection string for the protein (Default value = None)
      ligand (str): PyMOL-only PyMOL selection string for the ligand (Default value = None)
      prot_file (str): filename for the input pdb file containing the peptide--redundant with protein argument (Default value =- )
      lig_file (str): filename for the input pdb file containing a ligand--redundant with ligand argument (Default value = None)
      min_rad (float): radius for SES calculations (Default value = 1.4)
      max_rad (float): radius used to identify the outer, bulk solvent exposed surface (Default value = 3.4)
      constrain_radii (bool): restrict input radii to tested values? (Default value = False)
      mode (str): pocket identification mode (can be largest, all, or specific) (Default value = "largest")
      coordinates ([float]): 3D coordinate used for pocket specification (Default value = None)
      residue (str): Pymol-only PyMOL selection string for a residue to use for pocket specification (Default value=None)
      resid (str): residue identifier for pocket specification (Default value = None)
      lig_excl_rad (float): maximum distance from a provided ligand that can be included in calculated pockets (Default value = None)
      lig_incl_rad (float): minimum distance from a provided ligand that should be included in calculated pockets when solvent border is ambiguous (Default value = None)
      min_volume (float): minimum volume of pockets returned when running in 'all' mode (Default value = 200)
      subdivide (bool): calculate subpockets? (Default value = False)
      max_clusters (int): maximum number of clusters (Default value = None)
      min_subpocket_rad (float): minimum radius that identifies distinct subpockets (Default value = 1.7)
      max_subpocket_rad (float): maximum sampling radius used in subpocket identification (Default value = 3.4)
      min_subpocket_surf_rad (float): radius used to calculate subpocket surfaces (Default value = 1.0)
      inclusion_radius_buffer (float): buffer radius in excess of the nonextraneous radius from the identified pocket used to identify atoms pertinent to subpocket clustering (Default value = 1.0)
      radial_sampling (float): radial sampling used for subpocket clustering (Default value = 0.1)
      min_cluster_size (int): minimum number of spheres in a proper cluster; used to eliminate insignificant subpockets (Default value = 50)
      project_dir (str): parent directory in which to create the output directory if the output directory is unspecified (Default value = None)
      output_dir (str): filename of the directory in which to place all output; can be absolute or relative (Default value = None)
      prefix (str): identifying string for output (Default value = None)
      logger_stream_level (str): sets the logger level for stdio output (Default value = "INFO")
      logger_file_level (str): sets the logger level for file output (Default value = "DEBUG")
      protein_only (bool): PyMOL-only include only peptides in protein file
      display_mode (str): PyMOL-only display mode for calculated pockets (Default value = "solid")
      alpha (float): PyMOL-only display option specifying translucency of CGO objects (Default value = 1.0)
      palette (str): PyMOL-only display option representing a comma separated list of PyMOL color strings (Default value = None)

    """

    opts = {
        "protein": protein,
        "ligand": ligand,
        "prot_file": prot_file,
        "lig_file": lig_file,
        "min_rad": min_rad,
        "max_rad": max_rad,
        "constrain_radii": constrain_radii,
        "mode": mode,
        "residue": residue,
        "resid": resid,
        "coordinates": coordinates,
        "lig_excl_rad": lig_excl_rad,
        "lig_incl_rad": lig_incl_rad,
        "min_volume": min_volume,
        "subdivide": subdivide,
        "max_clusters": max_clusters,
        "min_subpocket_rad": min_subpocket_rad,
        "max_subpocket_rad": max_subpocket_rad,
        "min_subpocket_surf_rad": min_subpocket_surf_rad,
        "radial_sampling": radial_sampling,
        "inclusion_radius_buffer": inclusion_radius_buffer,
        "min_cluster_size": min_cluster_size,
        "project_dir": project_dir,
        "output_dir": output_dir,
        "prefix": prefix,
        "logger_stream_level": logger_stream_level,
        "logger_file_level": logger_file_level,
        "protein_only": protein_only,
        "display_mode": display_mode,
        "alpha": alpha,
        "palette": palette
    }

    pymol_pocket(**opts)

def pymol_pocket(**opts):
    """ Perform PyMOL-dependent processing of inputs to generate input files for PyVOL pocket processing

    Args:
      opts (dict): dictionary containing all PyVOL options (see pyvol.pymol_interface.pymol_pocket_cmdline for details)

    Returns:
      pockets ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct pocket or subpocket
      output_opts (dict): dictionary containing the actual options used in the pocket calculation

    """


    boolean_args = ["constrain_radii", "subdivide", "protein_only"]
    for arg in boolean_args:
        if not isinstance(opts.get(arg), bool):
            if opts.get(arg) in ["True", "true", "t", "1"]:
                opts[arg] = True
            elif opts.get(arg) in ["False", "false", "f", "0"]:
                opts[arg] = False
            else:
                logger.warning("Boolean argument {0} ({1}) not parsed correctly and reverting to default".format(arg, opts[arg]))

    opts = configuration.clean_opts(opts)

    if opts.get("protein") is None:
        if opts.get("prot_file") is None:
            logger.error("No protein input: prot_file and protein inputs are empty")
            raise ValueError
        else:
            logger.debug("Protein file already specified on disk; skipping protein processing.")
    else:
        if opts.get("protein_only"):
            opts["protein"] = "({0}) and (poly)".format(opts.get("protein"))

        if opts.get("ligand") is not None:
            opts["protein"] = "({0}) and not ({1})".format(opts.get("protein"), opts.get("ligand"))

        logger.debug("Final protein selection: {0}".format(opts.get("protein")))
        prot_atoms = cmd.count_atoms(opts.get("protein"))
        if prot_atoms == 0:
            logger.error("No atoms included in protein selection--ending calculation")
            return
        elif prot_atoms < 100:
            logger.warning("Only {0} atoms included in protein selection".format(prot_atoms))

        cmd.save(opts.get("prot_file"), opts.get("protein"))
        logger.debug("Protein '{0}' saved to {1}".format(opts.get("protein"), opts.get("prot_file")))

    if opts.get("ligand") is not None:
        cmd.save(opts.get("lig_file"), opts.get("ligand"))
        logger.debug("Ligand selection: {0}".format(opts.get("ligand")))

    if opts.get("coordinates") is not None:
        opts["residue"] = None
    else:
        if opts.get("residue") is not None:
            opts["coordinates"] = cmd.get_coords("{0} and sidechain".format(opts.get("residue")), 1)

    pockets, output_opts = identify.pocket_wrapper(**opts)

    display_pockets(pockets, **output_opts)
    return pockets, output_opts
