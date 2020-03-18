
from .spheres import Spheres
from . import cluster, configuration, utilities
import glob
import inspect
import itertools
import logging
import numpy as np
import os
import pandas as pd
import shutil
import sys

logger = logging.getLogger(__name__)

def load_calculation(data_dir, input_opts=None):
    """ load the results of a calculation from file

    Args:
      data_dir (str): directory where previous calculation results are stored
      input_opts (dict): dictionary of pyvol options that is used to update the options read in from file

    Returns:
      pockets ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct pocket or subpocket
      opts (dict): updated PyVOL options dictionary

    """

    if not os.path.isdir(data_dir):
        logger.error("{0} is not a directory".format(data_dir))
        raise FileNotFoundError

    cfg_files = glob.glob(os.path.join(data_dir, "*.cfg"))
    if len(cfg_files) == 0:
        logger.error("No cfg file found in {0}".format(data_dir))
        raise FileNotFoundError
    elif len(cfg_files) > 1:
        logger.error("Multiple cfg files found in {0}".format(data_dir))
        raise FileNotFoundError

    opts = configuration.file_to_opts(cfg_files[0])
    if isinstance(input_opts, dict):
        opts.update(input_opts)
        opts = configuration.clean_opts(opts)

    rept_file = os.path.join(data_dir, "{0}.rept".format(opts.get("prefix")))
    if not os.path.isfile(rept_file):
        logger.error("No rept file found at {0}".format(rept_file))
        raise FileNotFoundError

    rept_df = pd.read_csv(rept_file)
    pockets = []
    for index, row in rept_df.iterrows():
        xyzrg_file = os.path.join(data_dir, "{0}.xyzrg".format(row["name"]))
        pockets.append(Spheres(spheres_file=xyzrg_file))

    return pockets, opts


def pocket(**opts):
    """Calculates the SES for a binding pocket

    Args:
      opts (dict): dictionary containing all PyVOL options (see pyvol.pymol_interface.pymol_pocket_cmdline for details)

    Returns:
      pockets ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct pocket or subpocket

    """

    if os.path.dirname(opts.get("prot_file")) != opts.get("output_dir"):
        new_prot_file = os.path.join(opts.get("output_dir"), os.path.basename(opts.get("prot_file")))
        shutil.copyfile(opts.get("prot_file"), new_prot_file)
        opts["prot_file"] = new_prot_file

        if opts.get("lig_file") is not None:
            new_lig_file = os.path.join(opts.get("output_dir"), os.path.basename(opts.get("lig_file")))
            shutil.copyfile(opts.get("lig_file"), new_lig_file)
            opts["lig_file"] = new_lig_file

    p_s = Spheres(pdb=opts.get("prot_file"), name="{0}_prot".format(opts.get("prefix")))
    logger.debug("Protein geometry read from {0}".format(opts.get("prot_file")))

    pl_s = p_s.copy()
    if opts.get("lig_file") is not None:
        l_s = Spheres(pdb=opts.get("lig_file"), r=opts.get("lig_incl_rad"), name="{0}_lig_incl".format(opts.get("prefix")))
        logger.debug("Ligand geometry read from {0}".format(opts.get("lig_file")))
        if opts.get("lig_incl_rad") is not None:
            pl_s = p_s + l_s
            logger.debug("Ligand-inclusion radius of {0} applied".format(opts.get("lig_incl_rad")))
    else:
        l_s = None

    pl_s.name = "{0}_interior".format(opts.get("prefix"))

    pl_bs = pl_s.calculate_surface(probe_radius=opts.get("max_rad"))[0]
    logger.debug("Outer bulk-solvent surface calculated")
    pl_bs.name = "{0}_boundary".format(opts.get("prefix"))

    pa_s = p_s + pl_bs
    pa_s.name = "{0}_exterior".format(opts.get("prefix"))
    if (l_s is not None) and (opts.get("lig_excl_rad") is not None):
        le_s = Spheres(xyz=l_s.xyzr, r=opts.get("lig_excl_rad"), name="{0}_lig_excl".format(opts.get("prefix")))
        le_bs = le_s.calculate_surface(probe_radius=opts.get("max_rad"))[0]
        pa_s = pa_s + le_bs
        logger.debug("Ligand-excluded radius of {0} applied".format(opts.get("lig_excl_rad")))

    if opts.get("mode") == "all":
        all_pockets = pa_s.calculate_surface(probe_radius=opts.get("min_rad"), all_components=True, min_volume=opts.get("min_volume"))
        for index, pocket in enumerate(all_pockets):
            pocket.name = "{0}_p{1}".format(opts.get("prefix"), index)
        logger.info("Pockets calculated using mode 'all': {0}".format(len(all_pockets)))
        if opts.get("subdivide"):
            logger.warning("Subpocket clustering not currently supported when calculating all independent pockets")
    else:
        if opts.get("mode") == "largest":
            bp_bs = pa_s.calculate_surface(probe_radius=opts.get("min_rad"), all_components=True, largest_only=True)[0]
            logger.info("Largest pocket identified")
        elif opts.get("mode") == "specific":
            if opts.get("coordinates") is not None:
                coordinate = opts.get("coordinates")
                logger.info("Specific pocket identified from coordinate: {0}".format(opts.get("coordinates")))
            elif opts.get("resid") is not None:
                resid = str(opts.get("resid"))
                chain = None
                if not resid[0].isdigit():
                    chain = resid[0]
                    resid = int(resid[1:])
                else:
                    resid = int(resid)
                coordinate = utilities.coordinates_for_resid(opts.get("prot_file"), resid=resid, chain=chain)
                logger.info("Specific pocket identified from residue: {0} -> {1} (truncated)".format(opts.get("resid"), coordinate[0,:]))
            elif l_s is not None:
                lig_coords = l_s.xyz
                coordinate = np.mean(l_s.xyz, axis=0).reshape(1, -1)
                logger.info("Specific pocket identified from mean ligand position: {0}".format(coordinate))
            else:
                logger.error("A coordinate, ligand, or residue must be supplied to run in specific mode")
                return None

            p_bs = p_s.calculate_surface(probe_radius=opts.get("min_rad"))[0]
            id_coord = p_bs.nearest_coord_to_external(coordinate).reshape(1, -1)
            bp_bs = pa_s.calculate_surface(probe_radius=opts.get("min_rad"), coordinate=id_coord)[0]
        else:
            logger.error("Unrecognized mode <{0}>--should be 'all', 'largest', or 'specific'".format(opts.get("mode")))
            return None

        bp_bs.name = "{0}_p0".format(opts.get("prefix"))

        if bp_bs.mesh.volume > pl_bs.mesh.volume:
            logger.error("Binding pocket not correctly identified--try an alternative method to specify the binding pocket")
            return [], opts
        else:
            all_pockets = [bp_bs]

        if opts.get("subdivide"):
            all_pockets.extend(subpockets(bounding_spheres = pa_s, ref_spheres = bp_bs, **opts))
            logger.info("Subpockets identified: {0}".format(len(all_pockets) - 1))

    write_report(all_pockets, **opts)
    write_cfg(**opts)

    return all_pockets, opts


def pocket_wrapper(**opts):
    """ wrapper for pocket that configures the logger, sanitizes inputs, and catches errors; useful when running from the command line or PyMOL but split from the core code for programmatic usage

    Args:
      opts (dict): dictionary containing all PyVOL options (see pyvol.pymol_interface.pymol_pocket_cmdline for details)

    Returns:
      pockets ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct pocket or subpocket
      output_opts (dict): dictionary containing the actual options used in the pocket calculation

    """

    opts = configuration.clean_opts(opts)

    utilities.check_dir(opts.get("output_dir"))

    log_file = os.path.join(opts.get("output_dir"), "{0}.log".format(opts.get("prefix")))
    utilities.configure_logger(filename=log_file, stream_level=opts.get("logger_stream_level"), file_level=opts.get("logger_file_level"))
    logger.debug("Logger configured")

    all_pockets, output_opts = pocket(**opts)

    return all_pockets, output_opts


def subpockets(bounding_spheres, ref_spheres, **opts):
    """

    Args:
      bounding_spheres (Spheres): a Spheres object containing both the peptide and solvent exposed face external spheres
      ref_spheres (Spheres): a Spheres object holding the interior spheres that define the pocket to be subdivided
      opts (dict): a dictionary containing all PyVOL options (see pyvol.configuration.clean_opts for details)

    Returns:
      grouped_list ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct subpocket

    """

    nonextraneous_rad = opts.get("min_rad") + opts.get("max_rad") + opts.get("inclusion_radius_buffer")
    nonextraneous_spheres = bounding_spheres.identify_nonextraneous(ref_spheres=ref_spheres, radius=nonextraneous_rad)

    sampling_radii = np.flip(np.arange(opts.get("min_rad"), opts.get("max_subpocket_rad"), opts.get("radial_sampling")), axis=0)
    unmerged_sphere_lists = utilities.sphere_multiprocessing(nonextraneous_spheres, sampling_radii, all_components=True)
    spheres = cluster.merge_sphere_list(itertools.chain(*unmerged_sphere_lists))

    cluster.hierarchically_cluster_spheres(spheres, ordered_radii=sampling_radii, min_new_radius=opts.get("min_subpocket_rad"), min_cluster_size=opts.get("min_cluster_size"), max_clusters=opts.get("max_clusters"))

    cluster.remove_overlap(spheres, radii=sampling_radii, spacing=opts.get("radial_sampling"))
    cluster.remove_overlap(spheres)
    cluster.remove_interior(spheres)
    grouped_list = cluster.extract_groups(spheres, surf_radius=opts.get("min_subpocket_surf_rad"), prefix=opts.get("prefix"))
    return grouped_list


def write_cfg(**opts):
    """ write the processed configuration to file

    Args:
      output_dir (str): output directory, relative or absolute
      prefix (str): identifying prefix for the output files

    """

    utilities.check_dir(opts.get("output_dir"))
    configuration.opts_to_file(opts)


def write_report(all_pockets, **opts):
    """ Write a brief report of calculated volumes to file

    Args:
      all_pockets ([Spheres]): a list of Spheres objects each of which contains the complete information about a distinct pocket or subpocket
      output_dir (str): output directory, relative or absolute
      prefix (str): identifying prefix for output files

    """
    import os
    import pandas as pd

    utilities.check_dir(opts.get("output_dir"))

    rept_list = []

    for pocket in all_pockets:
        spheres_name = os.path.join(opts.get("output_dir"), "{0}.xyzrg".format(pocket.name))
        pocket.write(spheres_name)
        rept_list.append({"name": pocket.name,
                          "volume": pocket.mesh.volume
                          })
    rept_df = pd.DataFrame(rept_list)
    rept_name = os.path.join(opts.get("output_dir"), "{0}.rept".format(opts.get("prefix")))
    rept_df.to_csv(rept_name, index=False)
    logger.info("Report written to: {0}".format(rept_name))
