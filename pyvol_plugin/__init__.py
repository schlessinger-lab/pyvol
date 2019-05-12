

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

        subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "bio-pyvol"])
        refresh_status(form)

    def refresh_status(form, check_for_updates=False):
        import distutils.spawn
        import json
        import subprocess
        import sys

        def apply_color(string, color):
            return "<font color='{0}'>{1}</font>".format(color, string)

        pyvol_installed = False
        try:
            import pyvol
            pyvol_version = pyvol.__version__
            pyvol_installed = True
        except:
            pyvol_version = "not_found"

        update_available = False
        if check_for_updates:
            if pyvol_version != "not_found":
                versions = subprocess.check_output([sys.executable, "-m", "pip", "list", "--outdated", "--format=json"]).decode('utf-8').strip()
                packages = json.loads(versions)
                for package in packages:
                    if package["name"] == "bio-pyvol":
                        update_available = True
                        pyvol_version = apply_color("{0} ({1} available)".format(pyvol_version, package['latest_version']), "blue")
                        break
                if not update_available:
                    pyvol_version = apply_color(pyvol_version, "green")

        if pyvol_version == "not found":
            pyvol_version = apply_color("not found", "red")
            form.button_install.setText("Install PyVOL")
            form.button_install.clicked.connect(lambda: install_pyvol(form))
        else:
            if update_available == True:
                form.button_install.setText("Update PyVOL")
                form.button_install.clicked.connect(lambda: update_pyvol(form))
            else:
                form.button_install.setText("Check for Updates")
                form.button_install.clicked.connect(lambda: refresh_status(form, check_for_updates=True))

        try:
            import Bio
            biopython_version = Bio.__version__
            if pyvol_installed:
                biopython_version = apply_color(biopython_version, "green")
        except:
            biopython_version = apply_color("not found", "red")

        try:
            import numpy as np
            numpy_version = np.__version__
            if pyvol_installed:
                numpy_version = apply_color(numpy_version, "green")
        except:            
            numpy_version = apply_color("not found", "red")

        try:
            import pandas as pd
            pandas_version = pd.__version__
            if pyvol_installed:
                pandas_version = apply_color(pandas_version, "green")
        except:
            pandas_version = apply_color("not found", "red")

        try:
            import scipy
            scipy_version = scipy.__version__
            if pyvol_installed:
                scipy_version = apply_color(scipy_version, "green")
        except:
            scipy_version = apply_color("not found", "red")

        try:
            import sklearn
            sklearn_version = sklearn.__version__
            if pyvol_installed:
                sklearn_version = apply_color(sklearn_version, "green")
        except:
            sklearn_version = apply_color("not found", "red")

        try:
            import trimesh
            trimesh_version = trimesh.__version__
            if pyvol_installed:
                trimesh_version = apply_color(trimesh_version, "green")
        except:
            trimesh_version = apply_color("not found", "red")

        msms_exe = distutils.spawn.find_executable("msms")
        if msms_exe == None:
            msms_exe = apply_color("not found", "red")
        else:
            msms_exe = apply_color(msms_exe, "green")
            
        form.label.setText(("Current installation status:<br>"
                            "&nbsp;   pyvol: {0}<br>"
                            "&nbsp;   biopython: {1}<br>"
                            "&nbsp;   numpy: {2}<br>"
                            "&nbsp;   pandas: {3}<br>"
                            "&nbsp;   scipy: {4}<br>"
                            "&nbsp;   sklearn: {5}<br>"
                            "&nbsp;   trimesh: {6}<br>"
                            "&nbsp;   msms exe: {7}<br><br>"
                            "Please be patient when installing, updating, or checking for updates--the PyPI and conda servers can sometimes take a few seconds."
        ).format(pyvol_version, biopython_version, numpy_version, pandas_version, scipy_version, sklearn_version, trimesh_version, msms_exe))

        form.button_close.clicked.connect(dialog.close)

    refresh_status(form)
    dialog.show()
