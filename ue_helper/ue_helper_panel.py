import bpy

from . mark_op import UEMark_OT_Operator
from . unmark_op import UEUnmark_OT_Operator

class UEHelper_PT_Panel(bpy.types.Panel):
    bl_idname = "uehelper.main_panel"
    bl_label = "UE Helper"
    bl_category = "UE Helper"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_context = "objectmode"   
    
    def draw(self, context):
        layout = self.layout
        obj = context.object
        scene = context.scene

        layout.label(text="UE Export helpers:")
        col = layout.column(align=True)
        col.operator(UEMark_OT_Operator.bl_idname, text="Mark selected for export", icon="CONSOLE")
        col.operator(UEUnmark_OT_Operator.bl_idname, text="Unmark selected for export", icon="CONSOLE")

        layout.separator()
        layout.label(text="Options:")
        layout.prop(scene, "ue_helper_rotate_z_setting")