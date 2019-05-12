
from Bio.PDB import PDBParser
import multiprocessing
import numpy as np
import os
import subprocess
import sys
import types

def check_dir(location):
    if not os.path.isdir(location):
        try:
            os.makedirs(location)
        except:
            pass


def coordinates_for_resid(pdb_file, resid, chain=None, model=0):
    p = PDBParser(PERMISSIVE=1, QUIET=True)
    structure = p.get_structure("prot", pdb_file)

    if chain is not None:
        res = structure[model][chain][residue]
    else:
        res = [r for r in structure[model].get_residues() if r[1] == residue]
        if len(res) != 1:
            print("Error: ambiguous or absent residue definition")
            return None
    return np.array([atom.get_coord() for atom in res.get_atoms()])


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)


def run_cmd(options, in_directory=None):
    if in_directory is not None:
        current_working_dir = os.getcwd()
        os.chdir(in_directory)

    opt_strs = [str(opt) for opt in options]
    # print(" ".join(opt_strs))

    # with open(os.devnull, 'w') as devnull:
    #     subprocess.call(opt_strs, stdout=devnull, stderr=devnull)
    # subprocess.call(opt_strs)
    try:
        subprocess.check_output(opt_strs, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Process Failed: {0}".format(" ".join(opt_strs)))

    if in_directory is not None:
        os.chdir(current_working_dir)


def surface_multiprocessing(args):
    spheres, probe_radius, kwargs = args
    return spheres.calculate_surface(probe_radius=probe_radius, **kwargs)
        

def sphere_multiprocessing(spheres, radii, workers=None, **kwargs):
    if workers is None:
        workers = multiprocessing.cpu_count()
    
    pool = multiprocessing.Pool(processes=workers)
    results = pool.map(surface_multiprocessing, [(spheres, probe_radius, kwargs) for probe_radius in radii])
    pool.close()
    return results


if sys.version_info < (3,):
    import copy_reg
    copy_reg.pickle(types.MethodType, _pickle_method)
