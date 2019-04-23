
from Bio.PDB import PDBParser
import numpy as np
import os
import subprocess

def check_dir(location):
    if not os.path.isdir(location):
        os.makedirs(location, exist_ok=True)

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


def coordinates_for_residue(pdb_file, residue, chain=None, model=0):
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
