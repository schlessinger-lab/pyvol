
import logging
import pandas as pd
from rdkit import Chem

logger = logging.getLogger(__name__)


if __name__ == "__main__":

    pose_file = '/home/rsmith/Dropbox (Schlessinger lab)/Schlessinger lab Team Folder/rsmith/papers/pyvol/sm/ftsa_trimmed_screening_poses.sdf'
    spheres_file = '/home/rsmith/Dropbox (Schlessinger lab)/Schlessinger lab Team Folder/rsmith/papers/pyvol/sm/n2m.B01_10/'

    ms = [x for x in Chem.ForwardSDMolSupplier(pose_file) if x is not None]

    # read in spheres (must contain only subpockets)
    # for each molecule in the pose file:
    #   read in the atomic coordinates
    #   find the closest sphere at propagate the group identities
    #   calculate the all atom and heavy atom only occupancies of each group and load into a dataframe
    #   highlight atoms by group and render
    #   normalize dataframe and output summary statistics
