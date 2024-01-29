import bpy
from math import radians


# from https://blender.stackexchange.com/questions/146685/how-to-obtain-the-parent-of-a-collection-using-python

def get_parent_collection_names(collection, parent_names):
    for parent_collection in bpy.data.collections:
        if collection.name in parent_collection.children.keys():
            parent_names.append(parent_collection.name)
            get_parent_collection_names(parent_collection, parent_names)
            return


def turn_collection_hierarchy_into_path(obj):
    parent_collection = obj.users_collection[0]
    parent_names = [parent_collection.name]
    get_parent_collection_names(parent_collection, parent_names)
    parent_names.reverse()
    return '\\'.join(parent_names)


def mark_selected(for_export=True, context=None):
    z_rot = False
    lightmap_gen = False
    if context:
        z_rot = context.scene.ue_helper_rotate_z_setting
        lightmap_gen = context.scene.ue_helper_blender_gen_lightmap_uvs

    for obj in bpy.context.selected_objects:
        if for_export:
            obj.bfu_export_type = 'export_recursive'  # Set for export
            obj.bfu_export_folder_name = "".join(turn_collection_hierarchy_into_path(obj).split())
            if z_rot is True:
                obj.bfu_additional_rotation_for_export.z = radians(90)
            else:
                obj.bfu_additional_rotation_for_export.z = 0
        else:
            obj.bfu_export_type = 'auto'  # Set not for exporting


def generate_lightmap_uvs(context):
    lightmap_gen = False
    if context:
        lightmap_gen = context.scene.ue_helper_blender_gen_lightmap_uvs

    # Store current selection
    selected_objects = bpy.context.selected_objects
    old_active = bpy.context.view_layer.objects.active
    bpy.ops.object.select_all(action='DESELECT')

    # Iterate over selected objects
    for obj in selected_objects:
        if obj.type != 'MESH':
            continue
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if lightmap_gen is True:
            generate_lightmap_uvs_for_obj(obj)
            obj.bfu_generate_light_map_uvs = False
        else:
            mesh = obj.data
            if len(mesh.uv_layers) == 1:  # if it already had more than 1 UV map, don't mess with the setting
                obj.bfu_generate_light_map_uvs = True
        obj.select_set(False)

    # Restore selection
    bpy.context.view_layer.objects.active = old_active
    for obj in selected_objects:
        obj.select_set(True)


def generate_lightmap_uvs_for_obj(obj):
    # Check if the object is a mesh
    if obj.type != 'MESH':
        print("The object is not a mesh. Skipping uv lightmap generation.")
        return
    # Check if the object has more than one UV channel
    mesh = obj.data
    if len(mesh.uv_layers) == 1:
        # Create a new UV channel named "UVLightmap"
        mesh.uv_layers.new(name="UVLightmap")

        # Set the new UV channel as active
        mesh.uv_layers.active = mesh.uv_layers["UVLightmap"]

        # Generate lightmap UVs
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.uv.lightmap_pack(PREF_CONTEXT='ALL_FACES', PREF_PACK_IN_ONE=False, PREF_BOX_DIV=30, PREF_MARGIN_DIV=0.2)
        bpy.ops.object.mode_set(mode='OBJECT')

        # Reselect the original UV layer
        mesh.uv_layers[0].active = True
    else:
        print("The object has more than one UV channel or no UV channels.")
