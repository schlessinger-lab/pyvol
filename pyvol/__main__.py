
import argparse
from pyvol import configuration, identify


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="PyVOL", description="Identification, calculation, and segmentation of protein binding pockets", epilog="For complete documentation and tutorial on use, visit the project webpage: https://schlessingerlab.github.io/pyvol")
    parser.add_argument("cfg_file", help="input configuration file or output configuration file if specificying --template option")
    parser.add_argument("-t", "--template", action='store_true', help="write a template configuration file")

    args = parser.parse_args()

    if args.template:
        configuration.defaults_to_file(args.cfg_file)
    else:
        identify.pocket_wrapper(**configuration.file_to_opts(args.cfg_file))
