Module pyvol.utilities
======================

Functions
---------

    
`check_dir(location)`
:   Ensure that a specified directory exists
    
    Args:
      location (str): target directory

    
`coordinates_for_resid(pdb_file, resid, chain=None, model=0)`
:   Extract the 3D coordinates for all atoms in a specified residue from a pdb file
    
    Args:
      pdb_file (str): filename of the specified pdb file
      resid (int): residue number
      chain (str): chain identifier (Default value = None)
      model (int): model identifier (Default value = 0)
    
    Returns:
      coordinates ([[float]]): 3xN array containing all atomic positions

    
`run_cmd(options, in_directory=None)`
:   Run a program using the command line
    
    Args:
      options ([str]): list of command line options
      in_directory (str): directory in which to run the command (Default value = None)

    
`sphere_multiprocessing(spheres, radii, workers=None, **kwargs)`
:   A wrapper function to calculate multiple surfaces using multiprocessing
    
    Args:
      spheres (Spheres): input Spheres object
      radii ([float]): list of radii at which surfaces will be calculated
      workers (int): number of workers (Default value = None)
      **kwargs (dict): all remaining arguments accepted by surface calculation that are constant across parallel calculations
    
    Returns:
      surfaces ([Spheres]): a list of Spheres object each with its surface calculated

    
`surface_multiprocessing(args)`
:   A single surface calculation designed to be run in parallel
    
    Args:
      args: a tuple containing:
        spheres (Spheres): a Spheres object containing all surface producing objects
        probe_radius (float): radius to use for probe calculations
        kwargs (dict): all remaining arguments accepted by the surface calculation algorithm
    
    Returns:
      surface (Spheres): the input Spheres object but with calculated surface parameters