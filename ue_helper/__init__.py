# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "ue-helper",
    "author" : "Vertex Machine @ Vertex Rage Studio",
    "description" : "Simple helper addon for Blender For Unreal Engine addon",
    "blender" : (3, 2, 0),
    "version" : (0, 0, 2),
    "location" : "View3D",
    "warning" : "",
    "category" : "Import-Export"
}

import bpy
from bpy.props import BoolProperty

from . ue_helper_panel import UEHelper_PT_Panel
from . mark_op import UEMark_OT_Operator
from . unmark_op import UEUnmark_OT_Operator

classes = (UEHelper_PT_Panel, UEMark_OT_Operator, UEUnmark_OT_Operator)

#register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    bpy.types.Scene.ue_helper_rotate_z_setting = BoolProperty(
        name = "Rotate Z",
        description = "Rotate object in Z by 90 degrees?",
        default=False
    )
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.ue_helper_rotate_z_setting