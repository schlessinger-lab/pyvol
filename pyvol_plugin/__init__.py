

def __init_plugin__(app=None):
    try:
        from pymol import cmd
        from pyvol import pymol_interface
        cmd.extend('pocket', pymol_interface.pocket)
        cmd.extend('load_spheres', pymol_interface.load_spheres)
    except:
        pass
    finally:
        from pymol.plugins import addmenuitemqt
        addmenuitemqt('PyVOL Settings', settings_window)
        


def settings_window():
    import os
    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi

    dialog = QtWidgets.QDialog()
    uifile = os.path.join(os.path.dirname(__file__), 'settingswidget.ui')
    form = loadUi(uifile, dialog)

    def install_pyvol(form):
        import subprocess
        import sys

        subprocess.call([sys.executable, "-m", "pip", "install", "bio-pyvol"])
        if os.name in ['posix']:
            conda_path = os.path.join(os.path.dirname(sys.executable), "conda")
            if not os.path.isfile(conda_path):
                conda_path = "conda"
            subprocess.call([conda_path, "install", "-y", "-c", "bioconda", "msms"])

        from pymol import cmd
        from pyvol import pymol_interface
        cmd.extend('pocket', pymol_interface.pocket)
        refresh_status(form)

    def update_pyvol(form):
        import subprocess
        import sys

        subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "bio-pyvol"])
        refresh_status(form)

    def refresh_status(form):
        try:
            import pyvol
            pyvol_version = pyvol.__version__
        except:
            pyvol_version = "not found"
        
        try:
            import Bio
            biopython_version = Bio.__version__
        except:
            biopython_version = "not found"

        try:
            import numpy as np
            numpy_version = np.__version__
        except:            
            numpy_version = "not found"

        try:
            import pandas as pd
            pandas_version = pd.__version__
        except:
            pandas_version = "not found"

        try:
            import scipy
            scipy_version = scipy.__version__
        except:
            scipy_version = "not found"

        try:
            import sklearn
            sklearn_version = sklearn.__version__
        except:
            sklearn_version = "not found"

        try:
            import trimesh
            trimesh_version = trimesh.__version__
        except:
            trimesh_version = "not found"

        form.label.setText(("Current installation status:\n"
                            "  pyvol: {0}\n"
                            "  biopython: {1}\n"
                            "  numpy: {2}\n"
                            "  pandas: {3}\n"
                            "  scipy: {4}\n"
                            "  sklearn: {5}\n"
                            "  trimesh: {6}\n\n"
                            "Please be patient when installing or updating--the PyPI and conda servers can sometimes take a few minutes."
        ).format(pyvol_version, biopython_version, numpy_version, pandas_version, scipy_version, sklearn_version, trimesh_version))

        if pyvol_version == "not found":
            form.button_install.setText("Install PyVOL")
            form.button_install.clicked.connect(lambda: install_pyvol(form))
        else:
            form.button_install.setText("Update PyVOL")
            form.button_install.clicked.connect(lambda: update_pyvol(form))
        form.button_close.clicked.connect(dialog.close)

    refresh_status(form)
    dialog.show()
