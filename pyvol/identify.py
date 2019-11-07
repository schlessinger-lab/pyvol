
from .spheres import Spheres
from . import cluster, utilities
import inspect
import itertools
import logging
import numpy as np
import os

logger = logging.getLogger(__name__)
main_logger = logging.getLogger("pyvol")

def pocket(prot_file, mode="largest", lig_file=None, coordinate=None, resid=None, residue_coordinates=None, min_rad=1.4, max_rad=3.4, lig_excl_rad=None, lig_incl_rad=None, subdivide=False, minimum_volume=200, min_subpocket_rad=1.7, min_subpocket_surf_rad=1.0, max_clusters=None, prefix=None, output_dir=None, constrain_inputs=False):
    """Calculates the SES for a binding pocket

    Args:
      prot_file (str): filename for the input pdb file containing the peptidee
      mode (str): pocket identification mode (can be largest, all, or specific) (Default value = "largest")
      lig_file (str): filename for the input pdb file containing a ligand (Default value = None)
      coordinate ([float]): 3D coordinate used for pocket specification (Default value = None)
      resid (str): residue identifier for pocket specification (Default value = None)
      residue_coordinates ([float]): 3D coordinate of an atom in a surrounding residue used for pocket specification (Default value = None)
      min_rad (float): radius for SAS calculations (Default value = 1.4)
      max_rad (float): radius used to identify the outer, bulk solvent exposed surface (Default value = 3.4)
      lig_excl_rad (float): maximum distance from a provided ligand that can be included in calculated pockets (Default value = None)
      lig_incl_rad (float): minimum distance from a provided ligand that should be included in calculated pockets when solvent border is ambiguous (Default value = None)
      subdivide (bool): calculate subpockets? (Default value = False)
      minimum_volume (float): minimum volume of pockets returned when running in 'all' mode (Default value = 200)
      min_subpocket_rad (float): minimum radius that identifies distinct subpockets (Default value = 1.7)
      min_subpocket_surf_rad (float): radius used to calculate subpocket surfaces (Default value = 1.0)
      max_clusters (int): maximum number of clusters (Default value = None)
      prefix (str): identifying string for output (Default value = None)
      output_dir (str): filename of the directory in which to place all output; can be absolute or relative (Default value = None)
      constrain_inputs (bool): restrict quantitative input parameters to tested values? (Default value = False)

    Returns:
      pockets ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct pocket or subpocket

    """



    if prefix is None:
        prefix = os.path.splitext(os.path.basename(prot_file))[0]

    logger.debug("Output prefix: {0}".format(prefix))

    min_rad = float(min_rad)
    max_rad = float(max_rad)
    min_subpocket_rad = float(min_subpocket_rad)
    if minimum_volume is not None:
        minimum_volume = int(minimum_volume)
    if max_clusters is not None:
        max_clusters = int(max_clusters)

    if constrain_inputs:
        if min_rad < 1.2:
            logger.warning("Minimum radii under 1.2 and not supported and can lead to bizarre results or crashes; setting the minimum radius to 1.2")
            min_rad = 1.2
        elif min_rad > 2.0:
            logger.warning("Minimum radii under 1.2 and not supported and can lead to bizarre results or crashes; setting the minimum radius to 2.0")
            min_rad = 2.0
        if max_rad > 5.0:
            max_rad = 5.0
            logger.warning("Maximum radii exceeds maximum threshold of 5.0 and is being set to 5.0")
        elif max_rad < 2.0:
            max_rad = 2.0
            logger.warning("Maximum radii is below the minimum threshold of 2.0 and is being set to 2.0")
    else:
        if (min_rad < 1.2) or (min_rad > 2.0):
            logger.warning("Minimum radius is outside of usual bounds and might cause a crash")

    p_s = Spheres(pdb=prot_file)

    if lig_file is not None:
        if lig_incl_rad is not None:
            lig_incl_rad = float(lig_incl_rad)
            logger.debug("Ligand-included radius applied")
        l_s = Spheres(pdb=lig_file, r=lig_incl_rad)
    else:
        l_s = None

    pl_s = p_s + l_s

    pl_bs = pl_s.calculate_surface(probe_radius=max_rad)[0]
    logger.debug("Outer boundary surface calculated")

    pa_s = p_s + pl_bs
    if (l_s is not None) and (lig_excl_rad is not None):
        le_s = Spheres(xyz=l_s.xyzr, r=float(lig_excl_rad))
        le_bs = le_s.calculate_surface(probe_radius=max_rad)[0]
        pa_s = pa_s + le_bs
        logger.debug("Ligand-excluded radius applied")

    if mode == "all":
        all_pockets = pa_s.calculate_surface(probe_radius=min_rad, all_components=True, minimum_volume=minimum_volume)
        for index, pocket in enumerate(all_pockets):
            pocket.name = "{0}_p{1}".format(prefix, index)
        logger.debug("Pockets calculated using mode 'all': {0}".format(len(all_pockets)))
        logger.warning("Subpocket clustering not currently supported when calculating all independent pockets")
    else:
        if mode == "largest":
            bp_bs = pa_s.calculate_surface(probe_radius=min_rad, all_components=True, largest_only=True)[0]
            logger.debug("Largest pocket identified and calculated")
        elif mode == "specific":
            if coordinate is not None:
                if isinstance(coordinate, ("".__class__, u"".__class__)):
                    coordinate = coordinate.split()
                    coordinate = np.array([float(x) for x in coordinate])
                coordinate = coordinate.reshape(1, -1)
                logger.debug("Specific pocket identified from coordinate: {0}".format(coordinate))
            elif resid is not None:
                resid = str(resid)
                chain = None
                if not resid[0].isdigit():
                    chain = resid[0]
                    resid = int(resid[1:])
                else:
                    resid = int(resid)
                res_coords = utilities.coordinates_for_resid(prot_file, resid=resid, chain=chain)
                p_bs = p_s.calculate_surface(probe_radius=min_rad)[0]
                coordinate = p_bs.nearest_coord_to_external(res_coords).reshape(1, -1)
                logger.debug("Specific pocket identified from residue: {0} -> {1}".format(resid, coordinate))
            elif residue_coordinates is not None:
                p_bs = p_s.calculate_surface(probe_radius=min_rad)[0]
                coordinate = p_bs.nearest_coord_to_external(residue_coordinates).reshape(1, -1)
                logger.debug("Specific pocket identified from residue coordinate: {0} -> {1}".format(residue_coordinates, coordinate))
            elif l_s is not None:
                lig_coords = l_s.xyz
                coordinate = np.mean(l_s.xyz, axis=0).reshape(1, -1)
                logger.debug("Specific pocket identified from mean ligand position: {0}".format(coordinate))
            else:
                logger.error("A coordinate, ligand, or residue must be supplied to run in specific mode")
                return None
            bp_bs = pa_s.calculate_surface(probe_radius=min_rad, coordinate=coordinate)[0]
        else:
            logger.error("Unrecognized mode <{0}>--should be 'all', 'largest', or 'specific'".format(mode))

        bp_bs.name = "{0}_p0".format(prefix)

        if bp_bs.mesh.volume > pl_bs.mesh.volume:
            logger.error("Binding pocket not correctly identified--try an alternative method to specify the binding pocket")
            return None
        else:
            all_pockets = [bp_bs]

        if subdivide:
            all_pockets.extend(subpockets(bounding_spheres = pa_s, ref_spheres = bp_bs, min_rad=min_rad, max_rad=max_rad, min_subpocket_rad=min_subpocket_rad, max_clusters=max_clusters, prefix=prefix))
            logger.debug("Subpockets identified: {0}".format(len(all_pockets) - 1))

    if output_dir is not None:
        write_report(all_pockets, output_dir, prefix)

    return all_pockets


def subpockets(bounding_spheres, ref_spheres, min_rad, max_rad, min_subpocket_rad=1.7, min_subpocket_surf_rad=1.0, max_subpocket_rad=None, sampling=0.1, inclusion_radius_buffer=1.0, min_cluster_size=50, max_clusters=None, prefix=None):
    """

    Args:
      bounding_spheres (Spheres): a Spheres object containing both the peptide and solvent exposed face external spheres
      ref_spheres (Spheres): a Spheres object holding the interior spheres that define the pocket to be subdivided
      min_rad (float): radius for original SES calculations (Default value = 1.4)
      max_rad (float): radius originally used to identify the outer, bulk solvent exposed surface (Default value = 3.4)
      min_subpocket_rad (float): minimum radius that identifies distinct subpockets (Default value = 1.7)
      min_subpocket_surf_rad (float): radius used to calculate subpocket surfaces (Default value = 1.0)
      max_subpocket_rad (float): maximum spheres radius used for subpocket clustering (Default value = None)
      sampling (float): radial sampling frequency for clustering (Default value = 0.1)
      inclusion_radius_buffer (float): defines the inclusion distance for nonextraneous spheres in combination with min_rad and max_rad (Default value = 1.0)
      min_cluster_size (int): minimum number of spheres that can constitute a proper clusterw (Default value = 50)
      max_clusters (int): maximum number of clusters (Default value = None)
      prefix (str): identifying string for output (Default value = None)

    Returns:
      pockets ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct subpocket
    """

    if max_subpocket_rad is None:
        max_subpocket_rad = max_rad

    nonextraneous_rad = min_rad + max_rad + inclusion_radius_buffer
    nonextraneous_spheres = bounding_spheres.identify_nonextraneous(ref_spheres=ref_spheres, radius=nonextraneous_rad)
    logger.debug("Nonextraneous bounding spheres identified")

    sampling_radii = np.flip(np.arange(min_rad, max_subpocket_rad, sampling), axis=0)
    unmerged_sphere_lists = utilities.sphere_multiprocessing(nonextraneous_spheres, sampling_radii, all_components=True)
    spheres = cluster.merge_sphere_list(itertools.chain(*unmerged_sphere_lists))
    logger.debug("Naive subpocket clusters identified")

    cluster.hierarchically_cluster_spheres(spheres, ordered_radii=sampling_radii, min_new_radius=min_subpocket_rad, min_cluster_size=min_cluster_size, max_clusters=max_clusters)
    logger.debug("Subpockets distinguished after hierarchical clustering")

    cluster.remove_overlap(spheres, radii=sampling_radii, spacing=sampling)
    cluster.remove_overlap(spheres)
    cluster.remove_interior(spheres)
    grouped_list = cluster.extract_groups(spheres, surf_radius=min_subpocket_surf_rad, prefix=prefix)
    logger.debug("Subpockets pruned of interior and overlapping spheres")
    return grouped_list


def write_report(all_pockets, output_dir, prefix):
    """ Write a brief report of calculated volumes to file

    Args:
      all_pockets ([Spherese]): a list of Spheres objects each of which contains the complete information about a distinct pocket or subpocket
      output_dir (str): output directory, relative or absolute
      prefix (str): identifying prefix for output files

    """
    import os
    import pandas as pd

    utilities.check_dir(output_dir)

    rept_list = []

    for pocket in all_pockets:
        spheres_name = os.path.join(output_dir, "{0}.csv".format(pocket.name))
        pocket.write(spheres_name)
        rept_list.append({"name": pocket.name,
                          "volume": pocket.mesh.volume
                          })
    rept_df = pd.DataFrame(rept_list)
    rept_name = os.path.join(output_dir, "{0}_rept.csv".format(prefix))
    rept_df.to_csv(rept_name, index=False)
    logger.debug("Report written to: {0}".format(rept_name))
