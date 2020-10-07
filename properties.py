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

    enable_rename_objects_data: bpy.props.BoolProperty(name='Rename Objects or Data', default=True, options=set())
    options_rename_objects_data : bpy.props.EnumProperty(name='Mode', items = [
        ('rename_objects_to_data', 'Objects to Linked Data', 'Rename objects to their linked datablock'),
        ('rename_data_to_objects', 'Data to Last Linking Object', 'Rename datablocks to the last object that links to them')
    ], options=set())

    enable_rename_images: bpy.props.BoolProperty(name='Images to Filenames', default=True, options=set())
    enable_rename_materials_image_textures: bpy.props.BoolProperty(name='Materials to Image Textures', default=False, options=set())
    enable_rename_collection_instances: bpy.props.BoolProperty(name='Collection Instances', default=True, options=set())


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
