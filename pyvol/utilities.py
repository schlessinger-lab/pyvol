
import itertools
import logging
import math
import multiprocessing
import numpy as np
import os
import scipy
import subprocess
import sys
import types

logger = logging.getLogger(__name__)

def calculate_rotation_matrix(ref_vector, new_vector):
    """ Calculates the 3D rotation matrix to convert from ref_vector to new_vector; not used in main PyVOL calculations

    Args:
        ref_vector (3x1 ndarray): original vector
        new_vector (3x1 ndarray): target vector

    Returns:
        rot_matrix (3x3 ndarray): rotation matrix to convert the original vector to the target vector
    """

    ref_vector = ref_vector / np.linalg.norm(ref_vector)
    new_vector = new_vector / np.linalg.norm(new_vector)

    rot_axis = np.cross(ref_vector, new_vector)
    if np.linalg.norm(rot_axis) != 0:
        rot_axis = rot_axis / np.linalg.norm(rot_axis)

    rot_angle = -1 * math.acos(np.dot(ref_vector, new_vector))
    ca = math.cos(rot_angle)
    sa = math.sin(rot_angle)

    rot_matrix = np.matrix([
        [
            1.0 + (1.0 - ca) * (rot_axis[0]**2 - 1.0),
            -rot_axis[2] * sa + (1.0 - ca) * rot_axis[0] * rot_axis[1],
            rot_axis[1] * sa + (1.0 - ca) * rot_axis[0] * rot_axis[2]
        ],[
            rot_axis[2] * sa + (1.0 - ca) * rot_axis[0] * rot_axis[1],
            1.0 + (1.0 - ca) * (rot_axis[1]**2 - 1.0),
            -1.0 * rot_axis[0] * sa + (1.0 - ca) * rot_axis[1] * rot_axis[2]
        ],[
            -1.0 * rot_axis[1] * sa + (1.0 - ca) * rot_axis[0] * rot_axis[2],
            rot_axis[0] * sa + (1.0 - ca) * rot_axis[1] * rot_axis[2],
            1.0 + (1.0 - ca) * (rot_axis[2]**2 - 1.0)
        ]])

    return rot_matrix


def closest_vertex_normals(ref_mesh, query_mesh, ref_coordinates=None, ref_radius=2, interface_gap=2):
    """ Returns the location and normal for the closest point between two meshes

    Args:
        ref_mesh (trimesh): origin mesh
        query_mesh (trimesh): target mesh
        ref_coordinates (3xN ndarray): coordinates used to specify the pertinent subregion on the ref_mesh
        ref_radius (float): radius used to identify points on the ref_mesh that are sufficiently close to the ref_coordinates
        interface_gap (float): maximum distance between the ref and query meshes at the identified point

    Returns:
        mean_pos (3x1 ndarray): coordinate of the central point between the meshes
        mean_normal (3x1 ndarray): normalized vector pointing from the ref_mesh to the query_mesh
    """

    if ref_coordinates is not None:
        reftree = scipy.spatial.cKDTree(ref_mesh.vertices)
        ref_groups = reftree.query_ball_point(ref_coordinates, ref_radius, n_jobs=-1)
        ref_indices = np.unique(list(itertools.chain.from_iterable(ref_groups)))
    else:
        ref_indices = np.arange(1, ref_mesh.vertices.shape[0])

    querytree = scipy.spatial.cKDTree(query_mesh.vertices)
    query_groups = querytree.query_ball_point(ref_mesh.vertices[ref_indices, :], interface_gap, n_jobs=-1)
    query_indices = np.unique(list(itertools.chain.from_iterable(query_groups)))

    kdtree = scipy.spatial.cKDTree(ref_mesh.vertices[ref_indices, :])
    dist, indices = kdtree.query(query_mesh.vertices[query_indices, :], n_jobs=-1)

    reorder = np.argsort(dist)
    for query_index in reorder:
        closest_ref_index = ref_indices[indices[query_index]]
        closest_query_index = query_indices[query_index]

        dp = np.dot(query_mesh.vertex_normals[closest_query_index], ref_mesh.vertex_normals[closest_ref_index])

        if dp < -0.95:
            mean_pos = np.mean(np.array([ref_mesh.vertices[closest_ref_index, :], query_mesh.vertices[closest_query_index, :]]), axis=0)
            mean_normal = -1 * np.mean(query_mesh.vertex_normals[query_indices, :], axis=0)
            return mean_pos, mean_normal
    return None, None


def check_dir(location):
    """ Ensure that a specified directory exists

    Args:
      location (str): target directory

    """
    if not os.path.isdir(location):
        try:
            os.makedirs(location)
        except:
            pass


def configure_logger(filename=None, stream_level=None, file_level=None):
    """ Configures the base logger

    Args:
      filename (str): target filename is the log is to be written to file (Default value = None)
      stream_level (str): log level for the stream handler (Default value = None)
      file_level (str): log level for the file handler (Default value = None)

    """

    clean_logger()

    if stream_level is None:
        stream_level = "INFO"
    if file_level is None:
        file_level = "DEBUG"

    main_logger = logging.getLogger("pyvol")
    main_logger.setLevel("DEBUG")

    formatter = logging.Formatter("%(name)-12s:".ljust(15) + "\t%(levelname)-8s" + "\t%(message)s")

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    sh.setLevel(stream_level)
    main_logger.addHandler(sh)

    if filename is not None:
        check_dir(os.path.dirname(filename))
        fh = logging.FileHandler(filename)
        fh.setFormatter(formatter)
        fh.setLevel(file_level)
        main_logger.addHandler(fh)

def clean_logger():
    """ Removes current handlers from the main PyVOL logger so that new ones can be assigned

    """

    main_logger = logging.getLogger("pyvol")
    main_logger.handlers = []


def coordinates_for_resid(pdb_file, resid, chain=None, model=0, sidechain_only=True):
    """ Extract the 3D coordinates for all atoms in a specified residue from a pdb file

    Args:
      pdb_file (str): filename of the specified pdb file
      resid (int): residue number
      chain (str): chain identifier (Default value = None)
      model (int): model identifier (Default value = 0)
      sidechain_only (bool): return only sidechain atom coordinates? (Default value = True)

    Returns:
      coordinates ([[float]]): 3xN array containing all atomic positions

    """
    logger.debug("Identifying coordinates for residue: {0}".format(resid))
    from Bio.PDB import PDBParser
    p = PDBParser(PERMISSIVE=1, QUIET=True)
    structure = p.get_structure("prot", pdb_file)

    if chain is not None:
        res = structure[model][chain][resid]
    else:
        res = [r for r in structure[model].get_residues() if r[1] == resid]
        if len(res) != 1:
            logger.error("Ambiguous or absent residue definition: {0} {2} {1}".format(pdb_file, resid, chain))
            return None
    return np.asarray([atom.get_coord() for atom in res.get_atoms() if atom.name not in ["C", "O", "CA", "N", "H", "HA"]])


def _pickle_method(m):
    """ Pickles a method; required for multiprocessing compatibility with python 2.x

    Args:
      m (method): method to be pickled

    Returns:
      pickled_method: pickled_method

    """
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


def run_cmd(options, in_directory=None):
    """ Run a program using the command line

    Args:
      options ([str]): list of command line options
      in_directory (str): directory in which to run the command (Default value = None)

    """
    if in_directory is not None:
        current_working_dir = os.getcwd()
        os.chdir(in_directory)

    opt_strs = [str(opt) for opt in options]

    try:
        subprocess.check_output(opt_strs, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        logger.error("Process Failed: {0}".format(" ".join(opt_strs)))
        raise

    logger.debug("Shell command: {0}".format(" ".join(opt_strs)))
    if in_directory is not None:
        os.chdir(current_working_dir)


def surface_multiprocessing(args):
    """ A single surface calculation designed to be run in parallel

    Args:
      args: a tuple containing:
        spheres (Spheres): a Spheres object containing all surface producing objects
        probe_radius (float): radius to use for probe calculations
        kwargs (dict): all remaining arguments accepted by the surface calculation algorithm

    Returns:
      surface (Spheres): the input Spheres object but with calculated surface parameters

    """
    spheres, probe_radius, kwargs = args
    return spheres.calculate_surface(probe_radius=probe_radius, **kwargs)


def sphere_multiprocessing(spheres, radii, workers=None, **kwargs):
    """ A wrapper function to calculate multiple surfaces using multiprocessing

    Args:
      spheres (Spheres): input Spheres object
      radii ([float]): list of radii at which surfaces will be calculated
      workers (int): number of workers (Default value = None)
      kwargs (dict): all remaining arguments accepted by surface calculation that are constant across parallel calculations

    Returns:
      surfaces ([Spheres]): a list of Spheres object each with its surface calculated

    """
    if workers is None:
        workers = multiprocessing.cpu_count()
    logger.debug("Splitting surface calculation at {0} radii across {1} workers".format(len(radii), workers))

    pool = multiprocessing.Pool(processes=workers)
    results = pool.map(surface_multiprocessing, [(spheres, probe_radius, kwargs) for probe_radius in radii])
    pool.close()
    return results


if sys.version_info < (3,):
    """ Necessary workaround to allow correct pickling of methods in Python 2.x

    """

    import copy_reg
    copy_reg.pickle(types.MethodType, _pickle_method)
