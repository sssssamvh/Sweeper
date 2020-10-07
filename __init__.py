bl_info = {
    'name': 'Sweeper',
    'description': 'A collection of scene maintenance tools.',
    'author': 'Sam Van Hulle',
    'version': (2, 0, 0),
    'blender': (2, 90, 0),
    'location': 'View3D > UI',
    'category': 'Tools'
}


##############################################################################
# Imports
##############################################################################


import bpy
from . import properties, operators, panels
modules = [properties, operators, panels]
from importlib import reload
for m in modules:
    reload(m)


##############################################################################
# Registration
##############################################################################


def register():
    for module in modules:
        module.register()


def unregister():
    for module in modules:
        module.unregister()


if __name__ == '__main__':
    register()
