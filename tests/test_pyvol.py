# for now, use pytest==5.3.5 with pytest-sugar and pytest-xdist
# run using python -m pytest in the pyvol root directory

import os
import pytest
from pyvol.identify import pocket_wrapper

@pytest.mark.parametrize("prot_file", ["/home/rsmith/research/pyvol_development/pyvol/tests/1uwh_B_prot.pdb"])
@pytest.mark.parametrize("min_rad", [1.2, 1.4, 1.6])
@pytest.mark.parametrize("max_rad", [3.2, 3.4, 3.6])
@pytest.mark.parametrize("mode,lig_file,resid,coordinates", [("all", None, None, None), ("largest", None, None, None),("specific", None, "B513", None), ("specific", None, None, "95.6,29.8,68.5")])
# ("specific","/home/rsmith/research/pyvol_development/pyvol/tests/1uwh_B_lig.pdb", None, None),
def test_specification(prot_file, min_rad, max_rad, mode, lig_file, resid, coordinates):
    opts = {
        "prot_file": prot_file,
        "min_rad": min_rad,
        "max_rad": max_rad,
        "mode": mode,
        "lig_file": lig_file,
        "resid": resid,
        "coordinates": coordinates,
        "project_dir": "/home/rsmith/research/pyvol_development/pytest1"
    }
    pockets, opts = pocket_wrapper(**opts)

    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}.log".format(opts.get("prefix"))))
    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}.rept".format(opts.get("prefix"))))
    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}.cfg".format(opts.get("prefix"))))
    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}_p0.xyzrg".format(opts.get("prefix"))))
    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}_p0.obj".format(opts.get("prefix"))))

@pytest.mark.parametrize("prot_file", ["/home/rsmith/research/pyvol_development/pyvol/tests/1uwh_B_prot.pdb"])
@pytest.mark.parametrize("min_rad", [1.2, 1.4])
@pytest.mark.parametrize("max_rad", [3.4, 3.6])
@pytest.mark.parametrize("max_clusters", [2, 10])
@pytest.mark.parametrize("min_subpocket_rad", [1.5, 1.7])
@pytest.mark.parametrize("max_subpocket_rad", [3.2, 3.4])
@pytest.mark.parametrize("min_subpocket_surf_rad", [1.0, 1.2])
@pytest.mark.parametrize("radial_sampling", [0.1, 0.2])
@pytest.mark.parametrize("inclusion_radius_buffer", [1.0])
@pytest.mark.parametrize("min_cluster_size", [50])
def test_subdivide(prot_file, min_rad, max_rad, max_clusters, min_subpocket_rad, max_subpocket_rad, radial_sampling, min_subpocket_surf_rad, inclusion_radius_buffer, min_cluster_size):
    opts = {
        "prot_file": prot_file,
        "min_rad": min_rad,
        "max_rad": max_rad,
        "max_clusters": max_clusters,
        "min_subpocket_rad": min_subpocket_rad,
        "max_subpocket_rad": max_subpocket_rad,
        "radial_sampling": radial_sampling,
        "min_subpocket_surf_rad": min_subpocket_surf_rad,
        "inclusion_radius_buffer": inclusion_radius_buffer,
        "min_cluster_size": min_cluster_size,
        "mode": "largest",
        "subdivide": True,
        "project_dir": "/home/rsmith/research/pyvol_development/pytest1"
    }
    pockets, opts = pocket_wrapper(**opts)

    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}.log".format(opts.get("prefix"))))
    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}.rept".format(opts.get("prefix"))))
    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}.cfg".format(opts.get("prefix"))))
    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}_p0.xyzrg".format(opts.get("prefix"))))
    assert os.path.isfile(os.path.join(opts.get("output_dir"), "{0}_p0.obj".format(opts.get("prefix"))))
