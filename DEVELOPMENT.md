# PyVOL Development

## Package Design
The main PyVOL algorithm is run from identify.py. There are two interfaces to this module which prepare user supplied inputs: `pyvol/pymol_interface.py` and the commandline entry point in `pyvol/__main__.py`. The PyMOL interface can be accessed directly through the PyMOL prompt or run using the included GUI. The commandline entry point is evoked using a configuration file.

## Algorithm Design
The primary algorithmic logic is supplied in `identify.py` which acts as the only interface between the user-facing modules and the computational backend.

The Spheres class holds all of the geometric information about proteins and pockets. It represents any object as a collection of spheres by holding their coordinates, radii, and cluster identifications in a 5D numpy array. Surface triangulation using MSMS and many other convenience functions are included in the class itself. The methods contained in the separate `cluster.py` would largely work as methods in the Spheres class but have been separated due to that class becoming too large and the specificity of those methods to subpocket partitioning.

## GUI Design
The GUI is developed using Qt Designer and run using PyQT5.

## Version Incrementation
PyVOL uses a standard incrementation scheme. The version of the backend must be updated in both `setup.py` and `pyvol/__init__.py`. The GUI version is set in `pyvol_plugin/__init__.py`, and the the version of the GUI that the backend expects is set again in `pyvol/__init__.py`.

## Distribution
The code is hosted on github by the Schlessinger Lab. The PyVOL backend is distributed through PyPI. This process of uploading to PyPI is automated in the deploy.sh script. The plugin will be available both from the github page and through the official PyMOL wiki.
