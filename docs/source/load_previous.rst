========================
Loading Previous Results
========================

PyMOL cannot load custom CGO objects back into sessions correctly, so any PyMOL session containing PyVOL surfaces will have issues. PyMOL log files can be used but can take a while to run on slower computers.

.. figure:: _static/loading_parameters_gui.png
  :align: center

  GUI section that loads previous calculations into PyMOL for visualization

The PyMOL `load_pocket` command allows previous results to be read back in from file and displayed. A display prefix and display options (previously described :ref:`output:Display Options`) can be provided to overwrite configuration file values. `load_pocket` requires the directory holding the data from a previous calculation as its first parameter. This corresponds to the `output_dir` for new calculations and by default ends in '.pyvol'. If a data file is instead provided, PyVOL instead processes the encompassing directory.

.. code-block:: python

  load_pocket <directory>
