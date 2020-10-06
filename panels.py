##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Panels
##############################################################################


class PROPERTIES_PT_sweeper(bpy.types.Panel):

    bl_idname = 'PROPERTIES_PT_sweeper'
    bl_label = 'Sweeper'
    bl_category = 'SamTools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        pass


class PROPERTIES_PT_renaming(bpy.types.Panel):

    bl_idname = 'PROPERTIES_PT_renaming'
    bl_label = 'Auto Rename'
    bl_parent_id = 'PROPERTIES_PT_sweeper'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True
        lay.prop(context.scene, 'sweeper_easy_rename')
        autorename = lay.column(align = True)
        autorename.scale_y = 1.5
        autorename.operator('sweeper.cleanup_ot_rename_objects_from_data', icon = 'OBJECT_DATA').data_from_objects = False
        autorename.operator('sweeper.cleanup_ot_rename_objects_from_data', text = 'Data From Objects', icon = 'MESH_DATA').data_from_objects = True
        autorename.separator()
        autorename.operator('sweeper.cleanup_ot_rename_images_from_filenames', icon = 'OUTLINER_OB_IMAGE')
        autorename.operator('sweeper.cleanup_ot_rename_materials_from_textures', icon = 'MATERIAL')
        autorename.separator()
        autorename.operator('sweeper.cleanup_ot_rename_instances_from_collections', icon = 'OUTLINER_OB_GROUP_INSTANCE')


class PROPERTIES_PT_removing(bpy.types.Panel):

    bl_idname = 'PROPERTIES_PT_removing'
    bl_label = 'Auto Remove'
    bl_parent_id = 'PROPERTIES_PT_sweeper'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True
        autoremove = lay.column(align = True)
        autoremove.scale_y = 1.5
        autoremove.operator('sweeper.cleanup_ot_remove_sharp_edges', icon = 'EDGESEL')
        autoremove.operator('sweeper.cleanup_ot_remove_unused_material_slots', icon = 'MATERIAL')
        autoremove.operator('sweeper.cleanup_ot_remove_vertex_groups', icon = 'GROUP_VERTEX')
        autoremove.operator('sweeper.cleanup_ot_remove_custom_normals', icon = 'GROUP_VERTEX')


##############################################################################
# Registration
##############################################################################


classes = [
    PROPERTIES_PT_sweeper,
    PROPERTIES_PT_renaming,
    PROPERTIES_PT_removing
]


def register():
    for class_to_register in classes:
        bpy.utils.register_class(class_to_register)


def unregister():
    for class_to_register in classes:
        bpy.utils.unregister_class(class_to_register)
