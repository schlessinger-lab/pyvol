
from pymol import cmd
from pyvol import pymol_interface

cmd.extend('pocket', pymol_interface.pocket)
