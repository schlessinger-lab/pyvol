
import importlib.util

def __init_plugin__(app=None):
    print("initializing")
    # # pyvol_spec = importlib.util.find_spec("pyvol")

    # if pyvol_spec is None:
    #     print("pyvol not found--installation route")
    #     # PyVOL is not installed; load installation options
    #     from pymol.plugins import addmenuitemqt

    #     addmenuitemqt('Install PyVOL', install_window)
    # else:
    #     print("pyvol found--extending pocket")
    #     # PyVOL has been installed; load main options
    #     from pymol import cmd
    #     from pyvol import pymol_interface

    #     cmd.extend('pocket', pymol_interface.pocket)

    try:
        from pymol import cmd
        from pyvol import pymol_interface
        cmd.extend('pocket', pymol_interface.pocket)
        cmd.extend('load_spheres', pymol_interface.load_spheres)
    except:
        from pymol.plugins import addmenuitemqt
        addmenuitemqt('Install PyVOL', install_window)
        


def install_window():
    import os
    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi

    dialog = QtWidgets.QDialog()
    uifile = os.path.join(os.path.dirname(__file__), 'installwidget.ui')
    form = loadUi(uifile, dialog)

    def install_pyvol():
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
        
        dialog.close()

    form.button_install.clicked.connect(install_pyvol)
    form.button_close.clicked.connect(dialog.close)

    dialog.show()
