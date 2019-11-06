
import logging
import multiprocessing
import numpy as np
import os
import subprocess
import sys
import types

logger = logging.getLogger(__name__)

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


def coordinates_for_resid(pdb_file, resid, chain=None, model=0):
    """ Extract the 3D coordinates for all atoms in a specified residue from a pdb file

    Args:
      pdb_file (str): filename of the specified pdb file
      resid (int): residue number
      chain (str): chain identifier (Default value = None)
      model (int): model identifier (Default value = 0)

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
    return np.array([atom.get_coord() for atom in res.get_atoms()])


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

    logger.debug("Ran command: {0}".format(" ".join(opt_strs)))
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
    import copy_reg
    copy_reg.pickle(types.MethodType, _pickle_method)
