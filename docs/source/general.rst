General Usage
=============

The GUI and shell command line prompts recapitulate the PyMOL prompt interface with few exceptions. General usage of PyVOL is shown here with specific examples and modifications for the other interfaces in the following pages. Programmatic invocation of internal functions is supported and covered through the module documentation.

Pocket Specification
--------------------

PyVOL by default recognizes the largest pocket and returns the volume and geometry for it. However, manual identification of the pocket of interest is generally preferable. This can be done through specification of a ligand, a residue, or a coordinate. If a specification is given, the mode is changed to specific by default.

Default Behavior (Largest Mode):
^^^^^^^^^^^^^^^^^

.. code-block:: python

   pocket protein_selection, mode=largest

Ligand Specification:
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   pocket protein_selection, mode=specific, ligand=ligand_selection
   pocket protein_selection, ligand=ligand_selection

Residue Specification:
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   pocket protein_selection, mode=specific, resid=A15
   pocket protein_selection, resid=A15
   pocket protein_selection, mode=specific, residue=residue_selection
   pocket protein_selection, residue=residue_selection

where the ``resid`` is written as :raw-html-m2r:`<Chain>`\ :raw-html-m2r:`<Residue number>`. If there is only one chain in the selection, the chain ID can be excluded.

Coordinate Specification:
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   pocket protein_selection, mode=specific, pocket_coordinate="5.0 10.0 15.0"
   pocket protein_selection, pocket_coordinate="5.0 10.0 15.0"

where the coordinate is provided as three floats separated by spaces and bounded by quotation marks.

Calculation of All Pockets
^^^^^^^^^^^^^^^^^^^^^^^^^^

Alternatively, PyVOL can return the surfaces and volumes for all pockets above a minimum volume that are identified. By default, this volume cutoff is set at 200 A^3.

.. code-block:: python

   pocket protein_selection, mode=all, minimum_volume=200

Extra Ligand Options
--------------------

When a ligand is provided, the atoms of the ligand can be used to identify both minimum and maximum extents of the calculated binding pocket.

Ligand Volume Inclusion
^^^^^^^^^^^^^^^^^^^^^^^

To include the volume of the ligand in the pocket volume (useful for when the ligand extends into bulk solvent), use the ``lig_incl_rad`` parameter:

.. code-block:: python

   pocket protein_selection, ligand=ligand_selection, lig_incl_rad=0.0

where the value of ``lig_incl_rad`` is added to the Van der Waals radii of each atom in the ligand selection when calculating the exterior surface of the protein.

Ligand-defined Maximum Volume
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The atoms of the ligand can also be used to define a maximum boundary to the calculated pocket by specifying the ``lig_excl_rad`` parameter:

.. code-block:: python

   pocket protein_selection, ligand=ligand_selection, lig_excl_rad=2.0

where the value of 11lig_excl_rad11 is added to the Van der Waals radii of each atom in the ligand selection when calculating the exterior surface of the protein.

Sub-pocket Partitioning
-----------------------

Sub-partitioning is enabled by setting the ``subdivide`` parameter to ``True``:

.. code-block:: python

   pocket protein_selection, subdivide=True

Parameters controlling the number of sub-pockets identified generally perform well using defaults; however, they can be easily adjusted as needed. The two most important parameters are the minimum radius of the largest sphere in each sub-pocket (this excludes small sub-pockets) and the maximum number of clusters:

.. code-block:: python

   pocket protein_selection, subdivide=True, min_subpocket_rad=1.7, max_clusters=10

If the number of clusters must be reduced, sub-pockets are merged on the basis of connectivity between the defining sets of tangent spheres. Practically, sub-pockets with a greater surface area boundary are merged first.

Display and Output Options
--------------------------

By default, PyVOL simply outputs a log containing volumes and, when invoked through PyMOL, displays pocket boundaries as semi-translucent surfaces. This behavior can be extensively customized.

The output name for all computed PyMOL objects and the base filename for any output files can be specified using the prefix option:

.. code-block:: python

   pocket protein_selection, prefix=favprot

PyVOL can also write the input and output files to a directory if given an output directory. In this case it writes out the input protein and ligand structures, a csv report of all calcuated volumes, and paired csv/obj files containing tangent sphere collections and 3D triangulated mesh files respectively.

.. code-block:: python

   pocket protein_selection, output_dir=chosen_out_dir

Calculated surfaces can be visualized in three different ways by setting the ``display_mode`` parameter. The following three commands set the output as a solid surface with transparency, a wireframe mesh, and a collection of spheres. Color is set with the ``color`` parameter and transparency (when applicable) with the ``alpha`` parameter:

.. code-block:: python

   pocket protein_selection, display_mode=solid, alpha=0.85, color=skyblue
   pocket protein_selection, display_mode=mesh, color=red
   pocket protein_selection, display_mode=spheres, color=firebrick

where ``alpha`` is [0, 1.0] and the color is any color defined within PyMOL. The presets should generally be sufficient, but custom colors can be chosen using the commands given on the PyMOL wiki.
