

class MSMSError(Exception):
    """ Raised when MSMS fails to run correctly for any reason

    """
    pass
"""
    prot_file (str): filename for the input pdb file containing the peptidee
      mode (str): pocket identification mode (can be largest, all, or specific) (Default value = "largest")
      lig_file (str): filename for the input pdb file containing a ligand (Default value = None)
      coordinate ([float]): 3D coordinate used for pocket specification (Default value = None)
      resid (str): residue identifier for pocket specification (Default value = None)
      coordinates ([float]): 3D coordinate of an atom in a surrounding residue used for pocket specification (Default value = None)
      min_rad (float): radius for SES calculations (Default value = 1.4)
      max_rad (float): radius used to identify the outer, bulk solvent exposed surface (Default value = 3.4)
      lig_excl_rad (float): maximum distance from a provided ligand that can be included in calculated pockets (Default value = None)
      lig_incl_rad (float): minimum distance from a provided ligand that should be included in calculated pockets when solvent border is ambiguous (Default value = None)
      subdivide (bool): calculate subpockets? (Default value = False)
      min_volume (float): minimum volume of pockets returned when running in 'all' mode (Default value = 200)
      min_subpocket_rad (float): minimum radius that identifies distinct subpockets (Default value = 1.7)
      min_subpocket_surf_rad (float): radius used to calculate subpocket surfaces (Default value = 1.0)
      max_clusters (int): maximum number of clusters (Default value = None)
      min_cluster_size (int): minimum number of spheres in a proper cluster; used to eliminate insignificant subpockets (Default value = 50)
      inclusion_radius_buffer (float): buffer radius in excess of the nonextraneous radius from the identified pocket used to identify atoms pertinent to subpocket clustering (Default value = 1.0)
      radial_sampling (float): radial sampling used for subpocket clustering (Default value = 0.1)
      prefix (str): identifying string for output (Default value = None)
      output_dir (str): filename of the directory in which to place all output; can be absolute or relative (Default value = None)
      constrain_inputs (bool): restrict quantitative input parameters to tested values? (Default value = False)
"""
