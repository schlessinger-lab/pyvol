
***********************************************************************
PyVOL: Protein Pocket Visualization, Segmentation, and Characterization
***********************************************************************

.. image:: https://img.shields.io/pypi/v/bio_pyvol.svg
  :target: https://pypi.python.org/pypi/bio_pyvol
  :alt: Pypi Version

.. image:: https://img.shields.io/pypi/l/bio_pyvol.svg
  :target: https://pypi.python.org/pypi/bio_pyvol/
  :alt: License

.. marker-start-introduction

Overview
--------

PyVOL is a python library packaged into a `PyMOL <https://pymol.org/2/>_` GUI for identifying protein binding pockets, partitioning them into sub-pockets, and calculating their volumes. PyVOL can be run as a PyMOL plugin through its GUI or the PyMOL prompt, as an imported python library, or as a command-line program. Visualization of results is exclusively supported through PyMOL though exported surfaces are compatible with standard 3D geometry visualization programs.

Quick Installation into PyMOL
-----------------------------

PyVOL can be installed into any python environment, but installing directly into PyMOL 2.0+ is easiest. Download the `installer zip file <https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip>_` and then use the plugin manager to install that file.

.. code-block:: bash

  https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip

This installs the PyVOL GUI. Select `PyVOL` under the plugins menu, and then select `Install from PyPI` under the settings tab. PyVOL currently requires the surface calculation program msms in order to run. Academic users can use the included binaries. Anyone with the Schrodinger incentive version can use the included binary. Anyone else must get msms from `MGLTools at Scripps <http://mgltools.scripps.edu/packages/MSMS/>_`.

Example Basic Run
-----------------

The simplest calculation just using the PyMOL prompt is to load a protein of interest and then run the `pocket` command. This is an example for the Sorafenib-bound structure of BRAF:

.. code-block:: python

   fetch 1UWH
   pocket "1UWH and chain B"

.. marker-end-introduction

More Examples & Documentation
-----------------------------
For more details on `how to run PyVOL`, `example calculations <https://schlessingerlab.github.io/pyvol/examples.html>_`, details on `installation <https://schlessingerlab.github.io/pyvol/installation.html>_`, and extensive `documentation <https://schlessingerlab.github.io/pyvol/pyvol.html>_`, look at the project documentation website:

.. code-block:: bash

  https://schlessingerlab.github.com/pyvol
