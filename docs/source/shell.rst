===============
Shell Interface
===============

PyVOL can also be run from the system command line using bash or any standard shell. If installed using ``pip``, a ``pyvol`` entry point should be automatically installed and made available on the path. Otherwise, manual invocation of ``pyvol/__main__.py`` should work.

Running from the Shell
----------------------

From the command-line, PyVOL is run exclusively using a configuration file.

.. code-block:: bash

   python -m pyvol <input_parameters.cfg>

Template Configuration File Generation
--------------------------------------

A template configuration file with default values supplied can be generated using:

.. code-block:: bash

   python -m pyvol -t <output_template.cfg>

Re-running Previous Calculations
--------------------------------

Each PyVOL job writes the configuration file to recapitulate the exact run. After modifying a configuration file, unset the `prefix` and `output_dir` parameters in order to direct the output of the new run into a new folder.


.. note::

  When unsetting parameters in the configuration file, delete the entire line including the parameter name rather than just leaving the definition blank. For some parameters, leaving the definition blank angers the configuration file reader.
