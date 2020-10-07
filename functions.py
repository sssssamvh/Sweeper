##############################################################################
# Imports
##############################################################################


import bpy
from pathlib import Path


##############################################################################
# Functions
##############################################################################


def clear_sharp():
    """Clear all sharp edges in meshes.\nOn selection or everything"""

    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH' and not ob.data.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.data.library]

    for ob in objects:
        for edge in ob.data.edges:
            if edge.use_edge_sharp:
                edge.use_edge_sharp = False


def clear_vertex_groups():
    """Delete all vertex groups.\nOn selection or everything"""

    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH' and not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.library]

    for ob in objects:
        ob.vertex_groups.clear()


def keyword_rename(self, context):
    for ob in [ob for ob in context.selected_objects if not ob.library]:
        ob.name = context.scene.sweeper_settings.rename_keyword
    return None


def remove_unused_material_slots():
    """Remove unused material slots from meshes and curves.\nOn selection or everything"""

    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH' and not ob.library and not ob.data.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.library and not ob.data.library]

    for ob in objects:
        if ob.type == 'MESH' or ob.type == 'CURVE':
            bpy.context.view_layer.objects.active = ob
            bpy.ops.object.material_slot_remove_unused()


def rename_images_to_filenames():
    """Auto-rename all images to their respective filename"""

    images = [image for image in bpy.data.images if not image.library and not image.name == 'Render Result']
    for image in images:
        image.name = Path(image.filepath).stem # Images are renamed to their filename, sans the extension


def rename_collection_instances():
    """Auto-rename the selected empties to the collection they instantiate.\nOn selection or everything"""

    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.instance_type == 'COLLECTION' and not ob.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.instance_type == 'COLLECTION' and not ob.library]

    for ob in objects:
        ob.name = ob.instance_collection.name


def rename_materials_to_textures():
    """Auto-rename all materials to the name of their first Image Texture node's datablock"""

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


def rename_objects_data(mode:str):
    """Auto-rename the selected objects to their data, or vice-versa.\nOn selection or everything"""

    def target_is_not_linked(ob:bpy.types.Object) -> bool:
        if mode == 'rename_objects_to_data':
            return not ob.library
        return not ob.data.library

    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.data and target_is_not_linked(ob)]
    else:
        objects = [ob for ob in bpy.data.objects if ob.data and target_is_not_linked(ob)]

    for ob in objects:
        if mode == 'rename_objects_to_data':
            ob.name = ob.data.name
        else:
            ob.data.name = ob.name


def remove_custom_normals():
    """Remove custom normals from all meshes.\nOn selection or everything"""

    if len(bpy.context.selected_objects) > 0:
        objects = [ob for ob in bpy.context.selected_objects if ob.type == 'MESH' and not ob.data.library]
    else:
        objects = [ob for ob in bpy.data.objects if ob.type == 'MESH' and not ob.data.library]

    for ob in objects:
        try:
            bpy.context.view_layer.objects.active = ob
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
        except RuntimeError:
            pass


def select_unsubdivided():
    """Select all objects with a mesh data block and no subdivisions"""

    objects = [ob for ob in bpy.context.scene.objects if ob.type == 'MESH' and not ob.library]

    bpy.ops.object.select_all(action = 'DESELECT')

    for ob in objects:
        has_enabled_subsurf_modifiers = False
        for mod in ob.modifiers:
            if mod.type == 'SUBSURF':
                has_enabled_subsurf_modifiers = mod.show_render and (mod.render_levels > 0 or ob.cycles.use_adaptive_subdivision)
                break
        if ob.name in bpy.context.view_layer.objects:
            ob.select_set(not has_enabled_subsurf_modifiers)
