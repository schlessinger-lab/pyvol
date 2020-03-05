
import argparse
import logging
from pyvol import configuration, identify

main_logger = logging.getLogger("pyvol")
main_logger.setLevel("DEBUG")
logger = logging.getLogger(__name__)

stdio_handler_found = False
for handler in main_logger.handlers:
    if type(handler) is logging.StreamHandler:
        stdio_handler_found = True
        break
if not stdio_handler_found:
    log_out = logging.StreamHandler()
    log_out.setLevel("INFO")
    log_out.setFormatter(logging.Formatter("%(name)-12s:".ljust(25) + "\t%(levelname)-8s" + "\t%(message)s"))
    main_logger.addHandler(log_out)







if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cfg_file", help="input configuration file or output configuration file if specificying --template option")
    parser.add_argument("-t", "--template", action='store_true', help="write a template configuration file")

    args = parser.parse_args()

    if args.template:
        configuration.create_default_cfg(args.cfg_file)
    else:
        configuration.run_from_cfg(args.cfg_file)
