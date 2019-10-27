Module pyvol.cluster
====================

Functions
---------

    
`cluster_between_r(spheres, ref_radius, target_radius)`
:   Cluster spheres from a target radius to a reference radius, modifying input data in situ
    
    Args:
      spheres (Spheres): complete set of input spheres
      ref_radius (float): radius from which cluster identities will be drawn
      target_radius (float): radius to which cluster identities will be propagated

    
`cluster_improperly_grouped(spheres, radius, min_cluster_size=1, max_clusters=None)`
:   Reassigns improperly clustered spheres to 'proper' clusters, modifying input data in situ
    
    Args:
      spheres (Spheres): complete set of input spheres
      radius (float): radius at which closest groups are identified
      min_cluster_size (int): minimum number of spheres in a 'proper' cluster (Default value = 1)
      max_clusters (int): maximum number of 'proper' clusters (Default value = None)

    
`cluster_within_r(spheres, radius, allow_new=True)`
:   Cluster spheres with the same radius using DBSCAN, modifying input data in situ
    
    Args:
      spheres (Spheres): complete set of input spheres
      radius (float): radius at which clustering is to occur
      allow_new (bool): permit new clusters? (Default value = True)

    
`extract_groups(spheres, surf_radius=None, prefix=None)`
:   Extracts spheres belonging to each cluster from the complete input set and optionally calculates bounded surfaces
    
    Args:
      spheres (Spheres): complete set of input spheres
      surf_radius: radius used to calculate bounding spheres for individual groups (Default value = None)
      prefix: prefix to identify new surfaces (Default value = None)
    
    Returns:
      group_list ([Spheres]): a list of Spheres objects each corresponding to a different cluster

    
`hierarchically_cluster_spheres(spheres, ordered_radii, min_new_radius=None, min_cluster_size=10, max_clusters=None)`
:   Cluster spheres by grouping spheres at large radius and propagating those assignments down to smaller radii
    
    Args:
      spheres (Spheres): complete set of input spheres
      ordered_radii ([float]): list of radii ordered from largest to smallest
      min_new_radius (float): smallest spheres to keep (Default value = None)
      min_cluster_size (int): minimum number of spheres in a cluster (Default value = 10)
      max_clusters (int): maximum number of clusters (Default value = None)

    
`identify_closest_grouped(spheres, group, radius)`
:   Identifies the closest 'properly' grouped cluster to a specified group
    
    Args:
      spheres (Spheres): complete set of input spheres
      group (float): group for which to identify the closest clusters
      radius (float): radius at which to perform the search
    
    Returns:
      group (float): passthrough of input group
      closest (float): id of the closest cluster
      magnitude (int): number of pairwise closest connections between the queried group and the closest identified cluster

    
`merge_sphere_list(s_list, r=None, g=None)`
:   Args:
      s_list ([Spheres]): list of input spheres
      r (float): radius value to assign to output Spheres (Default value = None)
      g (float): group value to assign to output Spheres (Default value = None)
    
    Returns:
      merged_spheres (Spheres): a single Spheres object containing the merged input lists

    
`reassign_group(spheres, source_group, target_group)`
:   Reassign a group in place
    
    Args:
      spheres (Spheres): complete set of input spheres
      source_group (float): group to change
      target_group (float): new group id

    
`reassign_groups_to_closest(spheres, group_list, radius, iterations=None, preserve_largest=False)`
:   Reassign a group to the closest group as identified by maximum linkage; operates in place
    
    Args:
      spheres (Spheres): complete set of input spheres
      group_list ([float]): list of group ids which are to be iteratively reassigned
      radius (float): radius at which searches are to take place
      iterations (int): number of times to attempt to reassign groups (Default value = None)
      preserve_largest: keep the group id of the group with more members? (Default value = False)

    
`remove_interior(spheres)`
:   Remove all spheres which are completely enclosed in larger spheres; operates in place
    
    Args:
      spheres (Spheres): complete set of input spheres

    
`remove_overlap(spheres, radii=None, spacing=0.1, iterations=20, tolerance=0.02)`
:   Remove overlap between groups; operates in place
    
    Args:
      spheres (Spheres): complete set of input spheres
      radii ([float]): radii at which to perform searches for overlap (Default value = None)
      spacing (float): binning radius (Default value = 0.1)
      iterations (int): number of times to attempt overlap removal (Default value = 20)
      tolerance (float): overlap tolerance (Default value = 0.02)