
Installation
============

PyVOL distribution is hosted by PyPI and accessed through pip. PyVOL can consequently be installed into any python environment. For convenience, the PyMOL GUI contains an installer.

Detailed Installation into PyMOL
--------------------------------
PyVOL is distributed as a GUI and a backend. Installation into PyMOL uses PyMOL's plugin manager to install the GUI and then the GUI to install the backend. The GUI is installed through the plugin manager through loading the `zipped GUI file <https://github.com/rhs2132/pyvol/blob/master/pyvolgui.zip>` _:

.. code-block:: bash

    https://github.com/rhs2132/pyvol/blob/master/pyvolgui.zip

This creates a new ``PyVOL`` menu entry under plugins. The third tab of the GUI allows installation of PyVOL from PyPI along with all available dependencies. On Linux and MacOS, MSMS is automatically installed from the platform-limited bioconda channel. MSMS installation instructions are otherwise :ref:`below <MSMS_Installation>`.


Manual Installation
-------------------
PyVOL minimally requires biopython, MSMS, numpy, pandas, scipy, scikit-learn, and trimesh in order to run. PyVOL is available for manual installation from github or through PyPI. Most conveniently:

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
