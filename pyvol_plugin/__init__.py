

def __init_plugin__(app=None):
    try:
        from pymol import cmd
        from pyvol import pymol_interface
        cmd.extend('pocket', pymol_interface.pocket)
        cmd.extend('load_pocket', pymol_interface.load_pocket)
    except:
        pass
    finally:
        from pymol.plugins import addmenuitemqt
        addmenuitemqt('PyVOL', pyvol_window)


def pyvol_window():
    import os
    from pymol.Qt import QtWidgets
    from pymol.Qt.utils import loadUi

    dialog = QtWidgets.QDialog()
    uifile = os.path.join(os.path.dirname(__file__), 'pyvolgui.ui')
    form = loadUi(uifile, dialog)

    def browse_pocket_file(form):
        pocket_file_name = QtWidgets.QFileDialog.getOpenFileNames(None, 'Open file', os.getcwd(), filter='Pocket Files (*.obj *.csv)')[0][0]
        form.pocket_file_ledit.setText(pocket_file_name)
    
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
            cmd.extend('load_pocket', pymol_interface.load_pocket)
        except:
            print("Installation still not complete")
        refresh_installation_status(form)

    def update_pyvol(form):
        import subprocess
        import sys

        subprocess.call([sys.executable, "-m", "pip", "install", "--upgrade", "bio-pyvol"])
        refresh_installation_status(form)

    def refresh_installation_status(form, check_for_updates=False):
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
            form.run_tab.setEnabled(True)
            form.run_button.setEnabled(True)
            form.load_tab.setEnabled(True)
            form.setWindowTitle("PyVOL v{0}".format(pyvol_version))
        except:
            pyvol_version = "not_found"
            form.run_tab.setEnabled(False)
            form.run_button.setEnabled(False)
            form.load_tab.setEnabled(False)

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
                    pyvol_version = apply_color("{0} (up-to-date)".format(pyvol_version), "green")

        if pyvol_version == "not found":
            pyvol_version = apply_color("not found", "red")
            form.install_button.setText("Install PyVOL")
            form.install_button.clicked.connect(lambda: install_pyvol(form))
        else:
            if update_available == True:
                form.install_button.setText("Update PyVOL")
                form.install_button.clicked.connect(lambda: update_pyvol(form))
            else:
                form.install_button.setText("Check for Updates")
                form.install_button.clicked.connect(lambda: refresh_installation_status(form, check_for_updates=True))

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
            
        form.install_status_browser.setText((
                            "&nbsp;   pyvol: {0}<br>"
                            "&nbsp;   biopython: {1}<br>"
                            "&nbsp;   numpy: {2}<br>"
                            "&nbsp;   pandas: {3}<br>"
                            "&nbsp;   scipy: {4}<br>"
                            "&nbsp;   sklearn: {5}<br>"
                            "&nbsp;   trimesh: {6}<br>"
                            "&nbsp;   msms exe: {7}<br><br>"
        ).format(pyvol_version, biopython_version, numpy_version, pandas_version, scipy_version, sklearn_version, trimesh_version, msms_exe))

    def run_gui_load(form):
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
            print("Supplied file not found: {0}".format(pocket_file))
            return
        else:
            pymol_interface.load_pocket(pocket_file, name=prefix, display_mode=display_mode, color=color, alpha=alpha)
        
    def run_gui_pyvol(form):
        from pyvol import pymol_interface
        
        # Basic Parameters
        protein = form.prot_sele_ledit.text()
        excl_org = form.excl_org_cbox.isChecked()
        min_rad = form.min_rad_ledit.text()
        max_rad = form.max_rad_ledit.text()

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
        if prefix == "":
            prefix = None
        output_dir = form.output_dir_ledit.text()
        if output_dir == "":
            output_dir = None

        # print(protein, mode, ligand, pocket_coordinate, residue, resid, prefix, min_rad, max_rad, lig_excl_rad, lig_incl_rad, display_mode, color, alpha, output_dir, subdivide, minimum_volume, min_subpocket_rad, min_subpocket_surf_rad, max_clusters, excl_org)

        pymol_interface.pocket(protein=protein, mode=mode, ligand=ligand, pocket_coordinate=pocket_coordinate, residue=residue, resid=resid, prefix=prefix, min_rad=min_rad, max_rad=max_rad, lig_excl_rad=lig_excl_rad, lig_incl_rad=lig_incl_rad, display_mode=display_mode, color=color, alpha=alpha, output_dir=output_dir, subdivide=subdivide, minimum_volume=minimum_volume, min_subpocket_rad=min_subpocket_rad, min_subpocket_surf_rad=min_subpocket_surf_rad, max_clusters=max_clusters, excl_org=excl_org)

    refresh_installation_status(form)
    
    form.close_button.clicked.connect(dialog.close)
    form.run_button.clicked.connect(lambda: run_gui_pyvol(form))

    form.browse_button.clicked.connect(lambda: browse_pocket_file(form))
    form.load_button.clicked.connect(lambda: run_gui_load(form))
    
    dialog.show()
