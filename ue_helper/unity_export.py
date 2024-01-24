import os
import bpy


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

                    # make this object only selected
                    obj.select_set(state=True)
                    bpy.context.view_layer.objects.active = obj

                    # save and zero location
                    obj_location = obj.location.copy()
                    obj.location = (0.0, 0.0, 0.0)

                    # EXPORT!
                    print("Exporting ", obj.name, "to file", export_file)

                    bpy.ops.export_scene.fbx(filepath=export_file,
                                             check_existing=False,
                                             filter_glob="*.fbx",
                                             use_selection=True,
                                             bake_space_transform=True,
                                             object_types={'MESH'}
                                             )

                    # make this object only selected, restore location
                    obj.select_set(state=False)
                    obj.location = obj_location

        return {'FINISHED'}
