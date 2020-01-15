
from pyvol.spheres import Spheres

import logging
import numpy as np
import pandas as pd
from rdkit import Chem
import scipy

logger = logging.getLogger(__name__)


print("test")
if __name__ == "__main__":

    pose_file = '/home/rsmith/Dropbox (Schlessinger lab)/Schlessinger lab Team Folder/rsmith/papers/pyvol/sm/ftsa_trimmed_screening_poses.sdf'
    spheres_file = '/home/rsmith/Dropbox (Schlessinger lab)/Schlessinger lab Team Folder/rsmith/papers/pyvol/sm/n2m.B01_10_v3/205526_n2m.strada.B01_spa.csv'

    ms = [x for x in Chem.ForwardSDMolSupplier(pose_file) if x is not None]
    sp = np.loadtxt(spheres_file, delimiter=' ')
    sp = sp[sp[:, 4] > 0, :]

    subpocket_spheres = Spheres(xyzrg=sp)

    m1 = ms[0]
    conformer = m1.GetConformers()[0]
    pos = conformer.GetPositions()

    subpocket_spheres.propagate_groups_to_external(pos)

    # read in spheres (must contain only subpockets)
    # for each molecule in the pose file:
    #   read in the atomic coordinates
    #   find the closest sphere at propagate the group identities
    #   calculate the all atom and heavy atom only occupancies of each group and load into a dataframe
    #   highlight atoms by group and render
    #   normalize dataframe and output summary statistics
