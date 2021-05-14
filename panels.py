##############################################################################
# Imports
##############################################################################


import bpy
from . import addon_updater_ops


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
        lay = self.layout
        addon_updater_ops.update_notice_box_ui(self, context)


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
        lay.label(text='Rename Selection To:')
        lay.prop(settings, 'rename_keyword', text='')
        lay.separator()
        lay.label(text='Auto Rename Everything:')
        box = lay.box()
        box.label(text='Apply Naming Conventions To:')
        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(settings, 'enable_rename_objects', icon='OBJECT_DATA')
        sub = row.column(align=True)
        sub.enabled = settings.enable_rename_objects
        sub.prop(settings, 'enable_rename_data', text='')
        col.prop(settings, 'enable_rename_collections', icon='GROUP')
        col.prop(settings, 'enable_rename_materials', icon='MATERIAL')
        box.label(text='Utilities:')
        col = box.column(align=True)
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
        lay.label(text='On selection or everything.')
        box = lay.box()
        col = box.column(align=True)
        col.prop(settings, 'enable_remove_custom_normals', icon='EDGESEL')
        col.prop(settings, 'enable_remove_unused_material_slots', icon='MATERIAL')
        col.prop(settings, 'enable_remove_uv_maps', icon='UV_DATA')
        col.prop(settings, 'enable_remove_vertex_groups', icon='GROUP_VERTEX')
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
        col = lay.column(align=True)
        col.operator('sweeper.utilities_ot_sort_collections_alphabetically', icon='OUTLINER')


##############################################################################
# Registration
##############################################################################


register, unregister = bpy.utils.register_classes_factory([
    VIEW3D_PT_sweeper,
    VIEW3D_PT_autorename,
    VIEW3D_PT_autoremove,
    VIEW3D_PT_utilities
])
