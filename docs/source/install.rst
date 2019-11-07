============
Installation
============

PyVOL consists of a back-end and a GUI. The back-end has been packaged into installers that contain all dependencies, but normal distribution is through PyPI and accessed through `pip`. PyVOL can consequently be installed into any python environment. For convenience, the PyVOL GUI contains an installer for easy installation into PyMOL 2.0+.

Installation into PyMOL from PyPI
---------------------------------

Download the :download:`basic GUI installer <https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip>` and then use the PyMOL plugin manager to install that file: :menuselection:`Plugins --> Plugin Manager --> Install New Plugin --> Install from local file -->` :guilabel:`Choose file...`

This installs the PyVOL GUI. Select :menuselection:`Plugins --> PyVOL --> Settings -->` :guilabel:`Install PyVOL from PyPI` to fetch PyVOL and any missing dependencies. For academic users and non-academic users with the Schrodinger incentive PyMOL distribution, installation is now complete. For all others :ref:`install:MSMS Installation`.

Installation into PyMOL Using a Packaged Installer
--------------------------------------------------

A larger installer with cached copies of PyVOL and its dependencies is also available. This option is useful if deploying PyVOL onto computers without internet access or if accessing a stable snapshot of a working build is necessary for some reason. :download:`full GUI installer <https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-full-installer.zip>` and then use the PyMOL plugin manager to install that file: :menuselection:`Plugins --> Plugin Manager --> Install New Plugin --> Install from local file -->` :guilabel:`Choose file...`

This installs the PyVOL GUI. Select :menuselection:`Plugins --> PyVOL --> Settings -->` :guilabel:`Install PyVOL from Cache` to install PyVOL and any missing dependencies from the installer. For academic users and non-academic users with the Schrodinger incentive PyMOL distribution, installation is now complete. For all others :ref:`install:MSMS Installation`.

Manual Installation
-------------------

PyVOL minimally requires `biopython`, `MSMS`, `numpy`, `pandas`, `scipy`, `scikit-learn`, `trimesh`, and `msms` in order to run. PyVOL is available for manual installation from `github <https://github.com/schlessingerlab/pyvol>`_ or through `PyPI <https://pypi.org/project/bio-pyvol/>`_. Most conveniently:

.. code-block:: bash

   pip install bio-pyvol

Again, for academic users and non-academic users with the Schrodinger incentive PyMOL distribution, installation is now complete. For all others, see manual :ref:`install:MSMS Installation`.

.. note::
  When using command-line installation commands, make sure to use the right python environment. By default, pip will use the system python, but PyMOL often includes its own python environment. To check which python environment to use, run `import sys; print(sys.executable)` on the PyMOL prompt. If that is anything besides the system default python, use `<PyMOL python executable> -m pip install bio-pyvol` to install PyVOL into the PyMOL-accessible environment.

MSMS Installation
-----------------

MSMS is provided with PyVOL for ease of use for academic users. It alternatively can be installed on MacOS and Linux using the bioconda channel:

.. code-block:: bash

   conda install -c bioconda msms

Otherwise MSMS must be installed manually by downloading it from `MGLTools <http://mgltools.scripps.edu/packages/MSMS/>`_ and adding it to the path.

Updating
--------

PyVOL can be updated through the PyMOL GUI simply by navigating :menuselection:`PyVOL --> Settings -->` :guilabel:`Check for Updates`. This queries the PyPI server to detect if an update is available. If an update is available for download, the same button becomes :guilabel:`Update PyVOL` and will update the back-end. The new version of the PyVOL back-end will notify you if it expects an updated GUI. If the GUI also needs to be updated, uninstall the `pyvol_gui` using :menuselection:`Plugins --> Plugin Manager --> Installed Plugins --> pyvol_gui x.x.x -->` :guilabel:`Uninstall`. Restart PyMOL, download the updated GUI from :download:`github <https://github.com/schlessingerlab/pyvol/blob/master/installers/pyvol-installer.zip>`, and install the updated GUI as described above.

Alternatively, PyVOL can be manually updated via the command line:

.. code-block:: bash

   pip update bio-pyvol

Uninstalling
------------

PyVOL can be uninstalled through its GUI by navigating :menuselection:`PyVOL --> Settings -->` :guilabel:`Uninstall PyVOL`. This uninstalls the back-end. Then use the plugin manager to uninstall the `pyvol_plugin`.

Again, PyVOL can also be uninstalled via the command line:

.. code-block:: bash

   pip uninstall bio-pyvol
