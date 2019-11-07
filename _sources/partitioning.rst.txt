====================
Partitioning Options
====================

PyVOL can deterministically divide a binding pocket into subpockets. This can be run on the output of any surface determination that results in a single returned surface. PyVOL currently calculates *de novo* complete binding pocket surfaces prior to partitioning because determination of the overall pocket is computationally trivial relative to subdivision.

.. figure:: _static/partitioning_parameters_gui.png
  :align: center

  GUI section controlling user binding pocket partition into subpockets

Enabling Subpocket Partitioning
-------------------------------

Subpocket partitioning is enabled in the GUI by selecting the `Subdivide` checkbox (command-line `subdivide`).

.. code-block:: python

   pocket <protein_selection>, subdivide=True

Limiting the Number of Subpockets
---------------------------------

Parameters controlling the number of sub-pockets identified generally perform well using defaults; however, they can be easily adjusted as needed. The two most important parameters are the `Maximum Sub-pockets` (command-line `max_clusters`) and the `Minimum Internal Radius` (command-line `min_subpocket_rad`). PyVOL clusters volume into the maximum number regions that make physical sense according to its hierarchical clustering algorithm. This means that there is a maximum number of clusters that is determined by the `Minimum Internal Radius` (the smallest sphere used to identify new regions) and the radial sampling frequency. Through its PyMOL interface, PyVOL currently fixes the radial sampling frequency at 10 A^-1. Larger values of the `Minimum Internal Radius` prohibit unique identification of smaller regions. The other parameter, `Maximum Sub-pockets`, sets the maximum number of clusters calculated. If the number of clusters originally determined is greater than the supplied maximum, clusters are iteratively merged using a metric that is related to the edge-weighted surface area between adjacent clusters.

.. code-block:: python

   pocket <protein_selection>, subdivide=True, min_subpocket_rad=<1.7>, max_clusters=<10>

Smoothness of the Subpocket Surfaces
------------------------------------

The size of the probe used to calculate surface accesibility of subpockets can be set with the `Minimum Surface Radius` (command-line `min_subpocket_surf_rad`) in the Partitioning Parameters section of the GUI. Calculation stability is less sensitive to the value of this parameter than the overall `Minimum Radius`. In practice, it should be set to a value slightly smaller than the overall `Minimum Radius` but not aphysically small. Unless changing the `Minimum Radius` used for overall calculations, the default value should be left unchanged.

.. code-block:: python

   pocket <protein_selection>, subdivide=True, min_subpocket_surf_rad=<1.2>
