# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import bpy
from bpy.props import BoolProperty, StringProperty

from .ue_helper_panel import UEHelper_PT_Panel
from .mark_op import UEMark_OT_Operator
from .unmark_op import UEUnmark_OT_Operator
from .unity_export import UEExport2Unity_OT_Operator

bl_info = {
    "name": "ue-helper",
    "author": "Vertex Machine @ Vertex Rage Studio",
    "description": "Simple helper addon for Blender For Unreal Engine addon",
    "blender": (4, 0, 0),
    "version": (0, 0, 6),
    "location": "View3D",
    "warning": "",
    "category": "Import-Export"
}

classes = (UEHelper_PT_Panel, UEMark_OT_Operator, UEUnmark_OT_Operator, UEExport2Unity_OT_Operator)


# register, unregister = bpy.utils.register_classes_factory(classes)

def register():
    bpy.types.Scene.ue_helper_rotate_z_setting = BoolProperty(
        name="Rotate Z",
        description="Rotate object in Z by 90 degrees?",
        default=False
    )

    bpy.types.Scene.ue_helper_blender_gen_lightmap_uvs = BoolProperty(
        name="Generate Lightmap UVs",
        description=(
            "Generate lightmap UVs for selected objects.\n"
            "Features:\n"
            "- Utilizes Blender's built-in lightmap UV generation with a quality setting of 30 and a margin of 0.2.\n"
            "- Toggles the 'Generate Lightmap UVs' option in BfU.\n"
            "- Effective only during the 'Mark for Export' process.\n"
            "- Adds a second UV map exclusively for objects with only one existing UV map"
        ),
        default=False
    )

    bpy.types.Scene.ue_helper_unity_export_path = StringProperty(
        name="Unity fbx export path",
        description="Where fbx files for unity should be put?",
        default="",
        subtype="DIR_PATH",
    )

    bpy.types.Scene.ue_helper_unity_expanded = BoolProperty(default=False)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.ue_helper_unity_expanded
    del bpy.types.Scene.ue_helper_unity_export_path
    del bpy.types.Scene.ue_helper_rotate_z_setting
