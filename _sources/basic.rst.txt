===========
Basic Usage
===========

The GUI and PyMOL prompt interfaces are all but identical. The shell interface is run using input configuration files and is best used to automate tasks first tested within PyMOL. Explanations for running PyVOL with the PyMOL GUI or prompt are covered first. Additional details covering shell invocation follow. Programmatic invocation of internal functions is supported and covered through the module documentation.

The next few section describe the parameters controlling Basic Usage, :ref:`pocket_specification:Pocket Specification`, :ref:`partitioning:Partitioning Options`, and :ref:`display:Output and Display Options` along with the corresponding GUI sections.

.. figure:: _static/basic_parameters_gui.png
  :align: center

  The Basic Parameters section of the PyVOL GUI

Protein Selection
-----------------

The `Protein Selection` (command-line `protein` required to be in the first position) is a PyMOL selection string that identifies all atoms that should be considered to occlude space. This can be any interpretable PyMOL selection. The `only include PyMOL 'poly'` checkbox (command-line `exclude_org`) is a convenience option that simply appends `'and poly'` to the given selection string to exclude water, solvents, and any other small molecule, non-peptide atoms. If a cofactor should be considered part of the binding site, it might make sense to group it in with the peptide for calculating the solvent accessible surface effectively present for the small molecule of interest.

.. code-block:: python

  pocket <protein selection>

Min and Max Radii
-----------------

The most important parameters (command-line `min_rad` and `max_rad`) controlling PyVOL pocket identification and boundary location are the minimum and maximum radii used for surface identification. The maximum radius determines the size of the probe used to identify regions accessible to bulk solvent. This parameter should be chosen to exclude any binding pockets of interest while not overly distorting the surface of the protein. Generally, values around 3.4 A are reasonable, but lower values can be provided to increase the stringency of pocket detection or higher values to reduce the stringency. The minimum radius controls two factors: The level of detail of the calculated binding pocket surfaces and the algorithmic lower limit to minimum internal radii of identified binding pockets. Lower minimum radii calculate the accessibility to smaller solvent molecules. This necessarily increases the number of nooks or crannies in the binding pocket surface that are calculated and can link adjacent pockets that can not accommodate even small organic molecules. Minimum radii as large as the smallest pharmacophore radius of potential ligands make sense for calculations, but the radius of water is default and normally best because it is what users expect when looking at solvent accessible surfaces.

.. code-block:: python

  pocket <protein selection>, max_rad=<3.4>, min_rad=<1.4>

Input Constraint
----------------

By default, input quantitative parameters are compared and constrained to test ranges. The `Constrain Inputs to Tested Ranges` (command-line `constrain_inputs`) toggles this feature. While edge cases are possible in which violating constraints is useful, in practice these constraints represent effective ranges. In particular, setting the minimum radius to absurdly low values will start fitting pockets in even intramolecular spaces and provide meaningless output if not a crash.

.. code-block:: python

  pocket <protein selection>, constrain_inputs=True

.. note::

  Be careful about saving `.pse` PyMOL sessions with PyVOL-produced surfaces. PyMOL does not currently use plugins to load unfamiliar CGO objects, so calculated surfaces will not load correctly from a saved PyMOL session. On the other hand, saved PyMOL `.pml` logs should recreate results. Surfaces can be loaded back into a session using the `Load Pocket` (command-line `load_pocket`) commands.
