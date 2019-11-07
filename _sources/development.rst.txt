===========
Development
===========

Package Design
--------------

The main PyVOL algorithm is run from identify.py. There are two interfaces to this module which prepare user supplied inputs: `pyvol/pymol_interface.py` and the commandline entry point in `pyvol/__main__.py`. The PyMOL interface can be accessed directly through the PyMOL prompt or run using the included GUI. The command line entry point is evoked using a configuration file. The main entry point for accessing with the API is through `pyvol/identify.py`.

Algorithm Design
----------------

The primary algorithmic logic is supplied in `identify.py` which acts as the only interface between the user-facing modules and the computational back-end.

The Spheres class holds all of the geometric information about proteins and pockets. It represents any object as a collection of spheres by holding their coordinates, radii, and cluster identifications in a 5D numpy array. Surface triangulation using MSMS and many other convenience functions are included in the class itself. The methods contained in the separate `cluster.py` would largely work as methods in the Spheres class but have been separated due to that class becoming too large and the specificity of those methods to subpocket partitioning.

GUI Design
----------

The GUI was developed using Qt Designer and run using PyQT5. PyQT does not run in earlier PyMOL distributions.

Version Incrementation
----------------------

PyVOL uses a standard incrementation scheme. The version of the back-end must be updated in `setup.py`, `pyvol/__init__.py`, and `docs/source/conf.py`. The GUI version is set in `pyvolgui/__init__.py`, and the the version of the GUI that the back-end expects is set again in `pyvol/__init__.py`.

Distribution
------------

The code is hosted on github by the Schlessinger Lab. The PyVOL backend is distributed through PyPI. This process of uploading to PyPI is automated in the `dev/build.sh` script. Installers are packaged using the `dev/package_plugins.sh` script. Documentation is generated and pushed to the github-hosted documentation website with the `dev/document.sh` script. All three are combined in the `dev/rebuild.sh` script. The plugin will be available both from the github page and through the official PyMOL wiki.

Documentation
-------------

Documentation is largely in the google style but being switched to sphinx style. Module documentation is collated using `sphinx-apidoc`. The documentation website is built using the `sphinx-rtd-theme` and maintained on the gh-pages branch of PyVOL. The `pyvol_manual.pdf` is generated using sphinx's evocation of pdfTeX. PyPI can apparently not parse rst files, so the README.rst is converted to a md file using pandoc just prior to deployment.
