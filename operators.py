##############################################################################
# Imports
##############################################################################


import bpy
from . import functions
from importlib import reload
reload(functions)


##############################################################################
# Operators
##############################################################################


class AUTORENAME_OT_run_auto_renamer(bpy.types.Operator):
    """Run the auto renamer"""

    bl_idname = 'sweeper.autorename_ot_run_auto_renamer'
    bl_label = 'Auto Rename'
    bl_options = {'UNDO'}

    def execute(self, context):
        settings = context.scene.sweeper_settings
        if settings.enable_rename_objects_data:
            functions.rename_objects_data(mode=settings.options_rename_objects_data)
        if settings.enable_rename_images:
            functions.rename_images_to_filenames()
        if settings.enable_rename_materials_image_textures:
            functions.rename_materials_to_textures()
        if settings.enable_rename_collection_instances:
            functions.rename_collection_instances()
        if settings.enable_rename_worlds_env_textures:
            functions.rename_worlds_to_env_textures()
        return {'FINISHED'}


class AUTOREMOVE_OT_run_auto_remover(bpy.types.Operator):
    """Run the auto remover"""

    bl_idname = 'sweeper.autoremove_ot_run_auto_remover'
    bl_label = 'Auto Remove'
    bl_options = {'UNDO'}

    def execute(self, context):
        settings = context.scene.sweeper_settings
        if settings.enable_remove_unused_material_slots:
            functions.remove_unused_material_slots()
        if settings.enable_remove_vertex_groups:
            functions.clear_vertex_groups()
        if settings.enable_remove_custom_normals:
            functions.remove_custom_normals()
        return {'FINISHED'}


class UTILITIES_OT_select_unsubdivided(bpy.types.Operator):
    """Select all objects with a mesh data block and no subdivisions"""

    bl_idname = "sweeper.utilities_ot_select_unsubdivided"
    bl_label = "Select Unsubdivided"
    bl_options = {'REGISTER'}

    def execute(self, context):
        functions.select_unsubdivided(context)
        return {'FINISHED'}


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    AUTOREMOVE_OT_run_auto_remover,
    AUTORENAME_OT_run_auto_renamer,
    UTILITIES_OT_select_unsubdivided
])
