
""" Defines the Spheres class which holds geometric information and performs basic operations on its data """

from . import utilities
from .exceptions import *
from Bio.PDB import PDBParser
from Bio.PDB.ResidueDepth import _get_atom_radius
import glob
import itertools
import logging
import numpy as np
import os
import pandas as pd
import scipy
import shutil
import sys
import tempfile
import trimesh

logger = logging.getLogger(__name__)


class Spheres(object):
    """ """

    def __init__(self, xyz=None, r=None, xyzr=None, xyzrg=None, g=None, pdb=None, bv=None, mesh=None, name=None, spheres_file=None):
        """
        A Spheres object contains a list of xyz centers with r radii and g groups. It can be defined using xyzrg, xyzr (and optionally g), xyz (and optionally r or g), a pdb file (and optionally r or g), or a list of vertices with normals bounded by the spheres (requires r and optionally includes g)

        Args:
          xyz (float nx3): Array containing centers (Default value = None)
          r (float nx1): Array containing radii (Default value = None)
          xyzr (float nx4): Array containing centers and radii (Default value = None)
          xyzrg (float nx5): Array containing centers, radii, and groups (Default value = None)
          g (float nx1): Array containing groups (Default value = None)
          pdb (str): filename of a pdb to be processed into spheres (Default value = None)
          bv (float nx6): Array containing vertices and normals (Default value = None)
          mesh (Trimesh): mesh object describing the surface (Default value = None)
          name (str): descriptive identifier (Default value = None)
          spheres_file (str): filename of a Spheres file to be read from disk (Default value = None)

        """

        if xyzrg is not None:
            self.xyzrg = xyzrg
        elif xyzr is not None:
            self.xyzr = xyzr

            if g is not None:
                self.g = g
        elif xyz is not None:
            self.xyz = xyz

            if r is not None:
                self.r = r
            if g is not None:
                self.g = g
        elif pdb is not None:
            if not sys.warnoptions:
                import warnings
                warnings.simplefilter("ignore")

            p = PDBParser(PERMISSIVE=1, QUIET=True)
            structure = p.get_structure("prot", pdb)

            self.xyz = np.array([atom.get_coord() for atom in structure[0].get_atoms()])

            if r is not None:
                self.r = r
            else:
                self.r = [_get_atom_radius(atom, rtype='united') for atom in structure[0].get_atoms()]

            if g is not None:
                self.g = g

        elif bv is not None and r is not None:
            self.xyz = bv[:, 0:3] + r * bv[:, 3:6]
            self.r = r
            self.remove_duplicates()

            if g is not None:
                self.g = g
        elif spheres_file is not None:
            xyzr_file = None
            obj_file = None

            base, ext = os.path.splitext(spheres_file)
            if ext == ".xyzrg":
                xyzrg_file = spheres_file
                obj_file = "{0}.obj".format(base)
            elif ext == ".obj":
                xyzrg_file = "{0}.xyzrg".format(base)
                if not os.path.isfile(xyzrg_file):
                    logger.error("No spheres file found with the name: {0}.xyzr or {0}.xyzrg".format(base))
                obj_file = spheres_file
            else:
                logger.error("Invalid filename given to read in spheres object: {0}".format(spheres_file))
                raise ValueError("Spheres objects must be .xyzrg or .obj ({0} provided)".format(spheres_file))
            spheres_data = np.loadtxt(xyzrg_file, delimiter=' ')

            if spheres_data.shape[1] == 5:
                self.xyzrg = spheres_data
            elif spheres_data.shape[1] == 4:
                self.xyzr = spheres_data
            else:
                logger.error("Spheres csv file contains the wrong number of columns")
                raise ValueError("{0} columns found in file {1}; must contain 4 or 5".format(spheres_data.shape[1], spheres_file))
            mesh = trimesh.load_mesh(obj_file)

            if name is None:
                name = os.path.basename(base)

        if mesh is not None:
            self.mesh = mesh
        else:
            self.mesh = None

        if name is not None:
            self.name = name
        else:
            self.name = None

        unique_ind = np.unique(self.xyzrg, axis=0, return_index=True)[1]
        self.xyzrg = self.xyzrg[sorted(unique_ind), :]


    def __add__(self, other):
        """ Create a new Spheres object by overloading addition to concatenate xyzr contents; does not add meshes (just spheres)

        Args:
            other (Spheres): Spheres object to add

        Returns:
            (Spheres): Spheres object representing concatenation

        """

        if other is not None:
            return Spheres(xyzrg=np.concatenate([self.xyzrg, other.xyzrg], axis=0))
        else:
            return Spheres(xyzrg=np.copy(self.xyzrg))


    def copy(self):
        """ Creates a copy in memory of itself
        """
        return Spheres(xyzrg=np.copy(self.xyzrg))


    def calculate_surface(self, probe_radius=1.4, cavity_atom=None, coordinate=None, all_components=False, exclusionary_radius=2.5, largest_only=False, noh=True, min_volume=200):
        """Calculate the SAS for a given probe radius

        Args:
          probe_radius (float): radius for surface calculations (Default value = 1.4)
          cavity_atom (int): id of a single atom which lies on the surface of the interior cavity of interest (Default value = None)
          coordinate ([float]): 3D coordinate to identify a cavity atom (Default value = None)
          all_components (bool): return all pockets? (Default value = False)
          exclusionary_radius (float): maximum permissibile distance to the closest identified surface element from the supplied coordinate (Default value = 2.5)
          largest_only (bool): return only the largest pocket? (Default value = False)
          noh (bool): remove waters before surface calculation? (Default value = True)
          minimum_volume (int): minimum volume of pockets returned when using 'all_components' (Default value = 200)

        """

        tmpdir = tempfile.mkdtemp()
        xyzr_file = os.path.join(tmpdir, "pyvol.xyzr")
        msms_template = os.path.join(tmpdir, "pyvol_msms")

        np.savetxt(xyzr_file, self.xyzr, delimiter=' ', fmt='% 1.3f'+' % 1.3f'+' % 1.3f'+'% 1.2f')
        if (cavity_atom is None) and (coordinate is not None):
            cavity_atom = self.nearest(coordinate, max_radius=exclusionary_radius)

        msms_cmd = ["msms", "-if", xyzr_file, "-of", msms_template, "-probe_radius", "{0}".format(probe_radius), "-no_area"]
        if noh:
            msms_cmd.append("-noh")
        if cavity_atom is not None:
            msms_cmd.extend(["-one_cavity", 1, cavity_atom])
        elif all_components:
            msms_cmd.append("-all_components")

        utilities.run_cmd(msms_cmd)

        sphere_list = []

        def read_msms_output(msms_template):
            """ Read the results of a MSMS run

            Args:
              msms_template (str): file prefix for the output from MSMS

            Returns:
              verts_raw (float nx6): raw contents of vertices file
              vertices (float nx3): 1-indexed 3D coordinates of vertices
              faces (float nx3): vertex connectivity graph
            """
            try:
                verts_raw = pd.read_csv("{0}.vert".format(msms_template), sep=r'\s+', skiprows=3, dtype=np.float_, header=None, encoding='latin1').values
                faces = pd.read_csv("{0}.face".format(msms_template), sep=r'\s+', skiprows=3, usecols=[0, 1, 2], dtype=np.int_, header=None, encoding='latin1').values
            except IOError:
                logger.error("MSMS failed to run correctly for {0}".format(msms_template))
                raise MSMSError("MSMS failed to run correctly for {0}".format(msms_template))
            else:
                vertices = np.zeros((verts_raw.shape[0] + 1, 3))
                vertices[1:, :] = verts_raw[:, 0:3]
                return verts_raw, vertices, faces

        if not all_components:
            verts_raw, vertices, faces = read_msms_output(msms_template)

            mesh = trimesh.base.Trimesh(vertices=vertices, faces=faces)
            if mesh.volume < 0:
                faces = np.flip(faces, axis=1)
                mesh = trimesh.base.Trimesh(vertices=vertices, faces=faces)
            bspheres = Spheres(bv=verts_raw, r=probe_radius, mesh=mesh)
            shutil.rmtree(tmpdir)
            logger.debug("Single volume calculated for {0}".format(self.name))
            return [bspheres]

        else:
            spheres_list = []
            ac_template_list = [os.path.splitext(x)[0] for x in glob.glob("{0}_*.face".format(msms_template))]
            logger.debug("{0} volumes calculated for {1}".format(len(ac_template_list), msms_template))

            largest_mesh = None
            for ac_template in ac_template_list:
                verts_raw, vertices, faces = read_msms_output(ac_template)

                tm = trimesh.base.Trimesh(vertices=vertices, faces=faces)
                if tm.volume < 0:
                    tm = trimesh.base.Trimesh(vertices=vertices, faces=np.flip(faces, axis=1))

                if largest_only:
                    if largest_mesh is None:
                        largest_mesh = tm
                        bspheres = Spheres(bv=verts_raw, r=probe_radius, mesh=tm)
                    elif tm.volume > largest_mesh.volume:
                        largest_mesh = tm
                        bspheres = Spheres(bv=verts_raw, r=probe_radius, mesh=tm)
                else:
                    if min_volume is not None:
                        if tm.volume < min_volume:
                            continue
                    bspheres = Spheres(bv=verts_raw, r=probe_radius, mesh=tm)
                    spheres_list.append(bspheres)

            shutil.rmtree(tmpdir)
            if largest_only:
                logger.debug("Largest volume identified for {0}".format(msms_template))
                return [bspheres]
            else:
                logger.debug("{0} volumes identified with sufficient volume for {0}".format(len(spheres_list), msms_template))
                return sorted(spheres_list, key=lambda s: s.mesh.volume, reverse=True)


    def identify_nonextraneous(self, ref_spheres, radius):
        """Returns all spheres less than radius away from any center in ref_spheres using cKDTree search built on the non-reference set

        Args:
          ref_spheres (Spheres): object that defines the pocket of interest
          radius (float): maximum distance to sphere centers to be considered nonextraneous

        Returns:
          nonextraneous (Spheres): a filtered Spheres object

        """

        kdtree = scipy.spatial.cKDTree(self.xyz)
        groups = kdtree.query_ball_point(ref_spheres.xyz, radius, n_jobs=-1)
        indices = np.unique(list(itertools.chain.from_iterable(groups)))

        logger.debug("Non-extraneous spheres removed")
        return Spheres(xyzrg=np.copy(self.xyzrg[indices, :]))


    def nearest(self, coordinate, max_radius=None):
        """ Returns the index of the sphere closest to a coordinate; if max_radius is specified, the sphere returned must have a radius <= max_radius

        Args:
          coordinate (float nx3): 3D input coordinate
          max_radius (float): maximum permissibile distance to the nearest sphere (Default value = None)

        Returns:
          nearest_index: index of the closest sphere

        """

        if max_radius is None:
            sphere_list = self.xyz
        else:
            sphere_list = self.xyz[self.r <= max_radius]

        return np.argmin(scipy.spatial.distance.cdist(sphere_list, coordinate))


    def propagate_groups_to_external(self, coordinates, tolerance=3):
        """ Propagates group identifications to an external set of coordinates

        Args:
            coordinates (Nx3 ndarray): coordinates of the external spheres
            tolerance (float): maximum distance exclusive of the radii of the internal spheres

        Returns:
            prop_groups ([int]): list of group identifications for the supplied external coordinates

        """

        kdtree = scipy.spatial.cKDTree(self.xyz)
        dist, indices = kdtree.query(coordinates, n_jobs=-1)

        sphere_inclusion = dist - self.r[indices]
        prop_groups = self.g[indices].astype(int)
        prop_groups[sphere_inclusion > tolerance] = -1

        return prop_groups


    def nearest_coord_to_external(self, coordinates):
        """ Returns the coordinate of the sphere closest to the supplied coordinates

        Args:
          coordinates (float nx3): set of coordinates

        Returns:
          coordinate (float 1x3): coordinate of internal sphere closest to the supplied coordinates

        """

        kdtree = scipy.spatial.cKDTree(self.xyz)
        dist, indices = kdtree.query(coordinates, n_jobs=-1)

        return self.xyz[indices[np.argmin(dist)], :]


    def remove_duplicates(self, eps=0.01):
        """ Remove duplicate spheres by identifying centers closer together than eps using DBSCAN

        Args:
          eps (float): DBSCAN input parameter (Default value = 0.01)

        """
        from sklearn.cluster import DBSCAN

        db = DBSCAN(eps=eps, min_samples=1).fit(self.xyz)
        values, indices = np.unique(db.labels_, return_index=True)
        self.xyzrg = self.xyzrg[indices, :]


    def remove_ungrouped(self):
        """ Remove all spheres that did not adequately cluster with the remainder of the set

        """
        ungrouped_indices = np.where(self.g < 1)
        self.xyzrg = np.delete(self.xyzrg, ungrouped_indices, axis=0)
        self.mesh = None
        if len(ungrouped_indices) > 0:
            logger.debug("{0} ungrouped spheres removed".format(len(ungrouped_indices)))


    def remove_groups(self, groups):
        """ Remove all spheres with specified group affiliations

        Args:
          groups ([float]): list of groups to remove

        """
        group_indices = np.where(np.isin(self.g, groups))
        self.xyzrg = np.delete(self.xyzrg, group_indices, axis=0)
        self.mesh = None


    def write(self, filename, contents="xyzrg", output_mesh=True):
        """Writes the contents of _xyzrg to a space delimited file

        Args:
          filename (str): filename to write the report and mesh if indicated
          contents (str): string describing which columns to write to file (Default value = "xyzrg")
          output_mesh (bool): write mesh to file? (Default value = True)

        """

        if contents == "xyzrg":
            np.savetxt(filename, self.xyzrg, delimiter=' ')
            logger.debug("{0} written to xyzrg file: {1}".format(self.name, filename))
        elif contents == "xyzr":
            np.savetxt(filename, self.xyzr, delimiter=' ')
            logger.debug("{0} written to xyzr file: {1}".format(self.name, filename))
        elif contents == "xyz":
            np.savetxt(filename, self.xyz, delimiter=' ')
            logger.debug("{0} written to xyz file: {1}".format(self.name, filename))

        if output_mesh:
            if self.mesh is None:
                logger.error("Cannot write out an uninitialized mesh")
                raise ValueError("Mesh can not be written to file corresponding to {0}".format(filename))
            else:
                output_mesh = "{0}.obj".format(os.path.splitext(filename)[0])
                self.mesh.export(file_obj = output_mesh)
                logger.debug("{0} written to obj file: {1}.obj".format(self.name, os.path.splitext(filename)[0]))

    @property
    def xyzrg(self):
        """ Retrieve the coordinates, radii, and group ids

        """
        return self._xyzrg


    @xyzrg.setter
    def xyzrg(self, value):
        """ Set the coordinates, radii, and group ids

        Args:
          value (float 5xn): coordinates, radii, and group ids

        """
        if value.shape[1] != 5:
            raise ValueError("number of xyzrg array columns must equal 5")
        self._xyzrg = np.copy(value).astype(float)


    @property
    def xyzr(self):
        """ Retrieve coordinates and radii

        """
        return self._xyzrg[:, 0:4]


    @xyzr.setter
    def xyzr(self, value):
        """ Set the coordinates and radii

        Args:
          value (float 4xn): coordinates and radii

        """
        # resets all radii, groups, and positions
        if value.shape[1] != 4:
            raise ValueError("number of xyzr array columns must equal 4")
        xyzrg = np.zeros((value.shape[0], 5))
        xyzrg[:, 0:4] = value
        self._xyzrg = np.copy(xyzrg).astype(float)


    @property
    def xyz(self):
        """ Retrieve the coordinates

        """
        return self._xyzrg[:, 0:3]


    @xyz.setter
    def xyz(self, value):
        """ Selectively set the coordinates

        Args:
          value (float 3xn): coordinates

        """
        # resets all radii, groups, and positions
        if value.shape[1] != 3:
            raise ValueError("number of xyz array columns must equal 3")
        xyzrg = np.zeros((value.shape[0], 5))
        xyzrg[:, 0:3] = value
        self._xyzrg = np.copy(xyzrg).astype(float)


    @property
    def r(self):
        """ Retrieve the radii

        """
        return self._xyzrg[:, 3]


    @r.setter
    def r(self, value):
        """ Selectively set the radius index

        Args:
          value (float 1xn): radii

        """
        if value is np.ndarray:
            if self._xyzrg.shape[0] == value.shape[0]:
                self._xyzrg[:, 3] = np.copy(value).astype(float)
            else:
                raise ValueError("Number of radii values must match the number of rows in the internal xyz array")
        else:
            self._xyzrg[:, 3] = value


    @property
    def g(self):
        """ Retrieve the group indices

        """
        return self._xyzrg[:, 4]


    @g.setter
    def g(self, value):
        """ Selectively set the group index

        Args:
          value (float 1xn): group ids

        """
        if value is np.ndarray:
            if self._xyzrg.shape[0] == value.shape[0]:
                self._xyzrg[:, 4] = np.copy(value).astype(float)
            else:
                raise ValueError("Number of group values must match the number of rows in the internal xyzr array")
        else:
            self._xyzrg[:, 4] = value
