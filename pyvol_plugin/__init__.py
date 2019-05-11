

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

        try:
            from pymol import cmd
            from pyvol import pymol_interface
            cmd.extend('pocket', pymol_interface.pocket)
            cmd.extend('load_spheres', pymol_interface.load_spheres)
        except:
            print("Installation still not complete")
        refresh_status(form)

    def update_pyvol(form):
        import subprocess
        import sys

        subprocess.call([sys.executable, "-m", "pip", "install", "--update", "bio-pyvol"])
        refresh_status(form)

    def refresh_status(form):
        import distutils.spawn

        def apply_color(string, color):
            return "<font color='{0}'>{1}</font>".format(color, string)
        
        try:
            import pyvol
            pyvol_version = pyvol.__version__
        except:
            pyvol_version = "not_found"

        update_available = False
        if pyvol_version != "not_found":
            pypi_pyvol_version = subprocess.call([sys.executable, "-m", "pip", "list", "|", "grep", "bio-pyvol"])
            installed_version, pypi_version = pypi_pyvol_version.split()[1:3]
            if installed_version != pypi_version:
                pyvol_version = apply_color(pyvol_version, "blue")
                
        if pyvol_version == "not found":
            pyvol_version = apply_color("not found", "red")
            form.button_install.setText("Install PyVOL")
            form.button_install.clicked.connect(lambda: install_pyvol(form))
        else:
            if update_available = True:
                form.button_install.setText("Update PyVOL")
                form.button_install.clicked.connect(lambda: update_pyvol(form))
            else:
                form.button_install.setText("Check for Updates")
                form.button_install.clicked.connect(refresh_status)

        try:
            import Bio
            biopython_version = Bio.__version__
        except:
            biopython_version = apply_color("not found", "red")

        try:
            import numpy as np
            numpy_version = apply_color(np.__version__, "green")
        except:            
            numpy_version = apply_color("not found", "red")

        try:
            import pandas as pd
            pandas_version = apply_color(pd.__version__, "green")
        except:
            pandas_version = apply_color("not found", "red")

        try:
            import scipy
            scipy_version = apply_color(scipy.__version__, "green")
        except:
            scipy_version = apply_color("not found", "red")

        try:
            import sklearn
            sklearn_version = apply_color(sklearn.__version__, "green")
        except:
            sklearn_version = apply_color("not found", "red")

        try:
            import trimesh
            trimesh_version = apply_color(trimesh.__version__, "green")
        except:
            trimesh_version = apply_color("not found", "red")

        msms_exe = distutils.spawn.find_executable("msms")
        if msms_exe == None:
            msms_exe = apply_color("not found", "red")
        else:
            msms_exe = apply_color(msms_exe, "green")
            
        form.label.setText(("Current installation status:\n"
                            "  pyvol: {0}\n"
                            "  biopython: {1}\n"
                            "  numpy: {2}\n"
                            "  pandas: {3}\n"
                            "  scipy: {4}\n"
                            "  sklearn: {5}\n"
                            "  trimesh: {6}\n"
                            "  msms exe: {7}\n"
                            "Please be patient when installing or updating--the PyPI and conda servers can sometimes take a few minutes."
        )).format(pyvol_version, biopython_version, numpy_version, pandas_version, scipy_version, sklearn_version, trimesh_version, msms_exe)

        form.button_close.clicked.connect(dialog.close)

    refresh_status(form)
    dialog.show()
