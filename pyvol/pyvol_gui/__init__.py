

__version__ = "1.5.a3"

import logging
import os
from pymol.Qt import QtCore, QtWidgets
import subprocess
import sys
import time

logger = logging.getLogger("pyvol.plugin")

def __init_plugin__(app=None):
    # Load the plugin in three steps: 1) import PyVOL 2) find msms if necessary 3) try to add gui

    # Import PyVOL
    try:
        from pymol import cmd
        from pyvol import pymol_interface
        cmd.extend('pocket', pymol_interface.pymol_pocket_cmdline)
        cmd.extend('load_pocket', pymol_interface.load_pocket)
        # cmd.extend('pose_report', pymol_interface.pose_report)
        logger.debug("PyVOL successfully imported")
    except:
        logger.info("PyVOL not imported; installing from local cache or PyPI to use")

    # add MSMS path to PyMOL preferences
    import distutils
    import distutils.util

    msms_exe = distutils.spawn.find_executable("msms")
    if msms_exe is None:
        try:
            from pymol import plugins
            msms_exe = plugins.pref_get("pyvol_msms_exe", default=None)

            if msms_exe is not None:
                sys.path.append(msms_exe)
        except:
            logger.warning("Cannot load PyMOL plugins module")

    # Try to link the GUI

    try:
        from pymol.plugins import addmenuitemqt
        addmenuitemqt('PyVOL', pyvol_window)
    except:
        logger.warning("PyVOL GUI not able to be loaded. This is most often seen when using older PyMOL distributions that use tkinter for GUIs rather thean QT. Update PyMOL to enable the GUI")

    try:
        cmd.extend("install_pyvol", install_pypi_pyvol)
        cmd.extend("install_cached_pyvol", install_cached_pyvol)
        cmd.extend("update_pyvol", update_pypi_pyvol)
    except:
        logger.warning("PyVOL installation commands not able to be added to command-line interface")


def pyvol_window():
    """ """

    from pymol.Qt.utils import loadUi

    dialog = QtWidgets.QDialog()
    uifile = os.path.join(os.path.dirname(__file__), 'pyvol_gui.ui')
    form = loadUi(uifile, dialog)

    refresh_installation_status(form)

    form.close_button.clicked.connect(dialog.close)
    form.run_button.clicked.connect(lambda: run_gui_pyvol(form))

    form.browse_button.clicked.connect(lambda: browse_pocket_file(form))
    form.load_button.clicked.connect(lambda: run_gui_load(form))

    dialog.show()

def browse_pocket_file(form):
    """ Launches a window to select a file

    """

    pocket_file_name = QtWidgets.QFileDialog.getOpenFileNames(None, 'Open file', os.getcwd(), filter='Pocket Files (*.obj *.csv)')[0][0]
    form.pocket_file_ledit.setText(pocket_file_name)

def install_pypi_pyvol():
    """ Attempts a de novo PyVOL installation using pip

    """

    subprocess.check_output([sys.executable, "-m", "pip", "install", "bio-pyvol"])

    try:
        from pymol import cmd
        from pyvol import pymol_interface
        cmd.extend('pocket', pymol_interface.pocket)
        cmd.extend('load_pocket', pymol_interface.load_pocket)
    except:
        pass
    refresh_installation_status(form)

def install_remote_pyvol(form):
    """ GUI wrapper for de novo PyVOL installation using pip

    """
    install_pypi_pyvol()
    refresh_installation_status(form)

def install_cached_pyvol():
    import re

    installer_dir = os.path.dirname(os.path.realpath(__file__))
    cache_dir = os.path.join(installer_dir, "cached_source")

    if os.path.isdir(cache_dir):
        bio_pyvol_gz = None
        for f in os.listdir(cache_dir):
            if re.match('bio-pyvol', f):
                bio_pyvol_gz = os.path.join(cache_dir, f)
                break

        if bio_pyvol_gz is None:
            logger.info("Cache directory found but no pyvol distribution")
        else:
            subprocess.check_output([sys.executable, "-m", "pip", "install", bio_pyvol_gz])

            install_status = False
            try:
                from pymol import cmd
                from pyvol import pymol_interface

                cmd.extend('pocket', pymol_interface.pocket)
                # cmd.extend('load_pocket', pymol_interface.load_pocket)
                install_status = True
            except:
                logger.warning("Installation questionable")

            if install_status:
                logger.info("Installation succeeded")

                import shutil
                shutil.rmtree(cache_dir)
    else:
        logger.info("Local cache not found; requires installation through command-line or GUI")

def install_local_pyvol(form):
    """ GUI wrapper for local PyVOL installation

    """
    install_cached_pyvol()
    refresh_installation_status(form)

def uninstall_pyvol(form):
    """ Attempts to uninstall PyVOL using pip

    """

    subprocess.check_output([sys.executable, "-m", "pip", "uninstall", "-y", "bio-pyvol"])

    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setWindowTitle("PyVOL Backend Uninstalled")
    msg.setInformativeText("The PyVOL backend has been uninstalled; however, the plugin must also be uninstalled using PyMOL's plugin manager.")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setMinimumSize(QtCore.QSize(600, 200)) # Doesn't seem to work
    msg.exec_()

    refresh_installation_status(form)

def update_pypi_pyvol():
    """ Attempts to update PyVOL using pip

    """

    subprocess.check_output([sys.executable, "-m", "pip", "install", "--upgrade", "bio-pyvol"])

def update_pyvol(form):
    """ GUI wrapper for updating PyVOL using pip

    """

    update_pypi_pyvol()

    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setWindowTitle("PyVOL Updated")
    msg.setInformativeText("The PyVOL backend has been updated; however, PyMOL will not load the new code until it is restarted.")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setMinimumSize(QtCore.QSize(600, 200)) # Doesn't seem to work
    msg.exec_()

    refresh_installation_status(form)

def refresh_installation_status(form, check_for_updates=False, add_msms_source=False):
    """ Check for updates and adjust the GUI to reflect the current installation status and availability of updates

    Args:
      check_for_updates (bool): query servers to see if an update is available? (Default value = False)

    """
    import distutils
    import distutils.util
    import json

    def apply_color(string, color):
        """ Applies a color to html text

        Args:
          string (str): text
          color (str): color to apply

        Returns:
          colored_text (str): html formatted text

        """
        return "<font color='{0}'>{1}</font>".format(color, string)

    all_pckgs = subprocess.check_output([sys.executable, "-m", "pip", "list", "--format=json"]).decode('utf-8').strip()
    pckgs = json.loads(all_pckgs)

    status_msg = ""
    pyvol_version = None
    biopython_version = None
    numpy_version = None
    pandas_version = None
    scipy_version = None
    sklearn_version = None
    trimesh_version = None

    remote_msg = None

    pyvol_installed = False
    for pckg in pckgs:
        if pckg["name"] == "bio-pyvol":
            pyvol_version = pckg["version"]
            pyvol_installed = True

    for pckg in pckgs:
        if pckg["name"] == "biopython":
            biopython_version = pckg["version"]
            if pyvol_installed:
                biopython_version = apply_color(biopython_version, "green")
        elif pckg["name"] == "numpy":
            numpy_version = pckg["version"]
            if pyvol_installed:
                numpy_version = apply_color(numpy_version, "green")
        elif pckg["name"] == "pandas":
            pandas_version = pckg["version"]
            if pyvol_installed:
                pandas_version = apply_color(pandas_version, "green")
        elif pckg["name"] == "scipy":
            scipy_version = pckg["version"]
            if pyvol_installed:
                scipy_version = apply_color(scipy_version, "green")
        elif pckg["name"] == "scikit-learn":
            sklearn_version = pckg["version"]
            if pyvol_installed:
                sklearn_version = apply_color(sklearn_version, "green")
        elif pckg["name"] == "trimesh":
            trimesh_version = pckg["version"]
            if pyvol_installed:
                trimesh_version = apply_color(trimesh_version, "green")

    if pyvol_version is None:
        pyvol_version = apply_color("not found", "red")
    if biopython_version is None:
        biopython_version = apply_color("not found", "red")
    if numpy_version is None:
        numpy_version = apply_color("not found", "red")
    if pandas_version is None:
        pandas_version = apply_color("not found", "red")
    if scipy_version is None:
        scipy_version = apply_color("not found", "red")
    if sklearn_version is None:
        sklearn_version = apply_color("not found", "red")
    if trimesh_version is None:
        trimesh_version = apply_color("not found", "red")

    # new options for finding msms
    msms_installed = False
    default_msms_present = False
    default_msms_exe = None
    incentive_msms_present = False
    incentive_msms_exe = None

    # First check the bundled directory
    if pyvol_installed:
        try:
            import pyvol
            import platform

            pyvol_dir = os.path.dirname(pyvol.__file__)
            msms_dir = os.path.join(pyvol_dir, "pkgs", "msms_2.6.1")

            if platform.system() == 'Linux':
                msms_exe = os.path.join(msms_dir, 'msms.x86_64Linux2.2.6.1')
            elif platform.system() == 'Windows':
                msms_exe = os.path.join(msms_dir, 'msms.win32.2.6.1.exe')
            elif platform.system() == 'Darwin':
                msms_exe = os.path.join(msms_dir, 'msms.MacOSX.2.6.1')

            if os.path.exists(msms_exe):
                default_msms_present = True
            else:
                default_msms_exe = None
        except:
            pass

    # Now check for the incentive msms
    bin_dir = os.path.dirname(sys.executable)
    pymol_root_dir = os.path.dirname(bin_dir)
    incentive_msms_exe = os.path.join(pymol_root_dir, "pkgs", "msms-2.6.1-2/bin/msms")

    if os.path.exists(incentive_msms_exe):
        incentive_msms_present = True
    else:
        incentive_msms_exe = None

    test_custom = form.msms_custom_ledit.text()
    if form.msms_default_rbutton.isChecked() and default_msms_present:
        form.msms_new_label.setText("{0}".format(default_msms_exe))
    elif form.msms_pymol_rbutton.isChecked() and incentive_msms_present:
        form.msms_new_label.setText("{0}".format(incentive_msms_exe))
    elif form.msms_custom_rbutton.isChecked():
        custom_msms_exe = form.msms_custom_ledit.text()
        if os.path.exists(custom_msms_exe):
            form.msms_new_label.setText("{0}".format(custom_msms_exe))

    form.msms_new_button.clicked.connect(lambda: refresh_installation_status(form, add_msms_source=True))
    # form.msms_new_button.setEnabled(False)
    new_msms_exe = form.msms_new_label.text()

    enable_add_source = False
    if new_msms_exe is not None:
        if os.path.exists(new_msms_exe):
            # form.msms_new_button.setEnabled(True)
            enable_add_source = True
            if add_msms_source:
                from pymol import plugins
                plugins.pref_set("pyvol_msms_exe", new_msms_exe)
                plugins.pref_save()

                if new_msms_exe not in sys.path:
                    sys.path.append(new_msms_exe)
    form.msms_new_button.setEnabled(enable_add_source)

    form.check_source_button.clicked.connect(lambda: refresh_installation_status(form))
    form.check_source_button.setEnabled(True)

    if pyvol_installed:
        msms_exe = distutils.spawn.find_executable("msms")
        if msms_exe is not None:
            if os.path.exists(msms_exe):
                msms_installed = True
            else:
                msms_exe = None

    if msms_installed:
        form.msms_status_label.setText("MSMS path: {0}".format(apply_color(msms_exe, "blue")))
    else:
        form.msms_status_label.setText("MSMS path: {0}".format(apply_color("not found", "red")))

    if not pyvol_installed:
        gui_version = __version__
        form.run_tab.setEnabled(False)
        form.run_button.setEnabled(False)
        form.load_tab.setEnabled(False)
        form.tabWidget.setCurrentIndex(2)

        form.install_remote_browser.setText("PyPI has not yet been queried.<br>")
        form.install_remote_button.setEnabled(True)
        form.install_remote_button.setText("Install PyVOL from PyPI")
        form.install_remote_button.clicked.connect(lambda: install_remote_pyvol(form))

        form.install_status_button.setText("Install PyVOL from Cache")

        cache_present = False
        cache_version = None
        installer_dir = os.path.dirname(os.path.realpath(__file__))
        cache_dir = os.path.join(installer_dir, "cached_source")

        if os.path.isdir(cache_dir):
            import re
            bio_pyvol_gz = None
            for f in os.listdir(cache_dir):
                if re.match('bio-pyvol', f):
                    cache_present = True
                    break

        if cache_present:
            status_msg = status_msg + "PyVOL can be installed from a local cache.<br>"
            form.install_status_button.setEnabled(True)
            form.install_status_button.clicked.connect(lambda: install_local_pyvol(form))
            form.install_status_browser.setText(status_msg)
        else:
            form.install_status_browser.setText("PyVOL is not currently installed.<br>")
            form.install_status_button.setEnabled(False)

    if pyvol_installed:
        form.setWindowTitle("PyVOL v{0}".format(pyvol_version))
        form.install_status_button.setText("Uninstall PyVOL")
        form.install_status_button.clicked.connect(lambda: uninstall_pyvol(form))
        form.install_status_button.setEnabled(True)

        if not check_for_updates:
            form.install_remote_button.setText("Check for Updates")
            form.install_remote_button.clicked.connect(lambda: refresh_installation_status(form, check_for_updates=True))
            form.install_remote_button.setEnabled(True)
        else:
            update_available = False

            avail_pckgs = subprocess.check_output([sys.executable, "-m", "pip", "list", "--outdated", "--format=json"]).decode('utf-8').strip()
            avail = json.loads(avail_pckgs)
            for pckg in avail:
                if pckg["name"] == "bio-pyvol":
                    update_available = True
                    form.install_remote_browser.setText(("A new version of PyVOL is available through PyPI:<br>"
                        "&nbsp;   pyvol: {0} -> {1}").format(pyvol_version, apply_color(pckg['latest_version'], "blue")))
                    break

            if update_available:
                form.install_remote_button.setText("Update PyVOL")
                form.install_remote_button.clicked.connect(lambda: update_pyvol(form))
                form.install_remote_button.setEnabled(True)
            else:
                form.install_remote_button.setText("Check for Updates")
                form.install_remote_button.clicked.connect(lambda: refresh_installation_status(form, check_for_updates=True))
                form.install_remote_button.setEnabled(True)
                form.install_remote_browser.setText(("Local PyVOL is up to date (version {0})<br>").format(pyvol_version))

        if msms_installed:
            form.run_tab.setEnabled(True)
            form.run_button.setEnabled(True)
            form.load_tab.setEnabled(True)
            status_msg = "PyVOL seems to be correctly installed.<br>"
        else:
            form.run_tab.setEnabled(False)
            form.run_button.setEnabled(False)
            form.load_tab.setEnabled(False)
            form.tabWidget.setCurrentIndex(2)
            status_msg = apply_color("Error: MSMS must be installed for PyVOL to run.<br>", "red")

        gui_version = None
        expected_gui_version = None
        try:
            import pyvol
            expected_gui_version = pyvol.__guiversion__
            if __version__ == expected_gui_version:
                gui_version = apply_color(__version__, "green")
            else:
                gui_version = apply_color("{0} ({1} expected)".format(__version__, expected_gui_version), "blue")
                status_msg = status_msg + "{0}--check whether the PyVOL backend is up-to-date and using the PyMOL plugin manager reinstall the newet version of the plugin from <a href='https://github.com/schlessingerlab/pyvol/blob/master/pyvolgui.zip'>github</a>.<br>".format(apply_color("GUI version mismatch", "red"))
        except:
            gui_version = __version__
        form.install_status_browser.setText((
            "&nbsp;   pyvol: {0}<br>"
            "&nbsp;   pyvol gui: {7}<br>"
            "&nbsp;   biopython: {1}<br>"
            "&nbsp;   numpy: {2}<br>"
            "&nbsp;   pandas: {3}<br>"
            "&nbsp;   scipy: {4}<br>"
            "&nbsp;   sklearn: {5}<br>"
            "&nbsp;   trimesh: {6}<br><br>"
            "{8}"
        ).format(pyvol_version, biopython_version, numpy_version, pandas_version, scipy_version, sklearn_version, trimesh_version, gui_version, status_msg))

def run_gui_load(form):
    """ Loads a precalculated pocket into PyMOL

    """
    from pyvol import pymol_interface

    # Loading Parameters
    pocket_file = form.pocket_file_ledit.text()
    if form.load_solid_rbutton.isChecked():
        display_mode = "solid"
    elif form.load_mesh_rbutton.isChecked():
        display_mode = "mesh"
    elif form.load_spheres_rbutton.isChecked():
        display_mode = "spheres"
    color = form.load_color_ledit.text()
    alpha = form.load_alpha_ledit.text()
    prefix = form.load_prefix_ledit.text()

    if color == "":
        color = None
    if alpha == "":
        alpha = None
    if prefix == "":
        prefix = None

    if not os.path.isfile(pocket_file):
        logger.error("Supplied file not found: {0}".format(pocket_file))
        return
    else:
        pymol_interface.load_pocket(pocket_file, name=prefix, display_mode=display_mode, color=color, alpha=alpha)

def run_gui_pyvol(form):
    """ Runs a PyVOL calculation

    """
    from pyvol import pymol_interface

    # Basic Parameters
    protein = form.prot_sele_ledit.text()
    excl_org = form.excl_org_cbox.isChecked()
    min_rad = form.min_rad_ledit.text()
    max_rad = form.max_rad_ledit.text()
    constrain_inputs = form.constrain_cbox.isChecked()

    # Pocket Selection
    minimum_volume = None
    ligand = None
    lig_incl_rad = None
    lig_excl_rad = None
    residue = None
    resid = None
    pocket_coordinate = None

    if form.all_rbutton.isChecked():
        mode = "all"
        minimum_volume = form.min_volume_ledit.text()
    elif form.largest_rbutton.isChecked():
        mode = "largest"
    elif form.ligand_rbutton.isChecked():
        mode = "specific"
        ligand = form.lig_sele_ledit.text()
        if form.lig_incl_rad_ledit.text() != "":
            lig_incl_rad = form.lig_incl_rad_ledit.text()
        if form.lig_excl_rad_ledit.text() != "":
            lig_excl_rad = form.lig_excl_rad_ledit.text()
    elif form.residue_rbutton.isChecked():
        mode = "specific"
        residue = form.residue_sele_ledit.text()
    elif form.resid_rbutton.isChecked():
        mode = "specific"
        resid = form.resid_ledit.text()
    elif form.coordinate_rbutton.isChecked():
        mode = "specific"
        pocket_coordinate = form.coordinate_ledit.text()

    # Partitioning Parameters
    subdivide = form.subdivide_cbox.isChecked()
    if not subdivide:
        subdivide = None
    max_clusters = form.max_clusters_ledit.text()
    min_subpocket_rad = form.min_internal_rad_ledit.text()
    min_subpocket_surf_rad = form.min_surf_rad_ledit.text()

    # Display and Output Options
    if form.solid_rbutton.isChecked():
        display_mode = "solid"
    elif form.mesh_rbutton.isChecked():
        display_mode = "mesh"
    elif form.spheres_rbutton.isChecked():
        display_mode = "spheres"
    color = form.color_ledit.text()
    alpha = form.alpha_ledit.text()
    prefix = form.prefix_ledit.text()
    palette = form.palette_ledit.text()
    if palette == "":
        palette = None
    if prefix == "":
        prefix = None
    output_dir = form.output_dir_ledit.text()
    if output_dir == "":
        output_dir = None

    pymol_interface.pocket(protein=protein, mode=mode, ligand=ligand, pocket_coordinate=pocket_coordinate, residue=residue, resid=resid, prefix=prefix, min_rad=min_rad, max_rad=max_rad, lig_excl_rad=lig_excl_rad, lig_incl_rad=lig_incl_rad, display_mode=display_mode, color=color, alpha=alpha, output_dir=output_dir, subdivide=subdivide, minimum_volume=minimum_volume, min_subpocket_rad=min_subpocket_rad, min_subpocket_surf_rad=min_subpocket_surf_rad, max_clusters=max_clusters, excl_org=excl_org, constrain_inputs=constrain_inputs, palette=palette)
