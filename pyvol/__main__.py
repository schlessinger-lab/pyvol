
import argparse
import configparser
from pyvol import identify


def create_default_cfg(cfg_file = "defaults.cfg"):
    config = configparser.ConfigParser(allow_no_value=True)
    config.add_section("General")
    config.set("General", "prot_file", "input_prot.pdb")
    config.set("General", "lig_file", "input_lig.pdb")
    config.set("General", "min_rad", "1.4")
    config.set("General", "max_rad", "3.4")

    config.add_section("Specification")
    config.set("Specification", "mode", "largest")
    config.set("Specification", "coordinate")
    config.set("Specification", "residue")
    config.set("Specification", "lig_excl_rad")
    config.set("Specification", "lig_incl_rad")
    
    config.add_section("Partitioning")
    config.set("Partitioning", "subdivide", "False")
    config.set("Partitioning", "minimum_volume", "200")
    config.set("Partitioning", "max_clusters")
    config.set("Partitioning", "min_subpocket_rad", "1.7")
    
    config.add_section("Output")
    config.set("Output", "output_dir")
    config.set("Output", "prefix")

    with open(cfg_file, 'w') as configfile:
        config.write(configfile)


def run_from_cfg(cfg_file):
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(cfg_file)

    prot_file = config.get("General", "prot_file")
    lig_file = config.get("General", "lig_file", fallback=None)
    min_rad = config.getfloat("General", "min_rad", fallback=1.4)
    max_rad = config.getfloat("General", "max_rad", fallback=3.4)

    mode = config.get("Specification", "mode", fallback="largest")
    coordinate = config.get("Specification", "coordinate", fallback=None)
    residue = config.get("Specification", "residue", fallback=None)
    lig_excl_rad = config.get("Specification", "lig_excl_rad", fallback=None)
    if lig_excl_rad is not None:
        lig_excl_rad = float(lig_excl_rad)
    lig_incl_rad = config.get("Specification", "lig_incl_rad", fallback=None)
    if lig_incl_rad is not None:
        lig_incl_rad = float(lig_incl_rad)

    subdivide = config.getboolean("Partitioning", "subdivide", fallback=False)
    minimum_volume = config.getfloat("Partitioning", "minimum_volume", fallback=200)
    max_clusters = config.get("Partitioning", "max_clusters", fallback=None)
    if max_clusters is not None:
        max_clusters = int(max_clusters)
    min_subpocket_rad = config.getfloat("Partitioning", "min_subpocket_rad", fallback=1.7)

    output_dir = config.get("Output", "output_dir", fallback=None)
    prefix = config.get("Output", "prefix", fallback="pocket")

    spheres = identify.pocket(prot_file, mode=mode, lig_file=lig_file, coordinate=coordinate, residue=residue, min_rad=min_rad, max_rad=max_rad, lig_excl_rad=lig_excl_rad, lig_incl_rad=lig_incl_rad, subdivide=subdivide, minimum_volume=minimum_volume, min_subpocket_rad=min_subpocket_rad, max_clusters=max_clusters, prefix=prefix, output_dir=output_dir)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cfg_file", help="input configuration file or output configuration file if specificying --template option")
    parser.add_argument("-t", "--template", action='store_true', help="write a template configuration file")

    args = parser.parse_args()

    if args.template:
        create_default_cfg(args.cfg_file)
    else:
        run_from_cfg(args.cfg_file)
