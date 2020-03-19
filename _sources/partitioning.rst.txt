====================
Partitioning Options
====================

PyVOL can deterministically divide a binding pocket into subpockets. This can be run on the output of any surface determination that results in a single returned surface. PyVOL currently calculates *de novo* complete binding pocket surfaces prior to partitioning because determination of the overall pocket is computationally trivial relative to subdivision.

.. figure:: _static/partitioning_parameters_gui.png
  :align: center

  GUI section controlling user binding pocket partition into subpockets

Enabling Subpocket Partitioning
-------------------------------

Subpocket partitioning is enabled by setting the `subdivide` argument to `True`. In the GUI, this is done by selecting the `Subdivide` checkbox.

.. code-block:: python

  # arguments: subdivide
  pocket prot_file=<protein_pdb_filename>, subdivide=True
  pocket protein=<"PyMOL selection string">, subdivide=True

Controlling the Number of Subpockets
------------------------------------

Parameters controlling the number of sub-pockets identified generally perform well using defaults; however, they can be easily adjusted as needed. The two most important parameters are controlled with the `max_clusters` and `min_subpocket_rad` arguments. PyVOL clusters volume into the maximum number of regions that make physical sense according to its hierarchical clustering algorithm. This means that there is a maximum number of clusters that is determined by the `min_subpocket_rad` (the smallest sphere used to identify new regions). Larger values of the `min_subpocket_rad` can prohibit unique identification of smaller regions and can cause partitioning to fail altogether. Setting the maximum number of clusters simply sets an upper bound to the number of subpockets identified. If the number of clusters originally determined is greater than the supplied maximum, clusters are iteratively merged using a metric that is related to an edge-biased surface area between adjacent clusters.

.. code-block:: python

  # arguments: min_subpocket_rad, max_clusters
  pocket prot_file=<protein_pdb_filename>, subdivide=True, min_subpocket_rad=<1.7>, max_clusters=<10>
  pocket protein=<"PyMOL selection string">, subdivide=True, min_subpocket_rad=<1.7>, max_clusters=<10>

Other Partitioning Parameters
-----------------------------

The size of the probe used to calculate surface accesibility of subpockets can be set with the `min_subpocket_surf_rad`. Calculation stability is less sensitive to the value of this parameter than the overall minimum probe radius. In practice, it should be set to a value slightly smaller than the overall minimum radius but not less than 1.0 Å. Unless changing the minimum used for overall calculations, the default value should be left unchanged.

PyVOL currently defaults to performing radial sampling frequency at 0.1 inverse Å but this can be adjusted using the `radial_sampling` argument. Larger `radial_sampling` values should significantly improve calculation speed but at the cost of pocket resolution.

PyVOL isolates the pocket to be subdivided prior to running partitioning. The local environment of the pocket is isolated by identifying all atoms within a set distance of the surface calculated for the pocket of interest. This distance is set to the maximum radius used for bulk solvent surface identification plus a buffer. The magnitude of this buffer is by default 1 A and can be set using the `inclusion_radius_buffer` argument.

The maximum sampled internal radius of subpockets can be set with the `max_subpocket_rad` argument. Varying this parameter above ~2.7 Å is unlikely to alter results. The only practical scenario for setting this variable is when an unusually low maximum radius is used in determining bulk solvent surfaces. If internal pocket cross sections are larger than the external probe used, setting the `max_subpocket_rad` to a higher value can permit proper clustering. For the majority of users, this parameter should never be adjusted.

The minimum number of tangent surface spheres belonging to a subpocket can be set with the `min_cluster_size`. The purpose of this filter is to remove small, aphysical sphere groupings before clustering. In practice, this never needs to be adjusted.

.. code-block:: python

  # arguments: min_subpocket_surf_rad, radial_sampling, max_subpocket_rad, min_cluster_size
  pocket prot_file=<protein_pdb_filename>, subdivide=True, min_subpocket_rad=<1.7>, max_clusters=<10>, min_subpocket_surf_rad=<10>, radial_sampling=<0.1>, max_subpocket_rad=<3.4>, min_cluster_size=<50>
  pocket protein=<"PyMOL selection string">, subdivide=True, min_subpocket_rad=<1.7>, max_clusters=<10> min_subpocket_surf_rad=<10>, radial_sampling=<0.1>, max_subpocket_rad=<3.4>, min_cluster_size=<50>
