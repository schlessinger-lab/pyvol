
__version__ = "1.0.8"

def __init_plugin__(app=None):    
    from pymol import cmd
    

    from .pymol_interface import pocket, load_spheres
    cmd.extend('pocket', pocket)
    cmd.extend('load_spheres', load_spheres)
