bl_info = {
    'name': 'Sweeper',
    'description': 'Auto-renaming and scene cleanup tools.',
    'author': 'Sam Van Hulle',
    'version': (0, 0, 3),
    'blender': (2, 90, 0),
    'location': 'View3D > UI',
    'category': 'Tools'
}


##############################################################################
# Imports
##############################################################################


import bpy
from . import properties, operators, panels, addon_updater_ops
modules = [properties, operators, panels]
from importlib import reload
for m in modules:
    reload(m)


##############################################################################
# Addon Preferences
##############################################################################


class SweeperAddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    data_type_armature: bpy.props.StringProperty(name='Armatures', default='RIG')
    data_type_camera: bpy.props.StringProperty(name='Cameras', default='CAM')
    data_type_collection: bpy.props.StringProperty(name='Collections', default='GRP')
    data_type_curve: bpy.props.StringProperty(name='Curves', default='CRV')
    data_type_empty: bpy.props.StringProperty(name='Empties', default='LOC')
    data_type_grease_pencil: bpy.props.StringProperty(name='Grease Pencil', default='GPL')
    data_type_lattice: bpy.props.StringProperty(name='Lattices', default='LAT')
    data_type_material: bpy.props.StringProperty(name='Materials', default='MAT')
    data_type_mesh: bpy.props.StringProperty(name='Meshes', default='GEO')
    data_type_text: bpy.props.StringProperty(name='Text', default='TXT')
    data_type_volume: bpy.props.StringProperty(name='Volumes', default='VOL')

    light_type_bounce: bpy.props.StringProperty(name='Bounce Lights', default='BNC')
    light_type_fill: bpy.props.StringProperty(name='Fill Lights', default='FIL')
    light_type_key: bpy.props.StringProperty(name='Key Lights', default='KEY')
    light_type_kick: bpy.props.StringProperty(name='Kick Lights', default='KCK')
    light_type_portal: bpy.props.StringProperty(name='Portals', default='PTL')
    light_type_rim: bpy.props.StringProperty(name='Rim Lights', default='RIM')
    light_type_spill: bpy.props.StringProperty(name='Spill Lights', default='SPL')
    light_type_volume: bpy.props.StringProperty(name='Volume Lights', default='VOL')

    light_type_bounce_triggers: bpy.props.StringProperty(name='on', default='bnc,bounce')
    light_type_fill_triggers: bpy.props.StringProperty(name='on', default='fil,fill')
    light_type_kick_triggers: bpy.props.StringProperty(name='on', default='kck,kick,kicker')
    light_type_key_triggers: bpy.props.StringProperty(name='on', default='key')
    light_type_portal_triggers: bpy.props.StringProperty(name='on', default='portal,ptl')
    light_type_rim_triggers: bpy.props.StringProperty(name='on', default='rim')
    light_type_spill_triggers: bpy.props.StringProperty(name='on', default='spl,spil,spill')
    light_type_volume_triggers: bpy.props.StringProperty(name='on', default='vol,volume,vll')

    show_rename_objects: bpy.props.BoolProperty(name='Object Renaming Acronyms', description='Show object data acronyms', default=False)
    show_rename_data: bpy.props.BoolProperty(name='Data Renaming Acronyms', description='Show data acronyms', default=False)
    show_rename_lights: bpy.props.BoolProperty(name='Light Renaming Acronyms', description='Show light role acronyms', default=False)

    auto_check_update: bpy.props.BoolProperty(name='Auto-check for Update', description='If enabled, auto-check for updates using an interval', default=False,)
    updater_intrval_months: bpy.props.IntProperty(name='Months', description='Number of months between checking for updates', default=0, min=0)
    updater_intrval_days: bpy.props.IntProperty(name='Days', description='Number of days between checking for updates', default=7, min=0, max=31)
    updater_intrval_hours: bpy.props.IntProperty(name='Hours', description='Number of hours between checking for updates', default=0, min=0, max=23)
    updater_intrval_minutes: bpy.props.IntProperty(name='Minutes', description='Number of minutes between checking for updates', default=0, min=0, max=59)

    def draw(self, context):
        lay = self.layout
        icon_rename_objects = 'TRIA_RIGHT' if not self.show_rename_objects else 'TRIA_DOWN'
        icon_rename_data = 'TRIA_RIGHT' if not self.show_rename_data else 'TRIA_DOWN'
        icon_rename_lights = 'TRIA_RIGHT' if not self.show_rename_lights else 'TRIA_DOWN'

        box = lay.box()
        box.prop(self, 'show_rename_objects', emboss=False, icon=icon_rename_objects)
        box.use_property_split = True
        if self.show_rename_objects:
            col = box.column(align=True)
            col.prop(self, 'data_type_armature')
            col.prop(self, 'data_type_camera')
            col.prop(self, 'data_type_curve')
            col.prop(self, 'data_type_empty')
            col.prop(self, 'data_type_grease_pencil')
            col.prop(self, 'data_type_lattice')
            col.prop(self, 'data_type_mesh')
            col.prop(self, 'data_type_text')
            col.prop(self, 'data_type_volume')

        box = lay.box()
        box.prop(self, 'show_rename_data', emboss=False, icon=icon_rename_data)
        box.use_property_split = True
        if self.show_rename_data:
            col = box.column(align=True)
            col.prop(self, 'data_type_collection')
            col.prop(self, 'data_type_material')

        box = lay.box()
        box.prop(self, 'show_rename_lights', emboss=False, icon=icon_rename_lights)
        box.use_property_split = True
        if self.show_rename_lights:
            col = box.column(align=True)
            col.prop(self, 'light_type_bounce')
            col.prop(self, 'light_type_bounce_triggers')
            col = box.column(align=True)
            col.prop(self, 'light_type_fill')
            col.prop(self, 'light_type_fill_triggers')
            col = box.column(align=True)
            col.prop(self, 'light_type_key')
            col.prop(self, 'light_type_key_triggers')
            col = box.column(align=True)
            col.prop(self, 'light_type_kick')
            col.prop(self, 'light_type_kick_triggers')
            col = box.column(align=True)
            col.prop(self, 'light_type_portal')
            col.prop(self, 'light_type_portal_triggers')
            col = box.column(align=True)
            col.prop(self, 'light_type_rim')
            col.prop(self, 'light_type_rim_triggers')
            col = box.column(align=True)
            col.prop(self, 'light_type_spill')
            col.prop(self, 'light_type_spill_triggers')
            col = box.column(align=True)
            col.prop(self, 'light_type_volume')
            col.prop(self, 'light_type_volume_triggers')

        addon_updater_ops.update_settings_ui(self, context)


##############################################################################
# Registration
##############################################################################


def register():
    addon_updater_ops.register(bl_info)
    bpy.utils.register_class(SweeperAddonPreferences)
    for module in modules:
        module.register()


def unregister():
    bpy.utils.unregister_class(SweeperAddonPreferences)
    for module in reversed(modules):
        module.unregister()
    addon_updater_ops.unregister()


if __name__ == '__main__':
    register()
