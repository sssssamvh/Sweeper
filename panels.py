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
    bl_label = 'Renaming'
    bl_parent_id = 'VIEW3D_PT_sweeper'
    bl_region_type = 'UI'
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        settings = context.scene.sweeper_settings
        lay = self.layout
        lay.use_property_decorate=False
        lay.label(text='Keyword Rename:')
        lay.prop(settings, 'rename_keyword', text='')
        lay.separator()
        lay.label(text='Auto Rename:')
        box = lay.box()
        box.label(text='Objects:')
        row = box.row(align=True)
        row.prop(settings, 'enable_rename_objects_data', text='')
        row.prop(settings, 'options_rename_objects_data', text='', icon='OBJECT_DATA')
        row.prop(settings, 'enable_apply_naming_conventions', text='', icon='WORDWRAP_ON')
        box.label(text='Others:')
        col = box.column(align=True)
        col.prop(settings, 'enable_rename_collection_instances', icon='OUTLINER_OB_GROUP_INSTANCE')
        col.prop(settings, 'enable_rename_images', icon='OUTLINER_OB_IMAGE')
        col.prop(settings, 'enable_rename_materials_image_textures', icon='MATERIAL')
        col.prop(settings, 'enable_rename_worlds_env_textures', icon='WORLD_DATA')
        row = box.row()
        row.scale_y = 1.5
        row.operator('sweeper.autorename_ot_run_auto_renamer', icon='PLAY')


class VIEW3D_PT_autoremove(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_autoremove'
    bl_label = 'Removing'
    bl_parent_id = 'VIEW3D_PT_sweeper'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        settings = context.scene.sweeper_settings
        lay = self.layout
        lay.label(text='Auto Remove:')
        box = lay.box()
        col = box.column(align=True)
        col.prop(settings, 'enable_remove_unused_material_slots', icon='MATERIAL')
        col.prop(settings, 'enable_remove_vertex_groups', icon='GROUP_VERTEX')
        col.prop(settings, 'enable_remove_custom_normals', icon='EDGESEL')
        row = box.row()
        row.scale_y = 1.5
        row.operator('sweeper.autoremove_ot_run_auto_remover', icon='PLAY')


class VIEW3D_PT_utilities(bpy.types.Panel):

    bl_idname = 'VIEW3D_PT_utilities'
    bl_label = 'Utilities'
    bl_parent_id = 'VIEW3D_PT_sweeper'
    bl_region_type = 'UI'
    bl_options = {'DEFAULT_CLOSED'}
    bl_space_type = 'VIEW_3D'

    def draw(self, context):
        lay = self.layout
        lay.use_property_split = True
        lay.operator('sweeper.utilities_ot_select_unsubdivided', icon='MOD_SUBSURF')


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    VIEW3D_PT_sweeper,
    VIEW3D_PT_autorename,
    VIEW3D_PT_autoremove
])
