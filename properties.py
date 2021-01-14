##############################################################################
# Imports
##############################################################################


import bpy
from . import functions
from importlib import reload
reload(functions)


##############################################################################
# Properties
##############################################################################


class SweeperSettings(bpy.types.PropertyGroup):

    rename_keyword: bpy.props.StringProperty(name='Keyword', default='', update=functions.keyword_rename, options=set(), description='New name for the selected objects')

    enable_rename_objects: bpy.props.BoolProperty(name='Objects', default=True, options=set(), description='Apply naming conventions to Objects')
    enable_rename_data: bpy.props.EnumProperty(name='Data options', items = [
        ('and_data', 'And Data', 'Rename datablocks to their linking objects'),
        ('to_data', 'From Data', 'Rename objects to their linked datablocks')
    ], options=set(), default='and_data', description='Rename data to objects, or vice-versa')
    enable_rename_collections: bpy.props.BoolProperty(name='Collections', default=True, options=set(), description='Apply naming conventions to Collections')
    enable_rename_materials: bpy.props.BoolProperty(name='Materials', default=True, options=set(), description='Apply naming conventions to Materials')

    enable_rename_images: bpy.props.BoolProperty(name='Images to Filenames', default=True, options=set(), description='Rename Images to their filename, sans its extension')
    enable_rename_materials_image_textures: bpy.props.BoolProperty(name='Materials to Image Textures', default=False, options=set(), description='Rename Materials to their first Image Texture')
    enable_rename_worlds_env_textures: bpy.props.BoolProperty(name='Worlds to Environment Textures', default=False, options=set(), description='Rename Worlds to their first Environment Texture')

    enable_remove_unused_material_slots: bpy.props.BoolProperty(name='Unused Material Slots', default=True, options=set(), description='On selection or everything')
    enable_remove_vertex_groups: bpy.props.BoolProperty(name='Vertex Groups', default=False, options=set(), description='On selection or everything')
    enable_remove_custom_normals: bpy.props.BoolProperty(name='Custom Normals', default=False, options=set(), description='On selection or everything')
    enable_remove_uv_maps: bpy.props.BoolProperty(name='UV Maps', default=False, options=set(), description='On selection or everything')


##############################################################################
# Registration
##############################################################################


def register():
    bpy.utils.register_class(SweeperSettings)
    bpy.types.Scene.sweeper_settings = bpy.props.PointerProperty(type=SweeperSettings)


def unregister():
    bpy.utils.unregister_class(SweeperSettings)
    try:
        del bpy.types.Scene.sweeper_settings
    except:
        pass
