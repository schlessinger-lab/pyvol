
============
Introduction
============

.. marker-start-readme

Overview
--------

PyVOL is a python library packaged into a `PyMOL <https://pymol.org/2/>`_ GUI for identifying protein binding pockets, partitioning them into sub-pockets, and calculating their volumes. PyVOL can be run as a PyMOL plugin through its GUI or the PyMOL prompt, as an imported python library, or as a command-line program. Visualization of results is exclusively supported through PyMOL though exported surfaces are compatible with standard 3D geometry visualization programs.

Quick Installation into PyMOL
-----------------------------

PyVOL can be installed into any python environment, but installing directly into PyMOL 2.0+ is easiest. Download the :download:`basic GUI installer <https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip>` and then use the PyMOL plugin manager to install that file: :menuselection:`Plugins --> Plugin Manager --> Install New Plugin --> Install from local file -->` :guilabel:`Choose file...`

This installs the PyVOL GUI. Select :menuselection:`Plugins --> PyVOL --> Settings -->` :guilabel:`Install PyVOL from PyPI` to fetch PyVOL and any missing dependencies. For academic users and non-academic users with the Schrodinger incentive PyMOL distribution, installation is now complete. For all others :ref:`install:MSMS Installation`.

Example Basic Run
-----------------

A simple calculation using the PyMOL prompt is to load a protein of interest and then run the `pocket` command. This is an example for the Sorafenib-bound structure of BRAF:

.. code-block:: python

  fetch '1UWH'
  pocket "1UWH and chain B"
