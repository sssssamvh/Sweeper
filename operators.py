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
    """Run the auto renamer.\nOn selection or everything"""

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


class AUTOREMOVE_OT_remove_sharp_edges(bpy.types.Operator):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    bl_idname = 'sweeper.autoremove_ot_remove_sharp_edges'
    bl_label = 'Sharp Edges'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.clear_sharp()
        return {'FINISHED'}


class AUTOREMOVE_OT_remove_vertex_groups(bpy.types.Operator):
    """Delete all vertex groups.\nOn selection or everything"""

    bl_idname = 'sweeper.autoremove_ot_remove_vertex_groups'
    bl_label = 'Vertex Groups'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.clear_vertex_groups()
        return {'FINISHED'}


class AUTOREMOVE_OT_remove_unused_material_slots(bpy.types.Operator):
    """Remove unused material slots from meshes and curves.\nOn selection or everything"""

    bl_idname = 'sweeper.autoremove_ot_remove_unused_material_slots'
    bl_label = 'Unused Material Slots'
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.remove_unused_material_slots()
        return {'FINISHED'}


class AUTOREMOVE_OT_remove_custom_normals(bpy.types.Operator):
    """Remove custom normals from all meshes"""

    bl_idname = 'sweeper.autoremove_ot_remove_custom_normals'
    bl_label = 'Custom Split Normals'
    bl_options = {'UNDO'}

    def execute(self, context):
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
    AUTOREMOVE_OT_remove_sharp_edges,
    AUTOREMOVE_OT_remove_vertex_groups,
    AUTOREMOVE_OT_remove_unused_material_slots,
    AUTOREMOVE_OT_remove_custom_normals,
    AUTORENAME_OT_run_auto_renamer,
    UTILITIES_OT_select_unsubdivided
])
