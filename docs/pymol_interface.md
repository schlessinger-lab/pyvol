Module pyvol.pymol_interface
============================

Functions
---------

    
`load_pocket(spheres_file, name=None, display_mode='solid', color='marine', alpha=0.85)`
:   Args:
      spheres_file (str): filename
      name (str): internal display name (Default value = None)
      display_mode (str): display mode (Default value = "solid")
      color (str): PyMOL color string (Default value = 'marine')
      alpha (float): transparency value (Default value = 0.85)

    
`pocket(protein, mode=None, ligand=None, pocket_coordinate=None, residue=None, resid=None, prefix=None, min_rad=1.4, max_rad=3.4, lig_excl_rad=None, lig_incl_rad=None, display_mode='solid', color='marine', alpha=0.85, output_dir=None, subdivide=None, minimum_volume=200, min_subpocket_rad=1.7, min_subpocket_surf_rad=1.0, max_clusters=None, excl_org=False, constrain_inputs=True)`
:   Calculates the SAS for a binding pocket and displays it
    
    Args:
      protein (str): PyMOL selection string for the protein
      mode (str): pocket identification mode (can be largest, all, or specific) (Default value = None)
      ligand (str): PyMOL selection string for the ligand (Default value = None)
      pocket_coordinate ([float]): 3D coordinate used for pocket specification (Default value = None)
      residue (str): PyMOL residue selection string for pocket specification (Default value = None)
      resid (str): residue identifier for pocket specification (Default value = None)
      prefix (str): identifying string for output (Default value = None)
      min_rad (float): radius for SAS calculations (Default value = 1.4)
      max_rad (float): radius used to identify the outer, bulk solvent exposed surface (Default value = 3.4)
      lig_excl_rad (float): maximum distance from a provided ligand that can be included in calculated pockets (Default value = None)
      lig_incl_rad (float): minimum distance from a provided ligand that should be included in calculated pockets when solvent border is ambiguous (Default value = None)
      display_mode (str): display mode for calculated pockets (Default value = "solid")
      color (str): PyMOL color string (Default value = 'marine')
      alpha (float): transparency value (Default value = 0.85)
      output_dir (str): filename of the directory in which to place all output; can be absolute or relative (Default value = None)
      subdivide (bool): calculate subpockets? (Default value = None)
      minimum_volume (float): minimum volume of pockets returned when running in 'all' mode (Default value = 200)
      min_subpocket_rad (float): minimum radius that identifies distinct subpockets (Default value = 1.7)
      min_subpocket_surf_rad (float): radius used to calculate subpocket surfaces (Default value = 1.0)
      max_clusters (int): maximum number of clusters (Default value = None)
      excl_org (bool): exclude non-peptide atoms from the protein selection? (Default value = False)
      constrain_inputs (bool): constrain input quantitative values to tested ranges? (Default value = True)