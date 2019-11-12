
import numpy as np
from pyvol.spheres import Spheres
from pyvol import cluster, pymol_utilities
import os
from pymol import cgo, cmd
import shutil
import tempfile

def construct_3d_surfaces(*domains, **kwargs):
    surface_rad = 1.4

    atomic_spheres = None
    for index, domain in enumerate(domains):
        output_dir = tempfile.mkdtemp()
        prefix = "domain_{0}".format(index)
        domain_pdb_file = os.path.join(output_dir, "{0}.pdb".format(prefix))
        cmd.save(domain_pdb_file, "{0} and poly".format(domain))

        d_p = Spheres(pdb=domain_pdb_file, g=np.float64(index + 1))

        if atomic_spheres is None:
            atomic_spheres = d_p
        else:
            atomic_spheres = atomic_spheres + d_p
    print("full", atomic_spheres.xyzrg.shape)
    # pymol_utilities.display_spheres_object(atomic_spheres, "combined")

    raws = cluster.extract_groups(atomic_spheres, surf_radius=surface_rad, prefix="raw")
    for raw in raws:
        print(raw.name, raw.xyzrg.shape)
        # pymol_utilities.display_spheres_object(raw, raw.name, mode="spheres")
        # raw.write("/home/rsmith/research/pyvol_development/mek/{}.stl".format(raw.name))

    cluster.remove_overlap(atomic_spheres)
    print("post-remove", atomic_spheres.xyzrg.shape)

    # d_s = d_p.calculate_surface(probe_radius=surface_rad)[0]
    # cluster.remove_overlap(domain_spheres, radii=[surface_rad])
    domains = cluster.extract_groups(atomic_spheres, surf_radius=surface_rad, prefix="domain")

    colors = ['tv_red', 'tv_orange', 'tv_blue']
    for index, domain in enumerate(domains):
        print(domain.name, domain.xyzrg.shape)
        pymol_utilities.display_spheres_object(domain, domain.name, mode="spheres", color=colors[index])
        pymol_utilities.display_spheres_object(domain, "{0}_surf".format(domain.name), mode="mesh", color=colors[index])

from pymol import cmd
cmd.extend("test3d", construct_3d_surfaces)
