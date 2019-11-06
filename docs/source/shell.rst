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

Notes on Output
---------------

Currently, PyVOL only reports standard log output to stdout when run this way. So if an output directory is not provided, there is no easy way to retrieve the results.
