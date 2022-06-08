import bpy

from . utils import mark_selected

class UEUnmark_OT_Operator(bpy.types.Operator):
    bl_idname = "uehelper.unmark"
    bl_label = "Helper function for unmarking to export"
    bl_description = "Helper function for unmarking to export"


    def execute(self, context):
        mark_selected(False)
        return {'FINISHED'}