import os
import re
import bpy

# Unreal collision names, children named like this go into the object's fbx
COLLISION_PREFIXES = ("UBX_", "USP_", "UCP_", "UCX_")
# LOD levels are children named <object>_LOD1, _LOD2..., they go into the object's fbx,
# the object itself is level 0
LOD_NAME = re.compile(r"_LOD\d+$")
# what unparenting a child for the export changes on it
TRANSFORM = ("location", "rotation_euler", "rotation_quaternion", "rotation_axis_angle", "scale")


class UEExport2Unity_OT_Operator(bpy.types.Operator):
    bl_idname = "uehelper.export2unity"
    bl_label = "Export to unity"
    bl_description = "Export to unity"

    def execute(self, context):
        print("\n\nReady to go!\n")
        relative_path = context.scene.ue_helper_unity_export_path
        absolute_path = bpy.path.abspath(relative_path)
        export_path = os.path.normpath(absolute_path)
        if os.path.exists(export_path) is False:
            os.makedirs(export_path)

        # deselect all
        print("Deselecting objects")
        for obj in bpy.context.scene.objects:
            obj.select_set(state=False)

        print("Exporting objects")
        # export obj by obj
        for obj in bpy.context.scene.objects:
            if obj.type == "MESH":
                if obj.bfu_export_type == 'export_recursive':
                    export_suffix = obj.bfu_export_folder_name
                    export_subdir = export_path
                    if export_suffix != "SceneCollection":
                        export_subdir = os.path.join(export_path, export_suffix)

                    if os.path.exists(export_subdir) is False:
                        os.makedirs(export_subdir)

                    export_file = os.path.join(export_subdir, obj.name + '.fbx')

                    # make this object, its collision children and its LOD levels the only selected
                    obj.select_set(state=True)
                    bpy.context.view_layer.objects.active = obj
                    collisions = [child for child in obj.children if child.name[:4] in COLLISION_PREFIXES]
                    lods = [child for child in obj.children if LOD_NAME.search(child.name)]
                    for child in collisions + lods:
                        child.select_set(state=True)
                        if not child.select_get():
                            raise RuntimeError(child.name + " can't be selected (hidden?), it would be left out of the export")

                    # save and zero location
                    obj_location = obj.location.copy()
                    obj.location = (0.0, 0.0, 0.0)

                    # collisions go out without materials, Unity would list them as extra slots on the model
                    collision_materials = []
                    for child in collisions:
                        for slot in child.material_slots:
                            collision_materials.append((child, slot.slot_index, slot.material))
                    for child, index, material in collision_materials:
                        child.material_slots[index].material = None

                    # EXPORT!
                    print("Exporting ", obj.name, "to file", export_file)

                    # same switch BfU uses for the Unreal export, set on mark
                    colors_type = 'SRGB'
                    if obj.bfu_vertex_color_import_option == 'IGNORE':
                        colors_type = 'NONE'

                    # Unity's importer wants <name>_LOD0, _LOD1... next to each other, so with LOD levels
                    # the object goes out as level 0 and its children as its siblings
                    obj_name = obj.name
                    unparented = []
                    if lods:
                        obj.name = obj_name + "_LOD0"
                        bpy.context.view_layer.update()
                        for child in collisions + lods:
                            transform = {name: tuple(getattr(child, name)) for name in TRANSFORM}
                            unparented.append((child, child.matrix_parent_inverse.copy(), transform))
                            world = child.matrix_world.copy()
                            child.parent = None
                            child.matrix_world = world

                    bpy.ops.export_scene.fbx(filepath=export_file,
                                             check_existing=False,
                                             filter_glob="*.fbx",
                                             use_selection=True,
                                             bake_space_transform=True,
                                             object_types={'MESH'},
                                             colors_type=colors_type
                                             )

                    # make this object only selected, restore name, parenting, location and collision materials
                    obj.name = obj_name
                    for child, parent_inverse, transform in unparented:
                        child.parent = obj
                        child.matrix_parent_inverse = parent_inverse
                        for name, value in transform.items():
                            setattr(child, name, value)
                    obj.select_set(state=False)
                    for child in collisions + lods:
                        child.select_set(state=False)
                    obj.location = obj_location
                    for child, index, material in collision_materials:
                        child.material_slots[index].material = material

        return {'FINISHED'}
