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


class CLEANUP_OT_remove_sharp_edges(bpy.types.Operator):
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    bl_idname = "sweeper.cleanup_ot_remove_sharp_edges"
    bl_label = "Sharp Edges"
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.clear_sharp()
        return {'FINISHED'}


class CLEANUP_OT_remove_vertex_groups(bpy.types.Operator):
    """Delete all vertex groups.\nOn selection or everything"""

    bl_idname = "sweeper.cleanup_ot_remove_vertex_groups"
    bl_label = "Vertex Groups"
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.clear_vertex_groups()
        return {'FINISHED'}


class CLEANUP_OT_remove_unused_material_slots(bpy.types.Operator):
    """Remove unused material slots from meshes and curves.\nOn selection or everything"""

    bl_idname = "sweeper.cleanup_ot_remove_unused_material_slots"
    bl_label = "Unused Material Slots"
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.remove_unused_material_slots()
        return {'FINISHED'}


class CLEANUP_OT_rename_objects_from_data(bpy.types.Operator):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    bl_idname = "sweeper.cleanup_ot_rename_objects_from_data"
    bl_label = "Objects From Data"
    bl_options = {'UNDO'}

    data_from_objects : bpy.props.BoolProperty(name = "Data From Objects", default = False)

    def execute(self, context):
        functions.rename_objects_from_data(data_from_objects = self.data_from_objects)
        return {'FINISHED'}


class CLEANUP_OT_rename_instances_from_collections(bpy.types.Operator):
    """Auto-rename the selected empties to the collection they instance.\nOn selection or everything"""

    bl_idname = "sweeper.cleanup_ot_rename_instances_from_collections"
    bl_label = "Instances From Collections"
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.rename_instances_from_collections()
        return {'FINISHED'}


class CLEANUP_OT_rename_materials_from_textures(bpy.types.Operator):
    """Auto-rename all materials to the name of their first Image Texture node's datablock"""

    bl_idname = "sweeper.cleanup_ot_rename_materials_from_textures"
    bl_label = "Materials From Image Textures"
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.rename_materials_from_textures()
        return {'FINISHED'}


class CLEANUP_OT_rename_images_from_filenames(bpy.types.Operator):
    """Auto-rename all images to their respective filename"""

    bl_idname = "sweeper.cleanup_ot_rename_images_from_filenames"
    bl_label = "Images From Filenames"
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.rename_images_from_filenames()
        return {'FINISHED'}


class CLEANUP_OT_remove_custom_normals(bpy.types.Operator):
    """Remove custom normals from all meshes"""

    bl_idname = "sweeper.cleanup_ot_remove_custom_normals"
    bl_label = "Custom Split Normals"
    bl_options = {'UNDO'}

    def execute(self, context):
        functions.remove_custom_normals()
        return {'FINISHED'}





##############################################################################
# Registration
##############################################################################


classes = [
    CLEANUP_OT_remove_sharp_edges,
    CLEANUP_OT_remove_vertex_groups,
    CLEANUP_OT_remove_unused_material_slots,
    CLEANUP_OT_rename_images_from_filenames,
    CLEANUP_OT_rename_instances_from_collections,
    CLEANUP_OT_rename_materials_from_textures,
    CLEANUP_OT_rename_objects_from_data,
    CLEANUP_OT_remove_custom_normals
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)
    bpy.types.Scene.sweeper_easy_rename = bpy.props.StringProperty(name = "Batch Rename", default = "", update = functions.easy_rename, options = {'SKIP_SAVE'})


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
    del bpy.types.Scene.sweeper_easy_rename
