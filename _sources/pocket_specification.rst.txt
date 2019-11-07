====================
Pocket Specification
====================

PyVOL runs in one of three modes (`largest`, `specific` or `all`). By default it runs in `largest` mode and returns only a single volume and geometry. However, manual identification of the pocket of interest is generally preferable. This can be done through specification of a ligand, a residue, or a coordinate. If any specification is given, the mode is changed to `specific` by default. The `specific` mode is the fastest by a small margin because it calculates the fewest surfaces. All parameters controlling pocket specification are contained in the corresponding GUI section.

.. figure:: _static/pocket_specification_gui.png
  :align: center

  GUI section controlling user specification of binding pockets

Largest Mode
------------

In the default `largest` mode, PyVOL determines all surfaces with inward-facing normals, calculates the volume of each, and selects the largest. The pocket selected with this mode can normally choose the pharmacologically interesting pocket in a protein. However, sometimes changes in the minimum or maximum radius can lead to the unexpected selection of an alternative pocket.

.. code-block:: python

  # Equivalent expressions
  pocket <protein_selection>
  pocket <protein_selection>, mode="largest"

All Mode
--------

When running in `all` mode, PyVOL determines all surfaces with inward-facing normals with volume over a minimum threshold defined by the `Minimum Volume` (command-line `minimum_volume`). This functions similarly to the `largest` mode except that 1) all surfaces are returned rather than just the largest, 2) if the largest surface has a volume less than `Minimum Volume`, no surface will be returned, and 3) subpocket partitioning cannot occur on the output from this mode. By default the `Minimum Volume` is set to 200 A^3. This is a heuristically determined threshold that is generally useful at distinguishing between artifacts and interesting pockets.

.. code-block:: python

  pocket <protein_selection>, mode="all", minimum_volume=<200>

Specific Mode
-------------

The final mode, the `specific` mode, is invoked through specification of a ligand, residue, or coordinate. PyVOL automatically switches to this mode if any specification is provided. There is an internal priority to which specification is used, but only a single option should be used.

Ligand Specification
^^^^^^^^^^^^^^^^^^^^

A ligand occupying the binding pocket of interest can be specified using the GUI's :menuselection:`Ligand: --> PyMOL Selection` field (command-line `ligand`). If the ligand selection is included in the protein selection, it is removed from the protein selection before the algorithm runs.

.. code-block:: python

  # Equivalent expressions
  pocket <protein_selection>, mode="specific", ligand=<ligand_selection>
  pocket <protein_selection>, ligand=<ligand_selection>

  # Trivial case in which a single organic small molecule is present in the protein selection
  pocket <protein_selection>, ligand="<protein_selection> and org"

Supplying a ligand opens up two additional options. `Inclusion Radius` (command-line `lig_incl_rad`) prevents the exterior surface of the protein (bulk solvent surface definition) from being defined within that distance from the ligand. In cases where a ligand extends somewhat into solvent and calculated volumes would otherwise be smaller than the volume of the known ligand, this can be used to produce a more useful surface. `Exclusion Radius` (command-line `lig_excl_rad`) limits the maximum scope of the identified surface as the locus of points that distance from the supplied ligand. Both of these options introduce a heuristic that alters reported results. They are most useful when standardizing volumes across a series of similar structures as they provide a mechanism to limit volume variability due to variation in bulk solvent boundary determination.

.. code-block:: python

  # Equivalent expressions
  pocket <protein_selection>, ligand=<ligand_selection>, lig_incl_rad=<3.5>, lig_excl_rad=<5.2>

Residue Specification
^^^^^^^^^^^^^^^^^^^^^

A residue can be supplied to localize a pocket. This can be done either with a PyMOL selection string or by specifying a residue ID. The `Residue PyMOL Selection` (command-line `residue`) takes an input PyMOL selection (which can be arbitrarily large or small but was designed to hold a single side chain). The `Reside Id` (command-line `resid`) accepts a string specifying an optional chain and a required residue index. For example, residue 35 of chain A would be specified by 'A35'. If only a single chain is present, the chain identifier can be omitted. PyVOL tries to identify the residue atom closest to an interior surface and uses that atom to specify the adjacent pocket of interest. Sometimes a residue is adjacent to multiple pockets. That makes it a poor, unpredictable choice for specification. If having trouble, specify a single atom as a PyMOL selection string.

.. code-block:: python

  pocket <protein_selection>, resid=<A15>
  pocket protein_selection, residue=<residue_selection>


Coordinate Specification
------------------------

The final method for specifying a pocket interest is through providing a `Coordinate` (command-line `pocket_coordinate`) that is within the pocket. PyVOL identifies the closest atom in the protein selection to the supplied coordinate and uses it to define the surface of the calculated pocket. The coordinate value is accepted as a string of three floats with spaces in between values ("x y z"). When running on the command-line, quotation marks are necessary given default argument processing.

.. code-block:: python

   pocket protein_selection, pocket_coordinate="5.0 10.0 15.0"
