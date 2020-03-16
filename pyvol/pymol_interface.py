
from . import configuration
from . import identify
from . import pymol_utilities
from .spheres import Spheres
from . import utilities
import logging
import os
import shutil


logger = logging.getLogger(__name__)

try:
    from pymol import cgo, cmd, CmdException
except:
    logger.error("PyMOL not imported")


def display_pockets(pockets, **opts):
    """ Display a list of pockets

    """

    opts["palette"] = pymol_utilities.construct_palette(color_list=opts.get("palette"), max_value=len(pockets))

    if len(pockets) == 0:
        logger.info("No pockets found to display.")

    for index, pocket in enumerate(pockets):
        logger.info("Pocket {0} ({1}) Volume: \t{2} A^3\t({3})".format(index, pocket.name, np.round(pocket.mesh.volume), opts.get("palette")[index]))
        pymol_utilities.display_spheres_object(pocket, pocket.name, state=1, color=opts.get("palette")[index], alpha=opts.get("alpha"), mode=opts.get("display_mode"))


    # if mode in ["specific", "largest"]:
    #     if not subdivide:
    #         try:
    #             logger.info("Pocket Volume: {0} A^3".format(round(spheres[0].mesh.volume)))
    #             pymol_utilities.display_spheres_object(spheres[0], spheres[0].name, state=1, color=color, alpha=alpha, mode=display_mode)
    #         except:
    #             logger.warning("Volume not calculated for pocket")
    #
    #     else:
    #         try:
    #             logger.info("Whole Pocket Volume: {0} A^3".format(round(spheres[0].mesh.volume)))
    #         except:
    #             logger.warning("Volume not calculated for the whole pocket")
    #         pymol_utilities.display_spheres_object(spheres[0], spheres[0].name, state=1, color=color, alpha=alpha, mode=display_mode)
    #
    #         if palette is None:
    #             palette = pymol_utilities.construct_palette(max_value=(len(spheres) - 1))
    #         else:
    #             palette = pymol_utilities.construct_palette(color_list=palette.split(","), max_value =(len(spheres) - 1))
    #         for index, sps in enumerate(spheres[1:]):
    #             group = int(sps.g[0])
    #             try:
    #                 logger.info("{0} volume: {1} A^3".format(sps.name, round(sps.mesh.volume)))
    #                 pymol_utilities.display_spheres_object(sps, sps.name, state=1, color=palette[index], alpha=alpha, mode=display_mode)
    #             except:
    #                 logger.warning("Volume not calculated for pocket: {0}".format(sps.name))
    #
    #         cmd.disable(spheres[0].name)
    #
    #         if display_mode == "spheres":
    #             cmd.group("{0}_sg".format(spheres[0].name), "{0}*_g".format(spheres[0].name))
    #         else:
    #             cmd.group("{0}_g".format(spheres[0].name), "{0}*".format(spheres[0].name))
    #
    # else:
    #     # mode is all
    #     if len(spheres) == 0:
    #         logger.warning("No pockets found with volume > {0} A^3".format(minimum_volume))
    #         return
    #     else:
    #         logger.info("Pockets found: {0}".format(len(spheres)))
    #
    #     palette = pymol_utilities.construct_palette(max_value=len(spheres))
    #     for index, s in enumerate(spheres):
    #         try:
    #             logger.info("{0} volume: {1} A^3".format(s.name, round(s.mesh.volume)))
    #             pymol_utilities.display_spheres_object(s, s.name, state=1, color=palette[index], alpha=alpha, mode=display_mode)
    #         except:
    #             logger.warning("Volume not calculated for pocket: {0}".format(s.name))
    #
    #     name_template = "p".join(spheres[0].name.split("p")[:-1])
    #     if display_mode == "spheres":
    #         cmd.group("{0}sg".format(name_template), "{0}*_g".format(name_template))
    #     else:
    #         cmd.group("{0}g".format(name_template), "{0}*".format(name_template))


def load_pocket(spheres_file, name=None, display_mode="solid", color='marine', alpha=0.85):
    """ Loads a pocket from memory and displays it in PyMOL

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


def pymol_pocket_cmdline(protein, ligand=None, min_rad=1.4, max_rad=3.4, constrain_radii=True, mode="largest", coordinates=None, residue=None, resid=None, lig_excl_rad=None, lig_incl_rad=None, min_volume=200, subdivide=False, max_clusters=None, min_subpocket_rad=1.7, max_subpocket_rad=3.4, min_subpocket_surf_rad=1.0, radial_sampling=0.1, inclusion_radius_buffer=1.0, min_cluster_size=50, project_dir=None, output_dir=None, prefix=None, logger_stream_level="INFO", logger_file_level="DEBUG", protein_only=False, display_mode="solid", alpha=0.85, palette=None):
    """ PyMOL-compatible command line entry point

    """

    opts = {
        "protein": protein,
        "ligand": ligand,
        "prot_file": None,
        "lig_file": None,
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

    pymol_pocket(**configuration.clean_opts(opts))

def pymol_pocket(**opts):

    utilities.check_dir(opts.get("output_dir"))

    if opts.get("protein_only"):
        opts["protein"] = "({0}) and (poly)".format(opts.get("protein"))

    if opts.get("ligand") is not None:
        opts["protein"] = "({0}) and not ({1})".format(opts.get("protein"), opts.get("ligand"))

        cmd.save(opts.get("lig_file"), opts.get("ligand"))
        logger.debug("Ligand selection: {0}".format(opts.get("ligand")))

    logger.debug("Final protein selection: {0}".format(opts.get("protein")))

    prot_atoms = cmd.count_atoms(opts.get("protein"))
    if prot_atoms == 0:
        logger.error("No atoms included in protein selection--ending calculation")
        return
    elif prot_atoms < 100:
        logger.warning("Only {0} atoms included in protein selection".format(prot_atoms))

    cmd.save(opts.get("prot_file"), opts.get("protein"))
    logger.debug("Protein '{0}' saved to {1}".format(opts.get("protein"), opts.get("prot_file")))

    if opts.get("coordinates") is not None:
        opts["residue"] = None
    else:
        if opts.get("residue") is not None:
            opts["coordinates"] = cmd.get_coords(opts.get("residue"), 1)

    pockets, output_opts = identify.pocket_wrapper(**opts)

    display_pockets(pockets, **output_opts)
    return pockets, output_opts
