Module pyvol.identify
=====================

Functions
---------

    
`pocket(prot_file, mode='largest', lig_file=None, coordinate=None, resid=None, residue_coordinates=None, min_rad=1.4, max_rad=3.4, lig_excl_rad=None, lig_incl_rad=None, subdivide=False, minimum_volume=200, min_subpocket_rad=1.7, min_subpocket_surf_rad=1.0, max_clusters=None, prefix=None, output_dir=None, constrain_inputs=False)`
:   Calculates the SES for a binding pocket
    
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

    
`subpockets(bounding_spheres, ref_spheres, min_rad, max_rad, min_subpocket_rad=1.7, min_subpocket_surf_rad=1.0, max_subpocket_rad=None, sampling=0.1, inclusion_radius_buffer=1.0, min_cluster_size=50, max_clusters=None, prefix=None)`
:   Args:
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

    
`write_report(all_pockets, output_dir, prefix)`
:   Write a brief report of calculated volumes to file
    
    Args:
      all_pockets ([Spherese]): a list of Spheres objects each of which contains the complete information about a distinct pocket or subpocket
      output_dir (str): output directory, relative or absolute
      prefix (str): identifying prefix for output files