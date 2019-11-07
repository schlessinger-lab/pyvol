==========================
Output and Display Options
==========================

By default, PyVOL simply outputs a log containing volumes and, when invoked through PyMOL, displays pocket boundaries as semi-translucent surfaces. This behavior can be extensively customized.

.. figure:: _static/display_parameters_gui.png
  :align: center

  GUI section controlling file output and PyMOL visualization of new results

File Output Options
-------------------

The output name for all computed PyMOL objects and the base filename for any output files can be specified using the `Display Prefix` (command-line `prefix`) option. A prefix is otherwise derived from the input protein selection string.

.. code-block:: python

   pocket <protein_selection>, prefix=<output_prefix>

PyVOL can also write the input and output files to a directory specified with `Output Dir` (command-line `output_dir`). In this case it writes out the input protein and ligand structures, a csv report of all calcuated volumes, and paired csv/stl files containing tangent sphere collections and 3D triangulated mesh files respectively. Relative and absolute paths both work. However, in many cases referencing the home directory with ~ will not access the user's home directory. STL files can be read by almost all 3D file viewers.

.. code-block:: python

   pocket <protein_selection>, output_dir=<output_dir>

Display Options
---------------

Calculated surfaces can be visualized in three different ways by setting the `Display Mode` (command-line `display_mode`) parameter. The following three commands set the output as a solid surface with transparency, a wireframe mesh, and a collection of spheres. Color is set with the `Color` (command-line `color`) parameter that accepts any PyMOL color string. Transparency (when applicable) is set with the `Alpha` (command-line `alpha`) parameter that is a float [0.0, 1.0] that is equal to (1 - transparency).

.. code-block:: python

   pocket protein_selection, display_mode=solid, alpha=0.85, color=skyblue
   pocket protein_selection, display_mode=mesh, color=red
   pocket protein_selection, display_mode=spheres, color=firebrick

The presets should generally be sufficient, but custom colors can be chosen using the commands given on the PyMOL wiki. When creating multiple surfaces at the same time, PyVOL generates a palette and assigns each surface a different color. This can distinguish an arbitrary number of surfaces. The palette is currently not able to be changed from the default. If specific colors are needed for specific surfaces, the generated surfaces can be read back in
