Module pyvol.spheres
====================

Classes
-------

`Spheres(xyz=None, r=None, xyzr=None, xyzrg=None, g=None, pdb=None, bv=None, mesh=None, name=None, spheres_file=None)`
:   A Spheres object contains a list of xyz centers with r radii and g groups. It can be defined using xyzrg, xyzr (and optionally g), xyz (and optionally r or g), a pdb file (and optionally r or g), or a list of vertices with normals bounded by the spheres (requires r and optionally includes g)
    
    Args:
      xyz (float nx3): Array containing centers (Default value = None)
      r (float nx1): Array containing radii (Default value = None)
      xyzr (float nx4): Array containing centers and radii (Default value = None)
      xyzrg (float nx5): Array containing centers, radii, and groups (Default value = None)
      g (float nx1): Array containing groups (Default value = None)
      pdb (str): filename of a pdb to be processed into spheres (Default value = None)
      bv (float nx6): Array containing vertices and normals (Default value = None)
      mesh (Trimesh): mesh object describing the surface (Default value = None)
      name (str): descriptive identifier (Default value = None)
      spheres_file (str): filename of a Spheres file to be read from disk (Default value = None)

    ### Instance variables

    `g`
    :   Retrieve the group indices

    `r`
    :   Retrieve the radii

    `xyz`
    :   Retrieve the coordinates

    `xyzr`
    :   Retrieve coordinates and radii

    `xyzrg`
    :   Retrieve the coordinates, radii, and group ids

    ### Methods

    `calculate_surface(self, probe_radius=1.4, cavity_atom=None, coordinate=None, all_components=False, exclusionary_radius=2.5, largest_only=False, noh=True, minimum_volume=200)`
    :   Calculate the SAS for a given probe radius
        
        Args:
          probe_radius (float): radius for surface calculations (Default value = 1.4)
          cavity_atom (int): id of a single atom which lies on the surface of the interior cavity of interest (Default value = None)
          coordinate ([float]): 3D coordinate to identify a cavity atom (Default value = None)
          all_components (bool): return all pockets? (Default value = False)
          exclusionary_radius (float): maximum permissibile distance to the closest identified surface element from the supplied coordinate (Default value = 2.5)
          largest_only (bool): return only the largest pocket? (Default value = False)
          noh (bool): remove waters before surface calculation? (Default value = True)
          minimum_volume (int): minimum volume of pockets returned when using 'all_components' (Default value = 200)

    `copy(self)`
    :

    `identify_nonextraneous(self, ref_spheres, radius)`
    :   Returns all spheres less than radius away from any center in ref_spheres using cKDTree search built on the non-reference set
        
        Args:
          ref_spheres (Spheres): object that defines the pocket of interest
          radius (float): maximum distance to sphere centers to be considered nonextraneous
        
        Returns:
          nonextraneous (Spheres): a filtered Spheres object

    `nearest(self, coordinate, max_radius=None)`
    :   Returns the index of the sphere closest to a coordinate; if max_radius is specified, the sphere returned must have a radius <= max_radius
        
        Args:
          coordinate (float nx3): 3D input coordinate
          max_radius (float): maximum permissibile distance to the nearest sphere (Default value = None)
        
        Returns:
          nearest_index: index of the closest sphere

    `nearest_coord_to_external(self, coordinates)`
    :   Returns the coordinate of the sphere closest to the supplied coordinates
        
        Args:
          coordinates (float nx3): set of coordinates
        
        Returns:
          coordinate (float 1x3): coordinate of internal sphere closest to the supplied coordinates

    `remove_duplicates(self, eps=0.01)`
    :   Remove duplicate spheres by identifying centers closer together than eps using DBSCAN
        
        Args:
          eps (float): DBSCAN input parameter (Default value = 0.01)

    `remove_groups(self, groups)`
    :   Remove all spheres with specified group affiliations
        
        Args:
          groups ([float]): list of groups to remove

    `remove_ungrouped(self)`
    :   Remove all spheres that did not adequately cluster with the remainder of the set

    `write(self, filename, contents='xyzrg', output_mesh=True)`
    :   Writes the contents of _xyzrg to a space delimited file
        
        Args:
          filename (str): filename to write the report and mesh if indicated
          contents (str): string describing which columns to write to file (Default value = "xyzrg")
          output_mesh (bool): write mesh to file? (Default value = True)