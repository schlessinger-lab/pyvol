
# experimental code not included in distributed release

import math
import numpy as np
import os
from pyvol.spheres import Spheres
from pyvol import cluster, pymol_utilities, utilities
from pymol import cgo, cmd
import shutil
import tempfile

def make_interface(center, normal, rn=1.5, rp=0.6, rpn=1.0, gc=None, g1=None, g2=None):

    neg_xyz = np.array([
        [0, 0, 1.1],
        [1.1, 0, 1.1],
        [0.55, 0.95, 1.1],
        [-0.55, 0.95, 1.1],
        [-1.1, 0, 1.1],
        [-0.55, -0.95, 1.1],
        [0.55, -0.95, 1.1],
        [2.2, 0, 1.1],
        [1.9, 1.1, 1.1],
        [1.1, 1.9, 1.1],
        [0, 2.2, 1.1],
        [-1.1, 1.9, 1.1],
        [-1.9, 1.1, 1.1],
        [-2.2, 0, 1.1],
        [-1.9, -1.1, 1.1],
        [-1.1, -1.9, 1.1],
        [0, -2.2, 1.1],
        [1.1, -1.9, 1.1],
        [1.9, -1.1, 1.1],
        [0, 0, -1.1],
        [1.1, 0, -1.1],
        [0.55, 0.95, -1.1],
        [-0.55, 0.95, -1.1],
        [-1.1, 0, -1.1],
        [-0.55, -0.95, -1.1],
        [0.55, -0.95, -1.1],
        [2.2, 0, -1.1],
        [1.9, 1.1, -1.1],
        [1.1, 1.9, -1.1],
        [0, 2.2, -1.1],
        [-1.1, 1.9, -1.1],
        [-1.9, 1.1, -1.1],
        [-2.2, 0, -1.1],
        [-1.9, -1.1, -1.1],
        [-1.1, -1.9, -1.1],
        [0, -2.2, -1.1],
        [1.1, -1.9, -1.1],
        [1.9, -1.1, -1.1],
    ])
    p2_xyz = np.array([
        [0, 0, 3.2],
        [1.1, 0, 3.2],
        [0.55, 0.95,3.21],
        [-0.55, 0.95, 3.2],
        [-1.1, 0, 3.2],
        [-0.55, -0.95, 3.2],
        [0.55, -0.95, 3.2],
        [2.2, 0, 3.2],
        [1.9, 1.1, 3.2],
        [1.1, 1.9, 3.2],
        [0, 2.2, 3.2],
        [-1.1, 1.9, 3.2],
        [-1.9, 1.1, 3.2],
        [-2.2, 0, 3.2],
        [-1.9, -1.1, 3.2],
        [-1.1, -1.9, 3.2],
        [0, -2.2, 3.2],
        [1.1, -1.9, 3.2],
        [1.9, -1.1, 3.2],

        [4.3, 0, 3.2],
        [3.7, 2.15, 3.2],
        [2.15, 3.7, 3.2],
        [0, 4.3, 3.2],
        [-2.15, 3.7, 3.2],
        [-3.7, 2.15, 3.2],
        [-4.3, 0, 3.2],
        [-3.7, -2.15, 3.2],
        [-2.15, -3.7, 3.2],
        [0, -4.3, 3.2],
        [2.15, -3.7, 3.2],
        [3.7, -2.15, 3.2],

        [4.3, 0, 2.0],
        [3.7, 2.15, 2.0],
        [2.15, 3.7, 2.0],
        [0, 4.3, 2.0],
        [-2.15, 3.7, 2.0],
        [-3.7, 2.15, 2.0],
        [-4.3, 0, 2.0],
        [-3.7, -2.15, 2.0],
        [-2.15, -3.7, 2.0],
        [0, -4.3, 2.0],
        [2.15, -3.7, 2.0],
        [3.7, -2.15, 2.0],

        [4.3, 0, 0.8],
        [3.7, 2.15, 0.8],
        [2.15, 3.7, 0.8],
        [0, 4.3, 0.8],
        [-2.15, 3.7, 0.8],
        [-3.7, 2.15, 0.8],
        [-4.3, 0, 0.8],
        [-3.7, -2.15, 0.8],
        [-2.15, -3.7, 0.8],
        [0, -4.3, 0.8],
        [2.15, -3.7, 0.8],
        [3.7, -2.15, 0.8],
    ])
    p1_xyz = np.array([
        [0, 0, -3.2],
        [1.1, 0, -3.2],
        [0.55, 0.95, -3.21],
        [-0.55, 0.95, -3.2],
        [-1.1, 0, -3.2],
        [-0.55, -0.95, -3.2],
        [0.55, -0.95, -3.2],
        [2.2, 0, -3.2],
        [1.9, 1.1, -3.2],
        [1.1, 1.9, -3.2],
        [0, 2.2, -3.2],
        [-1.1, 1.9, -3.2],
        [-1.9, 1.1, -3.2],
        [-2.2, 0, -3.2],
        [-1.9, -1.1, -3.2],
        [-1.1, -1.9, -3.2],
        [0, -2.2, -3.2],
        [1.1, -1.9, -3.2],
        [1.9, -1.1, -3.2],

        [4.3, 0, -3.2],
        [3.7, 2.15, -3.2],
        [2.15, 3.7, -3.2],
        [0, 4.3, -3.2],
        [-2.15, 3.7, -3.2],
        [-3.7, 2.15, -3.2],
        [-4.3, 0, -3.2],
        [-3.7, -2.15, -3.2],
        [-2.15, -3.7, -3.2],
        [0, -4.3, -3.2],
        [2.15, -3.7, -3.2],
        [3.7, -2.15, -3.2],

        [4.3, 0, -2.0],
        [3.7, 2.15, -2.0],
        [2.15, 3.7, -2.0],
        [0, 4.3, -2.0],
        [-2.15, 3.7, -2.0],
        [-3.7, 2.15, -2.0],
        [-4.3, 0, -2.0],
        [-3.7, -2.15, -2.0],
        [-2.15, -3.7, -2.0],
        [0, -4.3, -2.0],
        [2.15, -3.7, -2.0],
        [3.7, -2.15, -2.0],

        [4.3, 0, -0.8],
        [3.7, 2.15, -0.8],
        [2.15, 3.7, -0.8],
        [0, 4.3, -0.8],
        [-2.15, 3.7, -0.8],
        [-3.7, 2.15, -0.8],
        [-4.3, 0, -0.8],
        [-3.7, -2.15, -0.8],
        [-2.15, -3.7, -0.8],
        [0, -4.3, -0.8],
        [2.15, -3.7, -0.8],
        [3.7, -2.15, -0.8],
    ])


    rot_matrix = utilities.calculate_rotation_matrix(np.array([0, 0, 1]), normal)

    neg_spheres = Spheres(xyz=neg_xyz * rot_matrix + center, r=np.float64(rn), g=np.float64(gc), name="negative_connection")
    p1p_spheres = Spheres(xyz=p1_xyz * rot_matrix + center, r=np.float64(rp), g=g1, name="p1_connection")
    p1n_spheres = neg_spheres + Spheres(xyz=p2_xyz * rot_matrix + center, r=np.float64(rpn), g=gc, name="p1n_connection")
    p1n_spheres.name = "p1n"

    p2p_spheres = Spheres(xyz=p2_xyz * rot_matrix + center, r=np.float64(rp), g=g2, name="p2_connection")
    p2n_spheres = neg_spheres + Spheres(xyz=p1_xyz * rot_matrix + center, r=np.float64(rpn), g=gc, name="p2n_connection")
    p2n_spheres.name = "p2n"
    return [p1p_spheres, p1n_spheres, p2p_spheres, p2n_spheres, neg_spheres]
    # return Spheres(xyz=neg_xyz * rot_matrix + center, r=np.float64(r), g=np.float64(g), name="negative_connection"), Spheres(xyz=p1_xyz * rot_matrix + center, r=np.float64(r), g=g1, name="p1_connection")

def construct_3d_surfaces(*domains, **kwargs):
    # test = Cylinder(np.array([0,0,1]), np.array([0, 0, 1]), g=9)

    surface_rad = 1.4

    atomic_spheres = None
    domain_names = []
    for index, domain in enumerate(domains):
        output_dir = tempfile.mkdtemp()
        prefix = "domain_{0}".format(index)
        domain_names.append(domain.split(" ")[0])
        domain_pdb_file = os.path.join(output_dir, "{0}.pdb".format(prefix))
        cmd.save(domain_pdb_file, "{0} and poly".format(domain))

        d_p = Spheres(pdb=domain_pdb_file, g=np.float64(index + 1))

        if atomic_spheres is None:
            atomic_spheres = d_p
        else:
            atomic_spheres = atomic_spheres + d_p

    cluster.remove_overlap(atomic_spheres)

    domains = cluster.extract_groups(atomic_spheres, surf_radius=surface_rad, group_names=domain_names)

    # add the connectors
    if True:
        g1 = 2
        g2 = 1
        gc = len(domains) + 1

        residue_coordinates = cmd.get_coords("2wtk and chain B and resi 185", 1)

        coord, normal = utilities.closest_vertex_normals(domains[g1 -1].mesh, domains[g2 -1].mesh, ref_coordinates=residue_coordinates)
        p1p, p1n, p2p, p2n, connector = make_interface(coord, normal, gc=gc, g1=g1, g2=g2)

        # domains = p1p, p1n, p2p, p2n

        g1_name = domains[g1 -1].name
        cluster.remove_included_spheres(domains[g1 -1], p2n, 1.5)
        domains[g1 - 1] = domains[g1 -1] + p1p
        domains[g1 - 1].g = g1
        domains[g1 - 1].name = g1_name

        g2_name = domains[g2 - 1].name
        cluster.remove_included_spheres(domains[g2 -1], p1n, 1.5)
        domains[g2 - 1] = domains[g2 -1] + p2p
        domains[g2 - 1].g = g2
        domains[g2 - 1].name = g2_name

        domains.append(connector)
        domains[-1].g = gc

        gestalt = cluster.merge_sphere_list(domains)

        print(gestalt, gestalt.xyzrg.shape, np.unique(gestalt.g))
        cluster.remove_overlap(gestalt, static_last_group=True)
        print(gestalt.xyzrg.shape, np.unique(gestalt.g))
        gestalt_names = [domain.name for domain in domains]
        domains = cluster.extract_groups(gestalt, surf_radius=surface_rad, group_names=gestalt_names)
        print(domains)

    colors = ['tv_red', 'tv_orange', 'tv_blue', 'tv_green']
    for index, domain in enumerate(domains):
        print(domain.name, domain.xyzrg.shape)
        if not "connection" in domain.name:
            pymol_utilities.display_spheres_object(domain, domain.name, mode="mesh", color=colors[index])
        else:
            pymol_utilities.display_spheres_object(domain, domain.name, mode="spheres", color=colors[index])



from pymol import cmd
cmd.extend("test3d", construct_3d_surfaces)
