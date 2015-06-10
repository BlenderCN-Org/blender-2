import bpy, bmesh, mathutils, time
from bpy.props import BoolProperty, IntProperty, FloatProperty, EnumProperty
from collections import defaultdict
from math import radians, hypot


class yzk_uvtools(bpy.types.Panel):
    bl_space_type = 'IMAGE_EDITOR'
    bl_region_type = 'TOOLS'
    bl_category = "yzk"
    bl_label = "yzk_uvtools"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("uv.select_all",text='deselect_all').action="TOGGLE"
        
        col = layout.column(align=True)
        col.operator("uv.unwrap")
        col.operator("uv.smart_project")
        col.operator("uv.lightmap_pack")
        col.operator("uv.follow_active_quads")
        
        col = layout.column(align=True)
        row = col.row(align=True)
        props=row.operator("transform.mirror",text='Mirror_X')
        props.constraint_axis=(True, False, False)
        props=row.operator("transform.mirror",text='Mirror_Y')
        props.constraint_axis=(False, True, False)
        
        col = layout.column(align=True)
        row = col.row(align=True)
        props=row.operator("transform.rotate",text='orientL')
        props.value=0.7854
        props.axis=(-0, -0, 1)
        props=row.operator("transform.rotate",text='orientR')
        props.value=0.7854
        props.axis=(-0, -0, -1)

def register():
    bpy.utils.register_class(yzk_uvtools)

def unregister():
    bpy.utils.unregister_class(yzk_uvtools)


if __name__ == "__main__":
    register()
