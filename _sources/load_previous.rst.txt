========================
Loading Previous Results
========================

PyMOL can not load custom CGO objects back into sessions correctly, so any PyMOL session containing PyVOL surfaces will have issues. PyMOL log files can be used but can take a while to run on slower computers. The `Load Pocket` (command-line `load_pocket`) command allows previous results to be read back in from file. In order to generate these input files, an `Output Dir` (command-line `output_dir`) must be set.

.. figure:: _static/loading_parameters_gui.png
  :align: center

  GUI section that loads previous calculations into PyMOL for visualization


Selecting Saved Results
-----------------------

PyVOL saves its output as a collection of two files that hold all of the information to recreate the original `Spheres` object in memory. These files consist of a csv holding `Spheres` data and a 3D file holding surface triangulation information. If a surface has not been computed for a `Spheres` object, the 3D file will not be written out. However, all modes accessible through the PyMOL command-line and GUI interfaces will write a 3D file. The 3D files by default are written in the `ascii STL` format (updated from the wavefront `obj` format in PyVOL 1.2.34 and GUI version 1.1.3). Either the 3D file or the csv can be provided to read in the collection of both.

.. code-block:: python

   load_pocket <3D or csv file>, name=<new PyMOL name>, display_mode=<"solid">, color=<"marine">, alpha=<0.5>

Display Options
---------------

These options in the GUI are identical to the display options when performing a *de novo* calculation. On the command-line, `name` is accepted in place of `prefix`. Please see :ref:`display:Display Options` for more information
