
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

.. marker-end-introduction

Examples & Documentation
------------------------
For more details on `how to run PyVOL`, `example calculations <https://schlessingerlab.github.io/pyvol/examples.html>`, details on `installation <https://schlessingerlab.github.io/pyvol/installation.html>`, and extensive `documentation <https://schlessingerlab.github.io/pyvol/pyvol.html>`, look at the project documentation website:

.. code-block:: bash

  https://schlessingerlab.github.com/pyvol


PyVOL is a python library packaged into a `PyMOL` GUI for identifying protein binding pockets, partitioning them into sub-pockets, and calculating their volumes. PyVOL can be run as a PyMOL plugin through its GUI or the PyMOL prompt, as an imported python library, or as a commandline program. Visualization of results is exclusively supported through PyMOL though exported surfaces are compatible with standard 3D geometry visualization programs.

.. _PyMOL: https://pymol.org/2/

Installation
============

PyVOL can be installed into any python environment; however, for most users direct installation into PyMOL will be easiest.

Installation into PyMOL
-----------------------

PyVOL is distributed as a GUI and a backend. Installation into PyMOL uses PyMOL's plugin manager to install the GUI and then the GUI to install the backend. The GUI is installed through the plugin manager through loading the `zipped GUI file <https://github.com/rhs2132/pyvol/blob/master/pyvolgui.zip>`_:

.. code-block:: bash

    https://github.com/rhs2132/pyvol/blob/master/pyvolgui.zip

This creates a new ``PyVOL`` menu entry under plugins. The third tab of the GUI allows installation of PyVOL from PyPI along with all available dependencies. For more information, especially on Windows, see the `installation page <https://schlessingerlab.github.io/pyvol/install.html>`_.

Running PyVOL
=============

Quick Start
-----------

From within PyMOL, the simplest binding pocket calculation is simply run at the PyMOL prompt with:

.. code-block:: python

   pocket protein_selection

The two parameters that most dramatically affect calculations are the maximum and minimum radii used to respectively define the exterior surface of the protein and the boundary of the binding pocket itself. In practice, the minimum radius does not need to be changed as its default (1.4) is broadly useful. The maximum radius does often need to be adjusted to find a suitable value using the max_rad parameter:

.. code-block:: python

   pocket protein_selection, min_rad=1.4, max_rad=3.4

Further Examples
----------------

For extensive explanations and documentations of the GUI and command line interfaces, see the `general usage page <https://schlessingerlab.github.io/pyvol/general.html>`_.

Module Documentation
====================
For full documentation of the code, see the `modules page <https://schlessingerlab.github.io/pyvol/modules.html>`_.
