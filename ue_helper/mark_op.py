import bpy

from .utils import mark_selected, generate_lightmap_uvs


class UEMark_OT_Operator(bpy.types.Operator):
    bl_idname = "uehelper.mark"
    bl_label = "Helper function for marking to export"
    bl_description = "Helper function for marking to export"

    def execute(self, context):
        mark_selected(True, context)
        generate_lightmap_uvs(context)
        return {'FINISHED'}
