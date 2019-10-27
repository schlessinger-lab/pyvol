Module pyvol.pymol_utilities
============================

Functions
---------

    
`construct_palette(color_list=None, max_value=7, min_value=1)`
:   Construct a palette
    
    Args:
      color_list ([str]): list of PyMOL color strings (Default value = None)
      max_value (int): max palette index (Default value = 7)
      min_value (int): min palette index (Default value = 1)
    
    Returns:
      palette ([str]): list of color definitions

    
`display_pseudoatom_group(spheres, name, color='gray60', palette=None)`
:   Displays a collection of pseudoatoms
    
    Args:
      spheres (Spheres): Spheres object holding pocket geometry
      name (str): display name
      color (str): PyMOL color string (Default value = 'gray60')
      palette ([str]): palette (Default value = None)

    
`display_spheres_object(spheres, name, state=1, color='marine', alpha=0.7, mode='solid', palette=None)`
:   Loads a mesh object into a cgo list for display in PyMOL
    
    Args:
      spheres (Spheres): Spheres object containing all geometry
      name (str): display name
      state (int): model state (Default value = 1)
      color (str): PyMOL color string (Default value = 'marine')
      alpha (float): transparency value (Default value = 0.7)
      mode (str): display mode (Default value = "solid")
      palette ([str]): palette (Default value = None)

    
`mesh_to_solid_CGO(mesh, color='gray60', alpha=1.0)`
:   Creates a solid CGO object for a mesh for display in PyMOL
    
    Args:
      mesh (Trimesh): Trimesh mesh object
      color (str): PyMOL color string (Default value = 'gray60')
      alpha (float): transparency value (Default value = 1.0)
    
    Returns:
      cgobuffer (str): CGO buffer that contains the instruction to load a solid object

    
`mesh_to_wireframe_CGO(mesh, color='gray60', alpha=1.0)`
:   Creates a wireframe CGO object for a mesh for display in PyMOL
    
    Args:
      mesh (Trimesh): Trimesh mesh object
      color (str): PyMOL color string (Default value = 'gray60')
      alpha (float): transparency value (Default value = 1.0)
    
    Returns:
      cgobuffer (str): CGO buffer that contains the instruction to load a wireframe object