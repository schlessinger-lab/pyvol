
============
Introduction
============

.. marker-start-readme

Overview
--------

PyVOL is a python library packaged into a `PyMOL <https://pymol.org/2/>`_ GUI for identifying protein binding pockets, partitioning them into sub-pockets, and calculating their volumes. PyVOL can be run as a PyMOL plugin through its GUI or the PyMOL prompt, as an imported python library, or as a command-line program. Visualization of results is exclusively supported through PyMOL though exported surfaces are compatible with standard 3D geometry visualization programs.

Quick Installation into PyMOL
-----------------------------

PyVOL can be installed into any python environment, but installing directly into PyMOL 2.0+ is easiest. Download the `installer zip file <https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip>`_ and then use the plugin manager to install that file.

.. code-block:: bash

  https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip

This installs the PyVOL GUI. Select `PyVOL` under the plugins menu, and then select `Install from PyPI` under the settings tab to fetch PyVOL and any missing dependencies. For academic users and non-academic users with the Schrodinger incentive PyMOL distribution, installation is now complete. For all others, see `manual installation <https://schlessingerlab.github.io/pyvol/install.html>`_ of `msms`.

Example Basic Run
-----------------

The simplest calculation just using the PyMOL prompt is to load a protein of interest and then run the `pocket` command. This is an example for the Sorafenib-bound structure of BRAF:

.. code-block:: python

   fetch 1UWH
   pocket "1UWH and chain B"
