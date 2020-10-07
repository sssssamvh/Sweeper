##############################################################################
# Imports
##############################################################################


import bpy


##############################################################################
# Panels
##############################################################################


class VIEW3D_PT_sweeper(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_sweeper'
    bl_label = 'Sweeper'
    bl_category = 'SamTools'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'

    def draw(self, context):
        pass


class VIEW3D_PT_autorename(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_autorename'
    bl_label = 'Auto Rename'
    bl_parent_id = 'VIEW3D_PT_sweeper'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        settings = context.scene.sweeper_settings
        lay = self.layout
        lay.use_property_split = False
        lay.use_property_decorate = False
        lay.label(text='Keyword Rename:')
        lay.prop(settings, 'rename_keyword', text='')
        lay.separator()
        lay.label(text='Auto Rename:')
        autorename = lay.box()
        row = autorename.row()
        row.prop(settings, 'enable_rename_objects_data', text='')
        row.prop(settings, 'options_rename_objects_data', text='', icon = 'OBJECT_DATA')
        col = autorename.column(align=True)
        col.prop(settings, 'enable_rename_collection_instances', icon = 'OUTLINER_OB_GROUP_INSTANCE')
        col.prop(settings, 'enable_rename_images', icon = 'OUTLINER_OB_IMAGE', toggle=0, expand=True)
        col.prop(settings, 'enable_rename_materials_image_textures', icon = 'MATERIAL')
        row = autorename.row()
        row.scale_y = 1.5
        row.operator('sweeper.autorename_ot_run_auto_renamer')


class VIEW3D_PT_autoremove(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_autoremove'
    bl_label = 'Auto Remove'
    bl_parent_id = 'VIEW3D_PT_sweeper'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True
        autoremove = lay.column(align = True)
        autoremove.scale_y = 1.5
        autoremove.operator('sweeper.autoremove_ot_remove_sharp_edges', icon = 'EDGESEL')
        autoremove.operator('sweeper.autoremove_ot_remove_unused_material_slots', icon = 'MATERIAL')
        autoremove.operator('sweeper.autoremove_ot_remove_vertex_groups', icon = 'GROUP_VERTEX')
        autoremove.operator('sweeper.autoremove_ot_remove_custom_normals', icon = 'GROUP_VERTEX')


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    VIEW3D_PT_sweeper,
    VIEW3D_PT_autorename,
    VIEW3D_PT_autoremove
])
