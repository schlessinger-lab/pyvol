
""" PyMOL convenience functions used by the front-end contained in pymol_interface. """

import logging

logger = logging.getLogger(__name__)

try:
    from pymol import cgo, cmd, CmdException
except:
    logger.warning("PyMOL not imported")

def construct_palette(color_list=None, max_value=7, min_value=1):
    """ Construct a palette

    Args:
      color_list ([str]): list of PyMOL color strings (Default value = None)
      max_value (int): max palette index (Default value = 7)
      min_value (int): min palette index (Default value = 1)

    Returns:
      palette ([str]): list of color definitions

    """
    if color_list is None:
        color_list = ['tv_red', 'tv_orange', 'tv_yellow', 'tv_green', 'tv_blue', 'aquamarine', 'violet']
    if max_value <= len(color_list):
        logger.debug("Input palette accepted")
        return color_list[:max_value]

    colors = [cmd.get_color_tuple(x) for x in color_list]
    output_range = max_value - min_value + 1

    palette = []

    color_vectors = len(colors) - 1
    steps = output_range / color_vectors
    for cv in range(color_vectors):
        for x in range(steps):
            fx = float(x) / steps
            cl = [fx * colors[cv + 1][i] + (1 - fx) * colors[cv][i] for i in range(3)]
            cn = '0x%02x%02x%02x' % tuple([255 * x for x in cl])
            palette.append(cn)
    logger.debug("Palette constructed with {0} colors".format(len(palette)))
    return palette


def display_pseudoatom_group(spheres, name, color='gray60', palette=None):
    """ Displays a collection of pseudoatoms

    Args:
      spheres (Spheres): Spheres object holding pocket geometry
      name (str): display name
      color (str): PyMOL color string (Default value = 'gray60')
      palette ([str]): palette (Default value = None)

    """

    if spheres is None:
        return

    for index, xyzrg in enumerate(spheres.xyzrg):
        if palette is None:
            cmd.pseudoatom("{0}.{1}".format(name, index), pos=list(xyzrg[0:3]), vdw=float(xyzrg[3]), color=color)
        else:
            cmd.pseudoatom("{0}.{1}".format(name, index), pos=list(xyzrg[0:3]), vdw=float(xyzrg[3]), color=palette[int(xyzrg[4] - 1)])

    group_name = "{0}_g".format(name)
    cmd.group(group_name, "{0}.*".format(name))
    cmd.show("spheres", group_name)
    logger.debug("Pseudoatom group of {0} spheres created with group name {1}".format(spheres.xyzrg.shape[0], group_name))
    return group_name


def display_spheres_object(spheres, name, state=1, color='marine', alpha=0.7, mode="solid", palette=None):
    """ Loads a mesh object into a cgo list for display in PyMOL

    Args:
      spheres (Spheres): Spheres object containing all geometry
      name (str): display name
      state (int): model state (Default value = 1)
      color (str): PyMOL color string (Default value = 'marine')
      alpha (float): transparency value (Default value = 0.7)
      mode (str): display mode (Default value = "solid")
      palette ([str]): palette (Default value = None)

    """

    alpha = float(alpha)
    if spheres is None:
        return None

    if (mode == "mesh") or (mode == "solid"):
        if spheres.mesh is None:
            return None
        else:
            if mode == "solid":
                cmd.load_cgo(mesh_to_solid_CGO(spheres.mesh, color=color, alpha=alpha), name, state)
            else:
                cmd.load_cgo(mesh_to_wireframe_CGO(spheres.mesh, color=color, alpha=alpha), name, state)
            return None
    elif mode == "spheres":
        return display_pseudoatom_group(spheres, name, color=color, palette=None)


def mesh_to_solid_CGO(mesh, color='gray60', alpha=1.0):
    """Creates a solid CGO object for a mesh for display in PyMOL

    Args:
      mesh (Trimesh): Trimesh mesh object
      color (str): PyMOL color string (Default value = 'gray60')
      alpha (float): transparency value (Default value = 1.0)

    Returns:
      cgobuffer (str): CGO buffer that contains the instruction to load a solid object

    """

    cgobuffer = [cgo.BEGIN, cgo.TRIANGLES, cgo.ALPHA, alpha]
    color_values = cmd.get_color_tuple(cmd.get_color_index(color))

    for face in mesh.faces:
        for v_index in face:
            cgobuffer.append(cgo.COLOR)
            cgobuffer.extend(color_values)

            cgobuffer.append(cgo.NORMAL)
            cgobuffer.extend([mesh.vertex_normals[v_index][i] for i in range(3)])
            cgobuffer.append(cgo.VERTEX)
            cgobuffer.extend([mesh.vertices[v_index][i] for i in range(3)])
    cgobuffer.append(cgo.END)
    logger.debug("CGO solid object created for mesh: {0}".format(mesh))
    return cgobuffer


def mesh_to_wireframe_CGO(mesh, color='gray60', alpha=1.0):
    """Creates a wireframe CGO object for a mesh for display in PyMOL

    Args:
      mesh (Trimesh): Trimesh mesh object
      color (str): PyMOL color string (Default value = 'gray60')
      alpha (float): transparency value (Default value = 1.0)

    Returns:
      cgobuffer (str): CGO buffer that contains the instruction to load a wireframe object

    """

    cgobuffer = [cgo.BEGIN, cgo.LINES, cgo.ALPHA, alpha]

    cgobuffer.append(cgo.COLOR)
    cgobuffer.extend(cmd.get_color_tuple(cmd.get_color_index(color)))

    for edge in mesh.edges:
        cgobuffer.append(cgo.VERTEX)
        cgobuffer.extend(mesh.vertices[edge[0]])
        cgobuffer.append(cgo.VERTEX)
        cgobuffer.extend(mesh.vertices[edge[1]])

    cgobuffer.append(cgo.END)
    logger.debug("CGO wireframe object created for mesh: {0}".format(mesh))
    return cgobuffer
