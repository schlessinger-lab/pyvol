============
Installation
============

PyVOL has been packaged into installers that contain all dependencies, but normal distribution is through PyPI and accessed through `pip`. PyVOL can consequently be installed into any python environment. For convenience, the PyMOL GUI contains an installer for easy installation into PyMOL 2.0+.

Installation into PyMOL from PyPI
---------------------------------
Download the `basic installer zip file <https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip>`_ and then use the PyMOL plugin manager to install that file.

.. code-block:: bash

  https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip

This installs the PyVOL GUI. Select `PyVOL` under the plugins menu, and then select `Install from PyPI` under the settings tab to fetch PyVOL and any missing dependencies. For academic users and non-academic users with the Schrodinger incentive PyMOL distribution, installation is now complete. For all others, see manual installation of `msms` :ref:`below <MSMS_Installation>`.

Installation into PyMOL Using a Packaged Installer
--------------------------------------------------
This option is useful if deploying PyVOL onto computers without internet access. Download the `full installer zip file <https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-full-installer.zip>`_ and then use the PyMOL plugin manager to install that file.

.. code-block:: bash

  https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-full-installer.zip

This installs the PyVOL GUI. Select `PyVOL` under the plugins menu, and then select `Install from Local Cache` under the settings tab to install PyVOL and any missing dependencies from a cache contained within the installer itself. For academic users and non-academic users with the Schrodinger incentive PyMOL distribution, installation is now complete. For all others, see manual installation of `msms` :ref:`below <MSMS_Installation>`.

Manual Installation
-------------------
PyVOL minimally requires biopython, MSMS, numpy, pandas, scipy, scikit-learn, and trimesh in order to run. PyVOL is available for manual installation from `github <https://github.com/schlessingerlab/pyvol>`_ or through `PyPI <https://pypi.org/project/bio-pyvol/>`_. Most conveniently:

.. code-block:: bash

   pip install bio-pyvol

.. _MSMS_Installation:

MSMS Installation
-----------------
MSMS can be installed on MacOS and Linux using the bioconda channel:

.. code-block:: bash

   conda install -c bioconda msms

Otherwise MSMS must be installed manually by downloading it from `MGLTools <http://mgltools.scripps.edu/packages/MSMS/>`_ and adding it to the path. PyMOL distributions from Schrodinger have MSMS included; however, it must still be added to the path manually. The executable is located at:

.. code-block:: bash

   <pymol_root_dir>/pkgs/msms-2.6.1-2/bin/msms

Updating
--------
PyVOL can be updated via the command line:

.. code-block:: bash

   pip update bio-pyvol

If using the PyMOL GUI, the third tab has a button labeled ``Check for Updates`` that will query PyPI to detect whether an update is available. If one is available, that button changes to ``Update PyVOL`` and permits updating with a single click.

Uninstallation
--------------
PyVOL can be uninstalled via the command line:

.. code-block:: bash

   pip uninstall bio-pyvol

If using the PyMOL GUI, the third tab has a button labeled ``Uninstall PyVOL`` that will remove the PyVOL backend. Afterwards, selecting uninstall on the plugin within the PyMOL plugin manager will the GUI.
