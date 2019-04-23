
from . import utilities
from Bio.PDB import PDBParser
from Bio.PDB.ResidueDepth import _get_atom_radius
import glob
import itertools
import numpy as np
import os
import pandas as pd
import scipy
import shutil
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import normalize
import sys
import tempfile
import trimesh


class Spheres(object):

    def __init__(self,
                 xyz=None,
                 r=None,
                 xyzr=None,
                 xyzrg=None,
                 g=None,
                 pdb=None,
                 bv=None,
                 mesh=None):
        """
        A Spheres object contains a list of xyz centers with r radii and g groups. It can be defined using xyzrg, xyzr (and optionally g), xyz (and optionally r or g), a pdb file (and optionally r or g), or a list of vertices with normals bounded by the spheres (requires r and optionally includes g)

        Parameters
        ----------
        xyz : (n, 3) float
            Array containing centers
        r : (n, 1) float
            Array containing radii
        xyzr : (n, 4) float
            Array containing centers and radii
        xyzrg : (n, 5) float
            Array containing centers, radii, and groups
        g : (n, 1) float
            Array containing groups
        pdb : string
            filename of a pdb to be processed into spheres
        bv : (n, 6) float
            Array containing vertices and normals
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
        if mesh is not None:
            self.mesh = mesh
        else:
            self.mesh = None


    def __add__(self, other):
        """
        Create a new Spheres object by overloading addition to concatenate xyzr contents
        Does not add meshes (just spheres)
        """
        
        if other is not None:
            return Spheres(xyzrg=np.concatenate([self.xyzrg, other.xyzrg], axis=0))
        else:
            return Spheres(xyzrg=np.copy(self.xyzrg))


    def copy(self):
        return Spheres(xyzrg=np.copy(self.xyzrg))


    def calculate_surface(self, probe_radius=1.4, cavity_atom=None, coordinate=None, all_components=False, exclusionary_radius=2.5, largest_only=False, noh=True, minimum_volume=200):
        """
        Calculate the SAS for a given probe radius 

        Parameters
        ----------
        probe_radius : float
            probe radius for msms calculation
        cavity_atom : int
            index of an atom used to define the binding pocket surface; only used for interior cavity identification; exclusive of all_components
        all_components : boolean
            flag to calculate all components; output mesh is None
        exclusionary_radius : float
            maximum radius of atoms considered by the nearest function (excludes pseudoatoms from identification)
        """

        tmpdir = tempfile.mkdtemp()
        xyzr_file = os.path.join(tmpdir, "pyvol.xyzr")
        msms_template = os.path.join(tmpdir, "pyvol_msms")
        
        np.savetxt(xyzr_file, self.xyzr, delimiter=' ')
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
            try:
                verts_raw = pd.read_csv("{0}.vert".format(msms_template), sep='\s+', skiprows=3, dtype=np.float_, header=None, encoding='latin1').values
                faces = pd.read_csv("{0}.face".format(msms_template), sep='\s+', skiprows=3, usecols=[0, 1, 2], dtype=np.int_, header=None, encoding='latin1').values
            except IOError:
                print("MSMS failed to run correctly", msms_template)
                raise IOError
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
            return [bspheres]
            
        else:
            spheres_list = []
            ac_template_list = [os.path.splitext(x)[0] for x in glob.glob("{0}_*.face".format(msms_template))]
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
                    if tm.volume >= minimum_volume:
                        bspheres = Spheres(bv=verts_raw, r=probe_radius, mesh=tm)
                        spheres_list.append(bspheres)

            if largest_only:
                return [bspheres]
            else:
                return spheres_list
            
    
    def identify_nonextraneous(self, ref_spheres, radius):
        """
        Returns all spheres less than radius away from any center in ref_spheres using cKDTree search built on the non-reference set

        Parameters
        ----------
        ref_spheres : Spheres
            A Spheres object containing the reference set
        radius : float
            Maximum distance between sets for inclusion
        """

        kdtree = scipy.spatial.cKDTree(self.xyz)
        groups = kdtree.query_ball_point(ref_spheres.xyz, radius, n_jobs=-1)
        indices = np.unique(list(itertools.chain.from_iterable(groups)))
        
        return Spheres(xyzrg=np.copy(self.xyzrg[indices, :]))


    def nearest(self, coordinate, max_radius=None):
        """
        returns the index of the sphere closest to a coordinate; if max_radius is specified, the sphere returned must have a radius <= max_radius

        Parameters
        ----------
        coordinate : (1, 3) float
            3D input coordinate
        max_radius : float
            maximum radius that the selected nearest sphere can have; used to exclude large radius exterior spheres from being selected 
        """

        if max_radius is None:
            sphere_list = self.xyz
        else:
            sphere_list = self.xyz[self.r <= max_radius]

        return np.argmin(scipy.spatial.distance.cdist(sphere_list, coordinate))


    def nearest_coord_to_external(self, coordinates):
        """
        returns the coordinate of the sphere closest to the supplied coordinates

        Parameters
        ----------
        coordinates : (n, 3) float
            3D input coordinates
        """
 
        kdtree = scipy.spatial.cKDTree(self.xyz)
        dist, indices = kdtree.query(coordinates, n_jobs=-1)
        
        return self.xyz[indices[np.argmin(dist)], :]
    
                
    def remove_duplicates(self, eps=0.01):
        """
        Remove duplicate spheres by identifying centers closer together than eps using DBSCAN

        Parameters
        ----------
        eps : float
            DBSCAN cutoff for identifying nearest neighbor distances between duplicate spheres
        """
        
        db = DBSCAN(eps=eps, min_samples=1).fit(self.xyz)
        values, indices = np.unique(db.labels_, return_index=True)
        self.xyzrg = self.xyzrg[indices, :]


    def remove_ungrouped(self):
        ungrouped_indices = np.where(self.g < 1)
        self.xyzrg = np.delete(self.xyzrg, ungrouped_indices, axis=0)
        self.mesh = None
        
        
    def write(self, filename, contents="xyzr", output_mesh=None):
        """
        Writes the contents of _xyzrg to a space delimited file 

        Parameters
        ----------
        filename : string
            filename for the output
        """

        if contents == "xyzrg":
            np.savetxt(filename, self.xyzrg, delimiter=' ')
        elif contents == "xyzr":
            np.savetxt(filename, self.xyzr, delimiter=' ')
        elif contents == "xyz":
            np.savetxt(filename, self.xyz, delimiter=' ')

        if output_mesh is not None:
            if self.mesh is None:
                print("Cannot write out an uninitialized mesh")
            else:
                if output_mesh == " ":
                    output_mesh = "{0}.obj".format(os.path.splitext(filename)[0])
                mesh.export(output_mesh)


    @property
    def xyzrg(self):
        return self._xyzrg


    @xyzrg.setter
    def xyzrg(self, value):
        if value.shape[1] != 5:
            raise ValueError("number of xyzrg array columns must equal 5")
        self._xyzrg = np.copy(value).astype(float)

        
    @property
    def xyzr(self):
        return self._xyzrg[:, 0:4]

    
    @xyzr.setter
    def xyzr(self, value):
        # resets all radii, groups, and positions
        if value.shape[1] != 4:
            raise ValueError("number of xyzr array columns must equal 4")
        xyzrg = np.zeros((value.shape[0], 5))
        xyzrg[:, 0:4] = value
        self._xyzrg = np.copy(xyzrg).astype(float)

        
    @property
    def xyz(self):
        return self._xyzrg[:, 0:3]

    
    @xyz.setter
    def xyz(self, value):
        # resets all radii, groups, and positions
        if value.shape[1] != 3:
            raise ValueError("number of xyz array columns must equal 3")
        xyzrg = np.zeros((value.shape[0], 5))
        xyzrg[:, 0:3] = value
        self._xyzrg = np.copy(xyzrg).astype(float)

        
    @property
    def r(self):
        return self._xyzrg[:, 3]

    
    @r.setter
    def r(self, value):
        if value is np.ndarray:
            if self._xyzrg.shape[0] == value.shape[0]:
                self._xyzrg[:, 3] = np.copy(value).astype(float)
            else:
                raise ValueError("Number of radii values must match the number of rows in the internal xyz array")
        else:
            self._xyzrg[:, 3] = value


    @property
    def g(self):
        return self._xyzrg[:, 4]

    
    @g.setter
    def g(self, value):
        if value is np.ndarray:
            if self._xyzrg.shape[0] == value.shape[0]:
                self._xyzrg[:, 4] = np.copy(value).astype(float)
            else:
                raise ValueError("Number of group values must match the number of rows in the internal xyzr array")
        else:
            self._xyzrg[:, 4] = value.astype(float)
