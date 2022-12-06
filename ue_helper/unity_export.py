import bpy
import os
import mathutils

class UEExport2Unity_OT_Operator(bpy.types.Operator):
    bl_idname = "uehelper.export2unity"
    bl_label = "Export to unity"
    bl_description = "Export to unity"


    def execute(self, context):
        print("\n\nReady to go!\n")
        export_path = context.scene.ue_helper_unity_export_path
        if os.path.exists(export_path) == False:
            os.makedirs(export_path)

        # deselect all
        print("Deselecting objects")
        for obj in bpy.context.scene.objects: obj.select_set(state=False)

        print("Exporting objects")
        # export obj by obj
        for obj in bpy.context.scene.objects:
            if obj.type == "MESH":
                if obj.ExportEnum == 'export_recursive':
                    export_suffix = obj.exportFolderName
                    export_subdir = export_path
                    if export_suffix != "SceneCollection":
                        export_subdir = os.path.join(export_path, export_suffix)
                    
                    if os.path.exists(export_subdir) == False:
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

                    # make this object only selected, restor location
                    obj.select_set(state=False)
                    obj.location = obj_location

        
        return {'FINISHED'}



#bpy.ops.export_scene.fbx(filepath="", check_existing=True, filter_glob="*.fbx", use_selection=False, use_visible=False, use_active_collection=False, global_scale=1, apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', use_space_transform=True, bake_space_transform=False, object_types={'EMPTY', 'CAMERA', 'LIGHT', 'ARMATURE', 'MESH', 'OTHER'}, use_mesh_modifiers=True, use_mesh_modifiers_render=True, mesh_smooth_type='OFF', use_subsurf=False, use_mesh_edges=False, use_tspace=False, use_triangles=False, use_custom_props=False, add_leaf_bones=True, primary_bone_axis='Y', secondary_bone_axis='X', use_armature_deform_only=False, armature_nodetype='NULL', bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=True, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1, bake_anim_simplify_factor=1, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True, axis_forward='-Z', axis_up='Y')