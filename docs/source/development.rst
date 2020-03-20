===========
Development
===========

Package Design
--------------

The main PyVOL algorithm is run from `identify.pocket`. Input option sanitization and logger configuration have been split into `identify.pocket_wrapper`. The pocket identification logic occurs within `identify.pocket` with almost all direct data manipulation handled by the class methods of `Spheres`. If enabled, subpocket clustering occurs in `identify.subpockets` with data manipulation occurring in `cluster`. Frequently used functions have been split into `utilities`. Configuration file reading and writing as well as input parameter checking is done in `configuration`.

The PyMOL interface is contained in `pymol_interface` though integration into the PyMOL environment is actually handled in `pyvol_gui.__init__`. Display and other PyMOL-specific functions are defined in `pymol_utilities`.

The two primary interfaces are via configuration file (invoked through the command line using the entry point in `__main__` that is created on installation) and via PyMOL. PyMOL is extended with all commands, and the GUI provides a limited interface to these functions. Programmatic invocation is also supported. If standard output options are reasonable, using the `identify.pocket_wrapper` entry point is better. For more customization, directly call `identify.pocket` after calling `configuration.clean_opts` on a dictionary containing all required options.

Algorithm Design
----------------

The primary algorithmic logic is supplied in `identify.py` which acts as the only interface between the user-facing modules and the computational back-end.

The Spheres class holds all of the geometric information about proteins and pockets. It represents any object as a collection of spheres by holding their coordinates, radii, and cluster identifications in a 5D numpy array. Surface triangulation using MSMS and many other convenience functions are included in the class itself. The methods contained in the separate `cluster.py` would largely work as methods in the Spheres class but have been separated due to that class becoming too large and the specificity of those methods to subpocket partitioning.

GUI Design
----------

The GUI was developed using Qt Designer and run using PyQT5. PyQT does not run in PyMOL 1.x distributions, so the GUI is only available in PyMOL 2.0+.

Version Incrementation
----------------------

PyVOL uses a standard incrementation scheme. The version of the back-end must be updated in `setup.py`, `pyvol/__init__.py`, and `docs/source/conf.py`. The GUI version is set in `pyvolgui/__init__.py`, and the the version of the GUI that the back-end expects is set again in `pyvol/__init__.py`. Experimental code is pushed with an alpha or beta designation (a or b before the final digit). GUI versions should only change when the GUI files are changed, but the version is intended to catch up to the backend version rather than the next available incrementation.

Distribution
------------

The code is hosted on github by the Schlessinger Lab. The PyVOL backend is distributed through PyPI. This process of uploading to PyPI is automated in the `dev/build.sh` script. Installers are packaged using the `dev/package_plugins.sh` script. Documentation is generated and pushed to the github-hosted documentation website with the `dev/document.sh` script. All three are combined in the `dev/rebuild.sh` script. The plugin will be available both from the github page and (eventually) through the official PyMOL wiki.

Documentation
-------------

Documentation is in the Sphinx/RTD style. Module documentation is collated using `sphinx-apidoc`. The documentation website is built using the `sphinx-rtd-theme` and maintained on the gh-pages branch of PyVOL. The `pyvol_manual.pdf` is generated using sphinx's evocation of pdfTeX. PyPI can apparently not parse rst files, so the README.rst is converted to a md file using pandoc just prior to deployment.

Testing
-------

Integration testing of the non-PyMOL components is performed using pytest out of `tests/test_pyvol.py`. These are invoked by running `python -m pytest` in the root pyvol directory. These tests have been run using pytest version 5.3.5. Installing `pytest-xdist` is recommended for efficiency's sake.
