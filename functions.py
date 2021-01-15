##############################################################################
# Imports
##############################################################################


import bpy
from pathlib import Path
import re


##############################################################################
# Functions
##############################################################################


def keyword_rename(self, context):
    settings = context.scene.sweeper_settings
    for ob in [ob for ob in context.selected_objects if not ob.library]:
        ob.name = naming_conventionify(original_name=settings.rename_keyword, data_type=ob.type)
        if not ob.data.library:
            ob.data.name = ob.name
    return None


def addon_prefs():
    return bpy.context.preferences.addons['Sweeper'].preferences


def is_datablock_linked(datablock:bpy.types.ID) -> bool:
    return datablock.library or datablock.override_library


def acronym_by_data_type(data_type:str):
    ap = addon_prefs()
    acronyms = {
        'ARMATURE': ap.data_type_armature,
        'CAMERA': ap.data_type_camera,
        'COLLECTION': ap.data_type_collection,
        'CURVE': ap.data_type_curve,
        'EMPTY': ap.data_type_empty,
        'GPENCIL': ap.data_type_grease_pencil,
        'LATTICE': ap.data_type_lattice,
        'MATERIAL': ap.data_type_material,
        'MESH': ap.data_type_mesh,
        'FONT': ap.data_type_text,
        'VOLUME': ap.data_type_volume
    }
    if data_type in acronyms.keys():
        return acronyms[data_type]
    return None


def acronym_by_light_name(light_name:str):
    ap = addon_prefs()
    light_roles = {}
    light_roles[ap.light_type_bounce]   = re.split('\W+', ap.light_type_bounce_triggers)
    light_roles[ap.light_type_fill]     = re.split('\W+', ap.light_type_fill_triggers)
    light_roles[ap.light_type_kick]     = re.split('\W+', ap.light_type_kick_triggers)
    light_roles[ap.light_type_portal]   = re.split('\W+', ap.light_type_portal_triggers)
    light_roles[ap.light_type_rim]      = re.split('\W+', ap.light_type_rim_triggers)
    light_roles[ap.light_type_spill]    = re.split('\W+', ap.light_type_spill_triggers)
    light_roles[ap.light_type_volume]   = re.split('\W+', ap.light_type_volume_triggers)
    for acronym, triggers in light_roles.items():
        for trigger in triggers:
            if trigger.lower() in light_name.lower():
                return acronym
    return 'LGT'


def naming_conventionify(original_name:str, data_type:str) -> str:
    keyword = ''.join([c for c in re.split('\W+', original_name)[0] if c.isalpha()])
    keyword = keyword[:1].lower() + keyword[1:]
    acronym = None
    if data_type == 'LIGHT':
        acronym = acronym_by_light_name(light_name=original_name)
    else:
        acronym = acronym_by_data_type(data_type=data_type)
    if not acronym:
        acronym = 'OBJ'
    return f'{keyword}.{acronym}.001'


def rename_objects(mode:str):
    # Object renaming starts here
    objects = [obj for obj in bpy.data.objects if not is_datablock_linked(obj)]
    for obj in objects:
        # If it's a collection instance, rename to the collection
        if obj.instance_collection:
            obj.name = obj.instance_collection.name
            continue
        # If not, the acronym is up to naming_conventionify
        if mode == 'and_data': # rename data to object
            obj.name = naming_conventionify(original_name=obj.name, data_type=obj.type)
            if obj.data:
                if not is_datablock_linked(obj.data):
                    obj.data.name = obj.name
        else: # rename object to data
            if obj.data:
                if not is_datablock_linked(obj.data):
                    obj.data.name = naming_conventionify(original_name=obj.data.name, data_type=obj.type)
                    obj.name = obj.data.name


def rename_collections():
    collections = [coll for coll in bpy.data.collections if not is_datablock_linked(coll)]
    for coll in collections:
        coll.name = naming_conventionify(original_name=coll.name, data_type='COLLECTION')


def rename_materials():
    materials = [mat for mat in bpy.data.materials if not is_datablock_linked(mat)]
    for mat in materials:
        mat.name = naming_conventionify(original_name=mat.name, data_type='MATERIAL')


def rename_images_to_filenames():
    images = [image for image in bpy.data.images if not image.library and not image.name == 'Render Result']
    for image in images:
        # Images are renamed to their filename, sans the extension
        image.name = Path(image.filepath).stem


def rename_materials_to_textures():
    materials = [mat for mat in bpy.data.materials if not mat.library]
    for mat in materials:
        first_image_texture = None
        for node in mat.node_tree.nodes:
            if node.bl_idname == 'ShaderNodeTexImage':
                if node.image:
                    first_image_texture = node
                    break
        if first_image_texture:
            mat.name = first_image_texture.image.name


def rename_worlds_to_env_textures():
    worlds = [world for world in bpy.data.worlds if not world.library]
    for world in worlds:
        first_env_texture = None
        if world.node_tree:
            for node in world.node_tree.nodes:
                if node.bl_idname == 'ShaderNodeTexEnvironment':
                    if node.image:
                        first_env_texture = node
                        break
            if first_env_texture:
                world.name = first_env_texture.image.name


def remove_vertex_groups():
    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH' and not is_datablock_linked(ob)]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not is_datablock_linked(ob)]
    for ob in objects:
        ob.vertex_groups.clear()


def remove_unused_material_slots():
    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH' and not is_datablock_linked(ob) and not is_datablock_linked(ob.data)]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not is_datablock_linked(ob) and not is_datablock_linked(ob.data)]
    for ob in objects:
        if ob.type == 'MESH' or ob.type == 'CURVE':
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.material_slot_remove_unused()


def remove_custom_normals():
    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH' and not is_datablock_linked(ob.data)]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not is_datablock_linked(ob.data)]
    for ob in objects:
        ob.data.use_auto_smooth = False
        for edge in ob.data.edges:
            if edge.use_edge_sharp:
                edge.use_edge_sharp = False
        try:
            bpy.context.view_layer.objects.active = ob
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        except RuntimeError:
            pass


def remove_uv_maps():
    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH' and not is_datablock_linked(ob.data)]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not is_datablock_linked(ob.data)]
    for ob in objects:
        for uv_map in ob.data.uv_layers:
            ob.data.uv_layers.remove(uv_map)


def select_unsubdivided():
    objects = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and not is_datablock_linked(ob)]
    bpy.ops.object.select_all(action = 'DESELECT')
    for ob in objects:
        has_enabled_subsurf_modifiers = False
        for mod in ob.modifiers:
            if mod.type == 'SUBSURF':
                has_enabled_subsurf_modifiers = mod.show_render and (mod.render_levels > 0 or ob.cycles.use_adaptive_subdivision)
                break
        if ob.name in bpy.context.view_layer.objects:
            ob.select_set(not has_enabled_subsurf_modifiers)
