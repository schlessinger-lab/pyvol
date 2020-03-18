
""" Handles options for PyVOL. Reads configuration files and objects and converts them to option dictionaries and then back again. Accepts and parses string input for all parameters from commandline/gui inputs. """

from . import utilities
import configparser
import logging
import numpy as np
import os
import re
import tempfile
from datetime import datetime

logger = logging.getLogger(__name__)

def clean_opts(input_opts):
    """ Cleans opts and then returns the sanitized contents

    Args:
      input_opts (dict): dictionary of all input options

    Returns:
      cleaned_opts (dict): dictionary containing all options for a PyVOL run with extraneous options removed and necessary defaults provided
    """

    timestamp = datetime.now().strftime(r"%H%M%S-%f")

    trimmed_opts = {}
    for k, v in input_opts.items():
        if v is not None:
            trimmed_opts[k] = v
    input_opts = trimmed_opts

    # Load options
    opts = {}
    opts["protein"] = input_opts.get("protein")
    opts["prot_file"] = input_opts.get("prot_file")
    opts["lig_file"] = input_opts.get("lig_file")
    opts["min_rad"] = float(input_opts.get("min_rad", 1.4))
    opts["max_rad"] = float(input_opts.get("max_rad", 3.4))
    opts["constrain_radii"] = input_opts.get("constrain_inputs", False)

    opts["mode"] = input_opts.get("mode")
    opts["coordinates"] = input_opts.get("coordinates")
    if opts.get("coordinates") is not None:
        if isinstance(opts.get("coordinates"), str):
            try:
                opts["coordinates"] = np.asarray([float(x) for x in opts.get("coordinates").split(",")]).reshape(-1,3)
            except:
                logger.error("Coordinates argument not parsed from str correctly: {0}".format(opts.get("coordinates")))
                raise ValueError
        if isinstance(opts.get("coordinates"), list):
            opts["coordinates"] = np.array([float(x) for x in opts.get("coordinates")]).reshape(-1,3)

        if opts.get("coordinates").shape != (1,3):
            logger.error("Coordinates argument contains the wrong number of dimensions: {0}".format(opts.get("coordinates").shape))
            raise ValueError
    opts["resid"] = input_opts.get("resid")
    opts["lig_excl_rad"] = input_opts.get("lig_excl_rad")
    if opts.get("lig_excl_rad") is not None:
        opts["lig_excl_rad"] = float(opts["lig_excl_rad"])
    opts["lig_incl_rad"] = input_opts.get("lig_incl_rad")
    if opts.get("lig_incl_rad") is not None:
        opts["lig_incl_rad"] = float(opts["lig_incl_rad"])
    opts["min_volume"] = input_opts.get("min_volume")
    if opts.get("min_volume") is not None:
        opts["min_volume"] = float(input_opts.get("min_volume"))
    else:
        if opts.get("mode") == "all":
            opts["min_volume"] = 200

    opts["subdivide"] = input_opts.get("subdivide", False)
    if not isinstance(opts["subdivide"], bool):
        opts["subdivide"] = False
    if opts["subdivide"]:
        opts["max_clusters"] = int(input_opts.get("max_clusters", 50))
        opts["min_subpocket_rad"] = float(input_opts.get("min_subpocket_rad", 1.7))
        opts["max_subpocket_rad"] = float(input_opts.get("max_subpocket_rad", 3.4))
        opts["min_subpocket_surf_rad"] = float(input_opts.get("min_subpocket_surf_rad", 1.0))
        opts["radial_sampling"] = float(input_opts.get("radial_sampling", 0.1))
        opts["inclusion_radius_buffer"] = float(input_opts.get("inclusion_radius_buffer", 1.0))
        opts["min_cluster_size"] = int(input_opts.get("min_cluster_size", 50))

    opts["project_dir"] = input_opts.get("project_dir")
    opts["output_dir"] = input_opts.get("output_dir")
    opts["prefix"] = input_opts.get("prefix")
    if opts["prefix"] is None:
        if opts.get("prot_file") is not None:
            opts["prefix"] = "{0}_{1}".format(timestamp, os.path.splitext(os.path.basename(opts["prot_file"]))[0])
        elif opts.get("protein") is not None:
            opts["prefix"] = "{0}_{1}".format(timestamp, opts.get("protein").split()[0].strip("(").strip(")"))
        else:
            logger.error("No protein input detected: either prot_file or the PyMOL protein selection must be defined")
            raise ValueError("No protein geometry defined: provide either a protein file or protein PyMOL selection")

    if opts.get("output_dir") is None:
        if opts.get("project_dir") is not None:
            opts["output_dir"] = os.path.join(opts.get("project_dir"), "{0}.pyvol".format(opts.get("prefix")))
        else:
            opts["output_dir"] = os.path.join(os.getcwd(), "{0}.pyvol".format(opts.get("prefix")))

    utilities.check_dir(opts.get("output_dir"))

    if opts.get("prot_file") is None:
        opts["prot_file"] = os.path.join(opts.get("output_dir"), "{0}_prot.pdb".format(opts.get("prefix")))

    if (opts.get("ligand") is not None) and (opts.get("lig_file") is None):
        opts["lig_file"] = os.path.join(opts.get("output_dir"), "{0}_lig.pdb".format(opts.get("prefix")))


    opts["logger_stream_level"] = input_opts.get("logger_stream_level")
    if opts["logger_stream_level"] not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        opts["logger_stream_level"] = None
    opts["logger_file_level"] = input_opts.get("logger_file_level")
    if opts["logger_file_level"] not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
        opts["logger_file_level"] = None

    opts["protein"] = input_opts.get("protein")
    opts["ligand"] = input_opts.get("ligand")
    opts["protein_only"] = input_opts.get("protein_only")
    if not isinstance(opts["protein_only"], bool):
        opts["protein_only"] = False
    opts["display_mode"] = input_opts.get("display_mode")
    if not opts["display_mode"] in ["solid", "mesh", "spheres"]:
        opts["display_mode"] = "solid"
    opts["palette"] = input_opts.get("palette")
    if opts.get("palette") is not None:
        palette_valid = False
        if isinstance(opts.get("palette"), str):
            fragments = re.split(r"[\(\)]", opts.get("palette"))
            cleaned_pieces = []
            for fragment in fragments:
                pieces = list(filter(None, fragment.split(",")))

                if len(pieces) > 0:
                    try:
                        rgb = [float(piece) for piece in pieces]
                        cleaned_pieces.append(rgb)
                    except:
                        cleaned_pieces.extend(pieces)
            opts["palette"] = cleaned_pieces

    if opts.get("alpha") is not None:
        opts["alpha"] = float(input_opts.get("alpha"))
    else:
        opts["alpha"] = 1.0

    # Clean options
    if opts["prot_file"] is None:
        logger.error("A protein file must be provided--Terminating job")
        raise

    if opts["constrain_radii"]:
        if opts["min_rad"] < 1.2:
            logger.info("Minimum radius constrained from {0} to 1.2".format(opts["min_rad"]))
            opts["min_rad"] = 1.2
        elif opts["min_rad"] > 2.0:
            logger.info("Minimum radius constrained from {0} to 2.0".format(opts["min_rad"]))
            opts["min_rad"] = 2.0

        if opts["max_rad"] < 2.0:
            logger.info("Maximum radius constrained from {0} to 2.0".format(opts["max_rad"]))
            opts["max_rad"] = 2.0
        elif opts["max_rad"] > 5.0:
            logger.info("Maximum radius constrained from {0} to 5.0".format(opts["max_rad"]))
            opts["max_rad"] = 5.0

    if opts["mode"] in ["all", "largest"]:
        opts["lig_file"] = None
        opts["coordinates"] = None
        opts["resid"] = None
        opts["lig_excl_rad"] = None
        opts["lig_incl_rad"] = None
    else:
        if opts["lig_file"] is not None:
            if opts["mode"] is None:
                logger.info("Pocket identified through provided ligand")
            opts["mode"] = "specific"
            opts["resid"] = None
            opts["coordinates"] = None
        elif opts["resid"] is not None:
            if opts["mode"] is None:
                logger.info("Pocket identified through resid: {0}".format(opts["resid"]))
            opts["mode"] = "specific"
            opts["coordinates"] = None
        elif opts["coordinates"] is not None:
            logger.info("Pocket identified through coordinates: {0}".format(opts["coordinates"]))
            opts["mode"] = "specific"
        else:
            opts["mode"] = "largest"

    if opts["subdivide"]:
        if opts["max_clusters"] <= 1:
            logger.warning("Subpocket analysis impossible with maximum clusters of {0}; disabling subpocket analysis".format(opts["max_clusters"]))
            opts["subdivide"] = False
            opts["max_clusters"] = None
            opts["min_subpocket_rad"] = None
            opts["max_cluster_rad"] = None
            opts["min_subpocket_surf_rad"] = None
            opts["radial_sampling"] = None
            opts["inclusion_radius_buffer"] = None
            opts["min_cluster_size"] = None

    # Remove all empty options
    cleaned_opts = {}
    for k, v in opts.items():
        if v is not None:
            cleaned_opts[k] = v

    logger.debug("Input options sanitized")
    return cleaned_opts


def opts_to_cfg(opts):
    """ creates the configuration file corresponding to input options

    Args:
      opts (dict): option dictionary for which to create a configuration object

    Returns:
      config (ConfigParser): configuration object containing formatted options
    """

    config = configparser.ConfigParser()

    config.add_section("General")
    if opts.get("prot_file") is not None:
        config.set("General", "prot_file", str(opts.get("prot_file")))
    if opts.get("lig_file") is not None:
        config.set("General", "lig_file", str(opts.get("lig_file")))
    if opts.get("min_rad") is not None:
        config.set("General", "min_rad", str(opts.get("min_rad")))
    if opts.get("max_rad") is not None:
        config.set("General", "max_rad", str(opts.get("max_rad")))
    if opts.get("constrain_radii") is not None:
        config.set("General", "constrain_radii", str(opts.get("constrain_radii")))

    config.add_section("Specification")
    if opts.get("mode") is not None:
        config.set("Specification", "mode", str(opts.get("mode")))
    if opts.get("resid") is not None:
        config.set("Specification", "resid", str(opts.get("resid")))
    if opts.get("coordinates") is not None:
        config.set("Specification", "coordinates", str(opts.get("coordinates")))
    if opts.get("lig_excl_rad") is not None:
        config.set("Specification", "lig_excl_rad", str(opts.get("lig_excl_rad")))
    if opts.get("lig_incl_rad") is not None:
        config.set("Specification", "lig_incl_rad", str(opts.get("lig_incl_rad")))
    if opts.get("min_volume") is not None:
        config.set("Specification", "min_volume", str(opts.get("min_volume")))

    config.add_section("Partitioning")
    if opts.get("subdivide") is not None:
        config.set("Partitioning", "subdivide", str(opts.get("subdivide")))
    if opts.get("max_clusters") is not None:
        config.set("Partitioning", "max_clusters", str(opts.get("max_clusters")))
    if opts.get("min_subpocket_rad") is not None:
        config.set("Partitioning", "min_subpocket_rad", str(opts.get("min_subpocket_rad")))
    if opts.get("max_subpocket_rad") is not None:
        config.set("Partitioning", "max_subpocket_rad", str(opts.get("max_subpocket_rad")))
    if opts.get("min_subpocket_surf_rad") is not None:
        config.set("Partitioning", "min_subpocket_surf_rad", str(opts.get("min_subpocket_surf_rad")))
    if opts.get("radial_sampling") is not None:
        config.set("Partitioning", "radial_sampling", str(opts.get("radial_sampling")))
    if opts.get("inclusion_radius_buffer") is not None:
        config.set("Partitioning", "inclusion_radius_buffer", str(opts.get("inclusion_radius_buffer")))
    if opts.get("min_cluster_size") is not None:
        config.set("Partitioning", "min_cluster_size", str(opts.get("min_cluster_size")))

    config.add_section("Output")
    if opts.get("project_dir") is not None:
        config.set("Output", "project_dir", str(opts.get("project_dir")))
    if opts.get("output_dir") is not None:
        config.set("Output", "output_dir", str(opts.get("output_dir")))
    if opts.get("prefix") is not None:
        config.set("Output", "prefix", str(opts.get("prefix")))
    if opts.get("logger_stream_level") is not None:
        config.set("Output", "logger_stream_level", str(opts.get("logger_stream_level")))
    if opts.get("logger_file_level") is not None:
        config.set("Output", "logger_file_level", str(opts.get("logger_file_level")))


    config.add_section("PyMOL")
    if opts.get("protein") is not None:
        config.set("PyMOL", "protein", str(opts.get("protein")))
    if opts.get("ligand") is not None:
        config.set("PyMOL", "ligand", str(opts.get("ligand")))
    if opts.get("protein_only") is not None:
        config.set("PyMOL", "protein_only", str(opts.get("protein_only")))
    if opts.get("display_mode") is not None:
        config.set("PyMOL", "display_mode", str(opts.get("display_mode")))
    if opts.get("palette") is not None:
        config.set("PyMOL", "palette", str(opts.get("palette")))
    if opts.get("alpha") is not None:
        config.set("PyMOL", "alpha", str(opts.get("alpha")))

    return config

def defaults_to_cfg():
    """ Creates a blank template cfg with all accepted fields and reasonable default values

    Returns:
      config (ConfigParser): configuration object containing defaults
    """
    config = configparser.ConfigParser(allow_no_value=True)
    config.add_section("General")
    config.set("General", "prot_file")
    config.set("General", "lig_file")
    config.set("General", "min_rad", "1.4")
    config.set("General", "max_rad", "3.4")
    config.set("General", "constrain_radii", "True")

    config.add_section("Specification")
    config.set("Specification", "mode", "largest")
    config.set("Specification", "coordinates")
    config.set("Specification", "resid")
    config.set("Specification", "lig_excl_rad")
    config.set("Specification", "lig_incl_rad")
    config.set("Specification", "min_volume", "200")

    config.add_section("Partitioning")
    config.set("Partitioning", "subdivide", "False")
    config.set("Partitioning", "max_clusters")
    config.set("Partitioning", "min_subpocket_rad", "1.7")
    config.set("Partitioning", "max_subpocket_rad", "3.4")
    config.set("Partitioning", "min_subpocket_surf_rad", "1.0")
    config.set("Partitioning", "radial_sampling", "0.1")
    config.set("Partitioning", "inclusion_radius_buffer", "1.0")
    config.set("Partitioning", "min_cluster_size", "50")

    config.add_section("Output")
    config.set("Output", "project_dir")
    config.set("Output", "prefix")
    config.set("Output", "logger_stream_level", "INFO")
    config.set("Output", "logger_file_level", "DEBUG")

    config.add_section("PyMOL")
    config.set("PyMOL", "protein")
    config.set("PyMOL", "ligand")
    config.set("PyMOL", "protein_only", "False")
    config.set("PyMOL", "display_mode", "solid")
    config.set("PyMOL", "palette")
    config.set("PyMOL", "alpha", "0.85")

    return config


def defaults_to_file(filename):
    """ writes a default configuation file to disk

    Args:
      filename (str): output filename to which to write the configuration file to disk
    """

    cfg_to_file(defaults_to_cfg(), filename)


def cfg_to_opts(config):
    """ converts a config to opts

    Args:
      config (ConfigParser): configuration object from which options are to be extracted

    Returns:
      opts (dict): dictionary of options read in from the configuration object
    """

    opts = {}
    opts["prot_file"] = config.get("General", "prot_file", fallback=None)
    opts["lig_file"] = config.get("General", "lig_file", fallback=None)
    opts["min_rad"] = config.getfloat("General", "min_rad", fallback=1.4)
    opts["max_rad"] = config.getfloat("General", "max_rad", fallback=3.4)

    opts["mode"] = config.get("Specification", "mode", fallback=None)
    opts["resid"] = config.get("Specification", "resid", fallback=None)
    opts["coordinates"] = config.get("Specification", "coordinates", fallback=None)
    opts["lig_excl_rad"] = config.getfloat("Specification", "lig_excl_rad", fallback=-1)
    opts["lig_incl_rad"] = config.getfloat("Specification", "lig_incl_rad", fallback=-1)

    opts["subdivide"] = config.getboolean("Partitioning", "subdivide", fallback=False)
    opts["min_volume"] = config.getint("Partitioning", "min_volume", fallback=200)
    opts["max_clusters"] = config.getint("Partitioning", "max_clusters", fallback=100)
    opts["min_subpocket_rad"] = config.getfloat("Partitioning", "min_subpocket_rad", fallback=1.7)
    opts["max_subpocket_rad"] = config.getfloat("Partitioning", "max_subpocket_rad", fallback=3.4)
    opts["min_subpocket_surf_rad"] = config.getfloat("Partitioning", "min_subpocket_surf_rad", fallback=1.0)
    opts["radial_sampling"] = config.getfloat("Partitioning", "radial_sampling", fallback=0.1)
    opts["inclusion_radius_buffer"] = config.getfloat("Partitioning", "inclusion_radius_buffer", fallback=1.0)
    opts["min_cluster_size"] = config.getint("Partitioning", "min_cluster_size", fallback=50)

    opts["project_dir"] = config.get("Output", "project_dir", fallback=None)
    opts["output_dir"] = config.get("Output", "output_dir", fallback=None)
    opts["prefix"] = config.get("Output", "prefix", fallback=None)
    opts["logger_stream_level"] = config.get("Output", "logger_stream_level", fallback="INFO")
    opts["logger_file_level"] = config.get("Output", "logger_file_level", fallback="DEBUG")

    opts["protein"] = config.get("PyMOL", "protein", fallback=None)
    opts["ligand"] = config.get("PyMOL", "ligand", fallback=None)
    opts["protein_only"] = config.get("PyMOL", "protein_only", fallback=True)
    opts["display_mode"] = config.get("PyMOL", "display_mode", fallback="solid")
    opts["palette"] = config.get("PyMOL", "palette", fallback=None)
    opts["alpha"] = config.get("PyMOL", "alpha", fallback=0.85)

    return opts


def cfg_to_file(cfg, filename):
    """ writes a configuration to file

    Args:
      cfg (ConfigParser): configuration object to be written to disk
      filename (str): target filename on disk
    """

    with open(filename, 'w') as configfile:
        cfg.write(configfile)
        logger.info("Configuration file written to {0}".format(filename))


def file_to_cfg(filename):
    """ reads a cfg file into a configuration object

    Args:
      filename (str): input filename of a configuration file

    Returns:
      config (ConfigParser): configuration object holding the contents of the file
    """

    config = configparser.ConfigParser()
    config.read(filename)
    logger.info("Configuration file read from {0}".format(filename))
    return config


def file_to_opts(filename):
    """ reads a cfg file and converts it into an options dictionary

    Args:
      filename (str): input filename of a configuration file

    Returns:
      opts (dict): dictionary object containing PyVOL options
    """

    return cfg_to_opts(file_to_cfg(filename))


def opts_to_file(opts, filename=None):
    """ writes options to a configuration file

    Args:
      opts (dict): dictionary object containing PyVOL options
      filename (str): target file to which to write the configuration

    """

    if filename is None:
        filename = os.path.join(opts.get("output_dir"), "{0}.cfg".format(opts.get("prefix")))

    cfg_to_file(opts_to_cfg(opts), filename)
