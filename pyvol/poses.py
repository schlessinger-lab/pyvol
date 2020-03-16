
# Experimental code not included in distributed release

from pyvol.spheres import Spheres
import logging
import numpy as np
import pandas as pd
import scipy

logger = logging.getLogger(__name__)

try:
    from rdkit import Chem
    from rdkit.Chem.Draw import rdMolDraw2D
    from rdkit.Chem import AllChem
except:
    logger.warning("rdkit not found; small molecule analysis will not be available prior to installation")


# def pose_report(pose_file, pocket_file, output_dir, output_prefix=None, name_parameter="_Name", scoring_parameter="r_i_glide_gscore", pocket_tolerance=3, panelx=250, panely=200, molsPerRow=4, rowsPerPage=6, palette=[(1,0.2,0.2), (1,0.55,0.15), (1,1,0.2), (0.2,1,0.2), (0.3,0.3,1), (0.5,1,1), (1,0.5,1)]):
#     """ Creates a report that highlights 2D compound representations by subpocket occupancy according to the poses in a provided sdf file
#
#     Args:
#       pose_file (str): input SDF file containing docked compound poses
#       pocket_file (str): input csv containing the spheres 5 dimensional array describing subpocket geometry; output with a "_spa.csv" ending
#       output_dir (str): output directory for all files
#       output_prefix (str): output prefix
#       name_parameter (str): SDF property key for the molecule name
#       scoring_parameter (str): SDF property key for whichever property should be shown in the report
#       pocket_tolerance (float): maximum distance (Angstrom) at which an atom outside of the defined subpocket volumes is still associated with a subpocket
#       panelx (int): horizontal width of the drawing space for each molecule
#       panely (int): vertical height of the drawing space for each molecule
#       molsPerRow (int): number of molecules to fit on a row (total width is <= panelx * molsPerRow)
#       rowsPerPage (int): number of rows of molecules to fit on each page (total height is <= panely * rowsPerPage)
#       palette ([(float,float,float)]): list of tuples of fractional RGB values that controls the highlighting colors
#
#     """
#
#     poses.compound_occupancy(pose_file, pocket_file, output_dir, output_prefix, name_parameter, scoring_parameter, pocket_tolerance, panelx, panely, molsPerRow, rowsPerPage, palette)


def compound_occupancy(pose_file, pocket_file, output_dir, output_prefix=None, name_parameter="_Name", scoring_parameter="r_i_glide_gscore", pocket_tolerance=3, panelx=250, panely=200, molsPerRow=4, rowsPerPage=6, palette=[(1,0.2,0.2), (1,0.55,0.15), (1,1,0.2), (0.2,1,0.2), (0.3,0.3,1), (0.5,1,1), (1,0.5,1)]):
    """ Creates a report that highlights 2D compound representations by subpocket occupancy according to the poses in a provided sdf file

    Args:
      pose_file (str): input SDF file containing docked compound poses
      pocket_file (str): input csv containing the spheres' 5 dimensional array describing subpocket geometry; output with a "_spa.csv" ending
      output_dir (str): output directory for all files
      output_prefix (str): output prefix
      name_parameter (str): SDF property key for the molecule name
      scoring_parameter (str): SDF property key for whichever property should be shown in the report
      pocket_tolerance (float): maximum distance (Angstrom) at which an atom outside of the defined subpocket volumes is still associated with a subpocket
      panelx (int): horizontal width of the drawing space for each molecule
      panely (int): vertical height of the drawing space for each molecule
      molsPerRow (int): number of molecules to fit on a row (total width is <= panelx * molsPerRow)
      rowsPerPage (int): number of rows of molecules to fit on each page (total height is <= panely * rowsPerPage)
      palette ([(float,float,float)]): list of tuples of fractional RGB values that controls the highlighting colors

    """

    molecules = [x for x in Chem.ForwardSDMolSupplier(pose_file) if x is not None]

    spheres = np.loadtxt(spheres_file, delimiter=' ')
    subpocket_spheres = Spheres(xyzrg=sp)

    for molecule in molecules:
        set_atom_subpockets(molecule, subpocket_spheres.propagate_groups_to_external(molecule.GetConformers()[0].GetPositions(), tolerance=pocket_tolerance))
    draw_molecules_with_subpockets(molecules, output_dir, output_prefix, palette, panelx, panely, molsPerRow, rowsPerPage, name_parameter, scoring_parameter)


def draw_molecules_with_subpockets(molecules, output_dir, output_prefix, palette=[(1,0.2,0.2), (1,0.55,0.15), (1,1,0.2), (0.2,1,0.2), (0.3,0.3,1), (0.5,1,1), (1,0.5,1)], panelx=250, panely=200, molsPerRow=4, rowsPerPage=6, name_parameter="_Name", scoring_parameter="r_i_glide_gscore"):
    """ Creates a report that highlights the 2D representation of docked molecules to indicate subpocket occupancy

    Args:
      molecules ([rdkit.Chem.rdchem.Mol]): list of rdkit molecules to draw
      output_dir (str): output directory
      output_prefix (str): output prefix
      palette ([(float,float,float)]): list of tuples of fractional RGB values; TODO: allow input of pymol style color strings
      panelx (int): horizontal width of the drawing space for each molecule
      panely (int): vertical height of the drawing space for each molecule
      molsPerRow (int): number of molecules to fit on a row (total width is <= panelx * molsPerRow)
      rowsPerPage (int): number of rows of molecules to fit on each page (total height is <= panely * rowsPerPage)
      name_parameter (str): SDF property key for the molecule name
      scoring_parameter (str): SDF property key for whichever property should be shown in the report

    """


    hats = []
    hbnds = []
    hatcolors = []
    hbndcolors = []
    prepped_mols = []
    legends = []
    for index, m in enumerate(molecules):
        ats = []
        bnds = []
        atcolors = {}
        bndcolors = {}

        for atom in m.GetAtoms():
            subpocket = atom.GetIntProp("subpocket")
            idx = atom.GetIdx()
            if subpocket >= 0:
                ats.append(idx)
            atcolors[idx] = palette[subpocket]

        for bnd in m.GetBonds():
            if bnd.GetBeginAtom().GetIntProp("subpocket") == bnd.GetEndAtom().GetIntProp("subpocket"):
                bnds.append(bnd.GetIdx())
                bndcolors[bnd.GetIdx()] = palette[bnd.GetBeginAtom().GetIntProp("subpocket")]

        hats.append(ats)
        hbnds.append(bnds)
        hatcolors.append(atcolors)
        hbndcolors.append(bndcolors)
        AllChem.Compute2DCoords(m)
        prepped_mols.append(rdMolDraw2D.PrepareMolForDrawing(m))
        legends.append("{0}: {1} ({2})".format(index, m.GetProp(name_parameter), m.GetProp(scoring_parameter)))

    molsPerPage = molsPerRow * rowsPerPage
    nPages = len(molecules) // molsPerPage
    if molsPerPage * nPages < len(molecules):
        nPages += 1

    page_data = []
    for page in range(nPages):
        start_mol = page * molsPerPage
        end_mol = min((page + 1) * molsPerPage, len(molecules))

        nRows = (end_mol - start_mol) // molsPerRow
        if molsPerRow * nRows < (end_mol - start_mol):
            nRows += 1

        canvasx = panelx * molsPerRow
        canvasy = panely * nRows

        drawer = rdMolDraw2D.MolDraw2DCairo(canvasx, canvasy, panelx, panely)

        page_mols = prepped_mols[start_mol:end_mol]
        page_hats = hats[start_mol:end_mol]
        page_hbnds = hbnds[start_mol:end_mol]
        page_hatcolors = hatcolors[start_mol:end_mol]
        page_hbndcolors = hbndcolors[start_mol:end_mol]
        page_legends = legends[start_mol:end_mol]

        drawer.DrawMolecules(page_mols, highlightAtoms=page_hats,highlightBonds=page_hbnds, highlightAtomColors=page_hatcolors, highlightBondColors=page_hbndcolors, legends=page_legends)

        drawer.FinishDrawing()
        txt = drawer.GetDrawingText()
        page_data.append(txt)

    filenames = [os.path.join(output_dir, "{0}_table_{1}.png".format(output_prefix, x)) for x in range(len(page_data))]

    for index, pd in enumerate(page_data):
        with open(filenames[index], 'wb') as f:
            f.write(page_data[index])


def set_atom_subpockets(molecule, groups):
    """ Apply calculated subpocket groups to each atom in a molecule

    Args:
      molecule (rdkit.Chem.rdchem.Mol): rdkit molecule object
      groups ([int]): list of subpocket identifiers

    """
    if molecule.GetNumAtoms() != groups.shape[0]:
        raise ValueError("Incorrect number of groups for molecule")

    for index, atom in enumerate(molecule.GetAtoms()):
        atom.SetIntProp("subpocket", int(groups[index]))
