
import importlib.util

def __init_plugin__(app=None):
    print("initializing")
    pyvol_spec = importlib.util.find_spec("pyvol")
    pyvol_spec = importlib.util.find_spec("pyvol2")
    print(pyvol_spec)

    if pyvol_spec is None:
        # PyVOL is not installed; load installation options
        from pymol.plugins import addmenuitemqt

        addmenuitemqt('Install PyVOL', install_window)
    else:
        # PyVOL has been installed; load main options
        from pymol import cmd
        from pyvol import pymol_interface

        cmd.extend('pocket', pymol_interface.pocket)


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
        
        dialog.close()

    form.button_install.clicked.connect(install_pyvol)
    form.button_close.clicked.connect(dialog.close)

    dialog.show()
