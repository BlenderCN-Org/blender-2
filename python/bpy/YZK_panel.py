bl_info = {
  "name": "yzk_Custom Menu",
  "category": "3D View",
  "author":"yzk"
  }

import bpy
from itertools import chain #yzk_select_handle
import zipfile, urllib.request, os, sys, re #yzk_update_addon

class yzk_CustomPanel1(bpy.types.Panel):
	"""Creates a Panel in the Object properties window"""
	bl_label = "PopupWindow"
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'TOOLS'
	bl_category = "yzk"
	bl_idname = "yzk_yzk_CustomPanel1"
	#bl_region_type = 'WINDOW'
	#bl_context = "object"

	def draw(self, context):
		layout = self.layout
		col = layout.column(align=True)
		col.operator("yzk.yzk_update_addon", text="yzk_update_addon")
		col.operator("yzk.yzk_popup_window", text="duplicateWindow", icon='INFO').areaType="INFO"
		row = col.row(align=True)
		row.operator("yzk.yzk_popup_window", text="python", icon='CONSOLE').areaType="CONSOLE"
		row.operator("yzk.yzk_popup_window", text="text", icon='TEXT').areaType="TEXT_EDITOR"
		row.operator("yzk.yzk_popup_window", text="user", icon='PREFERENCES').areaType="USER_PREFERENCES"

		col = layout.column(align=True)
		row = col.row(align=True)
		row.operator("view3d.view_persportho",text='pers/orth', icon='CAMERA_DATA')
		row.operator("view3d.view_all", text="focus", icon='BBOX')

		row = col.row(align=True)
		row.operator("object.shade_smooth", text="Smooth")
		row.operator("object.shade_flat", text="Flat")

		col = layout.column(align=True)
		obj = bpy.context.object
		
		if obj is not None and obj.type == 'MESH' and obj.mode == "EDIT":
			col.operator("mesh.reveal",text='UnHide_all')
		else:
			col.operator("object.hide_view_clear",text='UnHide_all ')
			col.operator("view3d.snap_mesh_view")


class yzk_CustomPanel2(bpy.types.Panel):
    bl_label = "addPrimitive"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "yzk"

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.menu("INFO_MT_add",text='Add', icon='OBJECT_DATA')

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.primitive_cube_add", text='cube', icon='MESH_CUBE')
        row.operator("mesh.primitive_cylinder_add", text='cylinder', icon='MESH_CYLINDER')
        row.operator("mesh.primitive_uv_sphere_add",text='sphere', icon='MESH_UVSPHERE')
        col.operator("yzk.yzk_curve_new", text="null curve", icon="CURVE_BEZCURVE")

class yzk_tools_panel(bpy.types.Panel):
    bl_label = "tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "yzk"

    def draw(self, context):
        layout = self.layout

        obj = context.active_object
        if obj is not None and obj.mode == "OBJECT":
            col = layout.column(align=True)
            col.menu("VIEW3D_MT_object", icon="OBJECT_DATAMODE")
        elif obj is not None and obj.mode == "EDIT":
            if obj.type == 'MESH':
                col = layout.column(align=True)
                col.menu("VIEW3D_MT_edit_mesh",icon="EDITMODE_HLT")
            elif obj.type == 'CURVE':
                col = layout.column(align=True)
                col.menu("VIEW3D_MT_edit_curve",icon="OUTLINER_OB_CURVE")
            else:
                layout.label(text="Active obj: unknownType")
        else:
            layout.label(text="Active obj: None")

        if obj is not None and obj.mode == "OBJECT":
                col = layout.column(align=True)
                col.menu("VIEW3D_MT_transform_object", icon="MANIPUL")
                col.operator("object.location_clear", text="reset Transform")
                col.operator("object.rotation_clear", text="reset Rotation")
                col.operator("object.scale_clear", text="reset Scale")

                row = col.row(align=True)
                row.operator("object.origin_set", text="center").type='ORIGIN_CENTER_OF_MASS'
                props = row.operator("object.transform_apply" ,text="freeze")
                props.location=True
                props.rotation=True
                props.scale=True

                col = layout.column(align=True)
                row = layout.row(align=True)
                row.operator("object.select_all").action='DESELECT'
                row.operator("object.select_grouped").type='GROUP'
                row = layout.row(align=True)
                row.operator("object.join", text="join")
                row.operator("mesh.separate").type='LOOSE'

                #col = layout.column(align=True)
                #col.operator("object.parent_clear",text='parent_clear').type='CLEAR'

                col = layout.column(align=True)
                row = col.row(align=True)
                row.operator("yzk.yzk_duplicate", text="duplicate")
                row.operator("yzk.yzk_instance", text="instance")

                if obj.type=='MESH':
                    col = layout.column(align=True)
                    col.operator("object.modifier_add",text='modifier', icon='MODIFIER')
                    row = col.row(align=True)
                    row.operator("object.modifier_add",text='mirror', icon='MOD_MIRROR').type='MIRROR'
                    row.operator("object.modifier_add",text='array', icon='MOD_ARRAY').type='ARRAY'
                    row = col.row(align=True)
                    row.operator("object.modifier_add",text='bevel', icon='MOD_BEVEL').type='BEVEL'
                    row.operator("object.modifier_add",text='subsurf', icon='MOD_SUBSURF').type='SUBSURF'

                    col = layout.column(align=True)
                    col.operator("object.convert",text="convert to curve").target='CURVE'

                elif obj.type=='CURVE':
                    col = layout.column(align=True)
                    col.operator("object.convert",text="convert to mesh").target='MESH'

        if obj is not None and obj.mode == "EDIT":
            #obj.type in {'MESH', 'CURVE', 'SURFACE','META','FONT','ARMATURE','LATTICE'}:
            col = layout.column(align=True)
            row = col.row(align=True)
            props = row.operator("transform.resize", text="alignX", icon="MANIPUL")
            props.value = (0,0,0)
            props.constraint_axis=(True, False, False)
            props = row.operator("transform.resize", text="alignY")
            props.value = (0,0,0)
            props.constraint_axis=(False, True, False)
            props = row.operator("transform.resize", text="alignZ")
            props.value = (0,0,0)
            props.constraint_axis=(False, False, True)

            if obj.type == 'MESH':
                col = layout.column(align=True)
                col.operator("mesh.flip_normals")

                col = layout.column(align=True)
                col.menu("VIEW3D_MT_edit_mesh_vertices", text='vertex', icon='VERTEXSEL')
                #col.operator_menu_enum("mesh.merge", "type")
                #col.operator("mesh.merge", text="mergeVertex").type='CENTER'
                col.operator("yzk.yzk_3dcursor", text="pivotToSelected")
                col.operator("mesh.remove_doubles")

                col = layout.column(align=True)
                col.menu("VIEW3D_MT_edit_mesh_edges", text='edge', icon='EDGESEL')
                #col.operator("mesh.loop_multi_select",text='edge_loop')
                row = col.row(align=True)
                row.operator("yzk.yzk_edge_hard",text='hard_edge')
                row.operator("yzk.yzk_edge_soft",text='soft_edge')
                row = col.row(align=True)
                props = row.operator("mesh.knife_tool",text='KnifeTool')
                props.use_occlude_geometry = True
                props.only_selected = False
                props = row.operator("mesh.knife_tool",text='KnifeThrough')
                props.use_occlude_geometry = False
                props.only_selected = False
                row = col.row(align=True)
                props = row.operator("mesh.bevel", text='bevel' )
                props.offset_type = "WIDTH"
                props.offset = 1
                props.segments = 1
                props.profile = 1
                props = row.operator("mesh.bevel", text='round' )
                props.offset_type = "WIDTH"
                props.offset = 1
                props.segments = 2
                props.profile = 1
                props = row.operator("mesh.bevel", text='filet' )
                props.offset_type = "WIDTH"
                props.offset = 1
                props.segments = 2
                props.profile = 0.15
                col.operator("mesh.bisect",text='slash')
                col.operator("mesh.edge_face_add",text='Fill')
                row = col.row(align=True)
                row.operator("mesh.subdivide")
                row.operator("mesh.unsubdivide")
                col = layout.column(align=True)
                col.menu("VIEW3D_MT_edit_mesh_faces", text='face', icon='FACESEL')
                col.operator("mesh.loopcut_slide")
                col.operator("mesh.edge_split",text='edge_split')
                col.operator("mesh.inset")
                row = col.row(align=True)
                row.operator("view3d.edit_mesh_extrude_move_normal", text="Extrude")
                row.operator("view3d.edit_mesh_extrude_individual_move", text="Extrude Individual")

                col = layout.column(align=True)
                col.menu("VIEW3D_MT_edit_mesh_delete")
                col.operator("yzk.yzk_delete")
                col.operator("mesh.dissolve_limited",text='delete_dissolve').angle_limit=180

            elif obj.type == 'CURVE':
                col = layout.column(align=True)
                row = col.row(align=True)
                row.operator("curve.spline_type_set", text="poly", icon="IPO_CONSTANT").type='POLY'
                row.operator("curve.spline_type_set", text="bezier", icon="CURVE_BEZCURVE").type='BEZIER'
                row.operator("curve.spline_type_set", text="nurbs", icon="CURVE_NCURVE").type='NURBS'
                row = col.row(align=True)
                row.operator("yzk.yzk_curve_dimensions", text="2D/3D")
                row.operator("curve.cyclic_toggle", text="close")
                row = col.row(align=True)
                row.operator("curve.switch_direction")
                row.operator("curve.make_segment")
                col.operator("curve.radius_set")

                col = layout.column(align=True)
                col.label(text="Handles:")
                row = col.row(align=True)
                row.operator("yzk.yzk_set_handle", text="Auto").type = 'AUTOMATIC'
                row.operator("yzk.yzk_set_handle", text="Vector").type = 'VECTOR'
                row = col.row(align=True)
                row.operator("yzk.yzk_set_handle", text="Align").type = 'ALIGNED'
                row.operator("yzk.yzk_set_handle", text="Free").type = 'FREE_ALIGN'
                col.operator("yzk.yzk_select_handle", text="getHandle")

                col = layout.column(align=True)
                col.label(text="Modeling:")
                col.operator("curve.extrude_move", text="Extrude")
                col.operator("curve.subdivide")
                col.operator("curve.smooth")
                col.operator("object.vertex_random")
                col.operator("curve.normals_make_consistent")


class yzk_CustomPanel5(bpy.types.Panel):
    bl_label = "show/hide"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "yzk"

    def draw(self, context):
        layout = self.layout

        obj = bpy.context.object
        if obj is not None and obj.type == 'MESH' and obj.mode == "EDIT":
            col = layout.column(align=True)
            col.menu("VIEW3D_MT_edit_mesh_showhide")
            col.operator("mesh.reveal",text='Show_all (Shift+A)')
            col.operator("mesh.hide",text='Hide_selected (Ctrl+H)').unselected=False
            col.operator("mesh.hide",text='Hide_Unselected (Alt+H)').unselected=True
        else:
            col = layout.column(align=True)
            col.menu("Show/Hide")
            col.menu("VIEW3D_MT_object_showhide")
            col.operator("object.hide_view_clear",text='Show_all (Shift+A)')
            col.operator("object.hide_view_set",text='Hide_selected (Ctrl+H)').unselected=False
            col.operator("object.hide_view_set",text='Hide_Unselected (Alt+H)').unselected=True

class yzk2_CustomPanel1(bpy.types.Panel):
    bl_label = "oldTools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "old"

    def draw(self, context):
        layout = self.layout

        obj = bpy.context.object
        layout.label(text="modeSelect")
        col = layout.column(align=True)
        col.operator("object.mode_set", text='objectMode', icon='OBJECT_DATAMODE').mode='OBJECT'
        col.operator("object.mode_set", text='editMode', icon='EDITMODE_HLT').mode='EDIT'

        layout.label(text="callMenu")
        col = layout.column(align=True)
        col.operator("wm.call_menu").name='INFO_MT_add'
        col.operator("wm.call_menu",text='addMeshMenu').name="INFO_MT_mesh_add"
        col.operator("wm.call_menu",text='addCurveMenu', icon='OUTLINER_OB_CURVE').name="INFO_MT_curve_add"
        col.operator("wm.call_menu",text='addSurfaceMenu', icon='OUTLINER_OB_SURFACE').name="INFO_MT_surface_add"
        col.operator("object.metaball_add",text='metaBall', icon='OUTLINER_OB_META')
        col.operator("object.text_add",text='addTextMenu', icon='OUTLINER_OB_FONT')
        col.operator("object.add",text='addLatticeMenu', icon='OUTLINER_OB_LATTICE').type='LATTICE'
        col.operator("wm.call_menu",text='addArmatureMenu', icon='OUTLINER_OB_ARMATURE').name="INFO_MT_armature_add"
        col.operator("object.empty_add",text='addEmptyMenu', icon='OUTLINER_OB_EMPTY')
        col.operator("object.lamp_add",text="addLampMenu", icon='OUTLINER_OB_LAMP')

        layout.label(text="addPrimitive")
        col = layout.column(align=True)
        col.menu("INFO_MT_add")
        col.menu("INFO_MT_mesh_add")
        row = col.row(align=True)
        row.operator("mesh.primitive_cube_add", text='cube', icon='MESH_CUBE')
        row.operator("mesh.primitive_cylinder_add", text='cylinder', icon='MESH_CYLINDER')
        row = col.row(align=True)
        row.operator("mesh.primitive_uv_sphere_add",text='sphere', icon='MESH_UVSPHERE')

        col.menu("INFO_MT_metaball_add")
        row = col.row(align=True)
        row.operator("object.metaball_add",text='metaBall', icon='META_BALL').type='BALL'
        row.operator("object.metaball_add",text='metaBall', icon='META_ELLIPSOID').type='ELLIPSOID'

        col.menu("INFO_MT_curve_add")
        row = col.row(align=True)
        row.operator("curve.primitive_nurbs_path_add", text='path',icon='CURVE_PATH')
        row.operator("curve.primitive_nurbs_circle_add",text='circle', icon='CURVE_NCIRCLE')

        row = layout.row(align=True)
        row.menu("INFO_MT_mesh_add")
        row.menu("INFO_MT_curve_add")
        row.operator("wm.call_menu",text="surfaceMenu", icon='OUTLINER_OB_SURFACE').name="INFO_MT_surface_add"
        row.menu("OUTLINER_OB_META")
        row.operator("object.text_add",text='textMenu', icon='OUTLINER_OB_FONT')
        row.operator("object.add",text='latticeMenu', icon='OUTLINER_OB_LATTICE').type='LATTICE'
        row.operator("wm.call_menu",text='armatureMenu', icon='OUTLINER_OB_ARMATURE').name="INFO_MT_armature_add"
        row.operator("object.empty_add",text='emptyMenu', icon='OUTLINER_OB_EMPTY')
        row.operator("object.lamp_add",text="lampMenu", icon='OUTLINER_OB_LAMP')

class yzk_popup_window(bpy.types.Operator):
    bl_idname = "yzk.yzk_popup_window"
    bl_label = "yzk_popup_window"
    areaType = bpy.props.StringProperty()

    def execute(self, context):
        currentAreaType = bpy.context.area.type
        bpy.context.area.type = self.areaType
        bpy.ops.screen.area_dupli('INVOKE_DEFAULT')
        bpy.context.area.type = currentAreaType
        return {'FINISHED'}

class yzk_select_edit_mode(bpy.types.Operator):
    bl_idname = "yzk.yzk_select_edit_mode"
    bl_label = "yzk_select_edit_mode"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        if bpy.context.object.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.wm.context_set_value(data_path="tool_settings.mesh_select_mode", value=self.editType)
        return {'FINISHED'}

class yzk_object_mode(bpy.types.Operator):
    bl_idname = "yzk.yzk_object_mode"
    bl_label = "yzk_object_mode"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        obj = bpy.context.object
        if obj is not None and obj.type in {'MESH', 'CURVE', 'SURFACE','META','FONT','ARMATURE','LATTICE'}:
            if obj.mode == 'OBJECT':
                bpy.ops.object.mode_set(mode='EDIT')
            elif obj.mode == 'EDIT':
                bpy.ops.object.mode_set(mode='OBJECT')
        return {'FINISHED'}

class yzk_delete(bpy.types.Operator):
    bl_idname = "yzk.yzk_delete"
    bl_label = "yzk_delete"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        obj = bpy.context.object
        if obj.mode == 'OBJECT':
            bpy.ops.object.delete()
        elif obj.mode == 'EDIT':
            if bpy.context.tool_settings.mesh_select_mode[0] == True: #vertex
                bpy.ops.mesh.delete(type='VERT')
            elif bpy.context.tool_settings.mesh_select_mode[1] == True: #edge
                #bpy.ops.mesh.delete(type='EDGE')
                bpy.ops.mesh.dissolve_limited(angle_limit=180.00)
            elif bpy.context.tool_settings.mesh_select_mode[2] == True: #face
                bpy.ops.mesh.delete(type='FACE')
        return {'FINISHED'}

class yzk_duplicate(bpy.types.Operator):
    bl_idname = "yzk.yzk_duplicate"
    bl_label = "yzk_duplicate"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.object.duplicate(linked=False)
        return {'FINISHED'}

class yzk_instance(bpy.types.Operator):
    bl_idname = "yzk.yzk_instance"
    bl_label = "yzk_instance"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.object.duplicate(linked=True)
        return {'FINISHED'}

class yzk_edge_soft(bpy.types.Operator):
    bl_idname = "yzk.yzk_edge_soft"
    bl_label = "yzk_soft"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.mesh.mark_sharp(clear=True)
        bpy.ops.transform.edge_crease(value=-1.0)
        return {'FINISHED'}

class yzk_edge_hard(bpy.types.Operator):
    bl_idname = "yzk.yzk_edge_hard"
    bl_label = "yzk_hard"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.mesh.mark_sharp(clear=False)
        bpy.ops.transform.edge_crease(value=1.0)
        return {'FINISHED'}

class yzk_snap_to_vertex_on(bpy.types.Operator):
    bl_idname = "yzk.yzk_snap_to_vertex_on"
    bl_label = "yzk_snap_to_vertex_on"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.use_snap = True
        return {'FINISHED'}

class yzk_snap_to_vertex_off(bpy.types.Operator):
    bl_idname = "yzk.yzk_snap_to_vertex_off"
    bl_label = "yzk_snap_to_vertex_off"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        bpy.context.scene.tool_settings.use_snap = False
        return {'FINISHED'}

class yzk_snap_vertex_toggle(bpy.types.Operator):
    bl_idname = "yzk.yzk_snap_vertex_toggle"
    bl_label = "yzk_snap_vertex_toggle"
    editType = bpy.props.StringProperty()

    def execute(self, context):
        bpy.context.scene.tool_settings.snap_element = 'VERTEX'
        snap = bpy.context.scene.tool_settings.use_snap
        if snap == False:
            bpy.context.scene.tool_settings.use_snap = True
        else:
            bpy.context.scene.tool_settings.use_snap = False
        return {'FINISHED'}

class yzk_3dcursor(bpy.types.Operator):
    bl_idname = "yzk.yzk_3dcursor"
    bl_label = "yzk_3dcursor"

    def execute(self, context):
        obj = bpy.context.object
        if obj.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        elif obj.mode == 'EDIT':
            bpy.ops.view3d.snap_cursor_to_selected()
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}

class yzk_curve_new(bpy.types.Operator):
    bl_idname = "yzk.yzk_curve_new"
    bl_label = "yzk_curve_new"

    def execute(self, context):
        obj = bpy.context.object
        if obj is not None and not obj.mode == 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.curve.primitive_bezier_curve_add()
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.curve.select_all(action='SELECT')
        bpy.ops.curve.delete(type='VERT')
        return {'FINISHED'}

class yzk_select_handle(bpy.types.Operator):
    bl_idname = "yzk.yzk_select_handle"
    bl_label = "yzk_select_handle"

    def execute(self, context):
        obj = bpy.context.object
        curve = obj.data # Assumed that obj.type == 'CURVE'
        obj.update_from_editmode() # Loads edit-mode data into object data

        selected_cpoints = [p for p in chain(*[s.bezier_points for s in curve.splines])
                            if p.select_control_point]

        #bpy.ops.curve.select_all(action='DESELECT')
        for cp in selected_cpoints:
            cp.select_control_point = True
            cp.select_left_handle = True
            cp.select_right_handle = True
        return {'FINISHED'}

class yzk_set_handle(bpy.types.Operator):
    bl_idname = "yzk.yzk_set_handle"
    bl_label = "yzk_set_handle"
    type = bpy.props.StringProperty()

    def execute(self, context):
        bpy.ops.yzk.yzk_select_handle()
        if self.type == "AUTOMATIC":
            bpy.ops.curve.handle_type_set(type='AUTOMATIC')
        elif self.type == "VECTOR":
            bpy.ops.curve.handle_type_set(type='VECTOR')
        elif self.type == "ALIGNED":
            bpy.ops.curve.handle_type_set(type='ALIGNED')
        elif self.type == "FREE":
            bpy.ops.curve.handle_type_set(type='FREE')
        return {'FINISHED'}

class yzk_curve_dimensions(bpy.types.Operator):
    bl_idname = "yzk.yzk_curve_dimensions"
    bl_label = "yzk_curve_dimensions"

    def execute(self, context):
        obj = bpy.context.object
        if obj.data.dimensions == '2D':
            bpy.context.object.data.dimensions = '3D'
        else:
            bpy.context.object.data.dimensions = '2D'
        return{'FINISHED'}

class yzk_set_screen(bpy.types.Operator):
    bl_idname = "yzk.yzk_set_screen"
    bl_label = "yzk_set_screen"
    screenNum = bpy.props.IntProperty()

    def execute(self, context):
        screenList = bpy.data.screens
        str_currentScreen = bpy.context.screen.name
        str_targetScreen = "scripting"

        int_currentScreen = 0
        int_targetScreen = self.screenNum

        i=0
        for var in screenList:
        	if var.name == str_currentScreen:
        		int_currentScreen = i
        	i=i+1

        i=0
        for var in screenList:
        	if i == int_targetScreen:
        		print(var.name)
        		print(i)
        	i=i+1

        int_delta = int_targetScreen - int_currentScreen
        print(int_currentScreen)
        print(int_delta)

        if int_delta < 0:
        	int_delta_a = int_delta * (-1)
        	i=0
        	for i in range(0,int_delta_a):
        		bpy.ops.screen.screen_set(delta=-1)
        		i=i+1
        elif int_delta > 0:
        	i=0
        	for i in range(0,int_delta):
        		bpy.ops.screen.screen_set(delta=1)
        		i=i+1
        elif int_delta == 0:
            print("screenDelta=0")

        return {'FINISHED'}

class yzk_update_addon(bpy.types.Operator):
	bl_idname = "yzk.yzk_update_addon"
	bl_label = "yzk_update_addon"
	bl_description = "Update YZK_panel addon"
	bl_options = {'REGISTER'}

	def execute(self, context):
		response = urllib.request.urlopen("https://github.com/coverman03/blender/archive/master.zip")
		tempDir = bpy.app.tempdir
		zipPath = tempDir + r"\blender-master.zip"
		addonDir = os.path.dirname(__file__)
		f = open(zipPath, "wb")
		f.write(response.read())
		f.close()
		zf = zipfile.ZipFile(zipPath, "r")
		for f in zf.namelist():
			if not os.path.basename(f):
				pass
			else:
				if ("blender_master/python/bpy/" in f):
					uzf = open(addonDir +"\\"+ os.path.basename(f), 'wb')
					uzf.write(zf.read(f))
					uzf.close()
		zf.close()
		self.report(type={"INFO"}, message="アドオンを更新しました、Blenderを再起動して下さい")
		return {'FINISHED'}

def register():
    bpy.utils.register_class(yzk_popup_window)
    bpy.utils.register_class(yzk_select_edit_mode)
    bpy.utils.register_class(yzk_object_mode)
    bpy.utils.register_class(yzk_delete)
    bpy.utils.register_class(yzk_duplicate)
    bpy.utils.register_class(yzk_instance)
    bpy.utils.register_class(yzk_edge_soft)
    bpy.utils.register_class(yzk_edge_hard)
    bpy.utils.register_class(yzk_snap_vertex_toggle)
    bpy.utils.register_class(yzk_snap_to_vertex_on)
    bpy.utils.register_class(yzk_snap_to_vertex_off)
    bpy.utils.register_class(yzk_3dcursor)
    bpy.utils.register_class(yzk_curve_new)
    bpy.utils.register_class(yzk_select_handle)
    bpy.utils.register_class(yzk_set_handle)
    bpy.utils.register_class(yzk_curve_dimensions)
    bpy.utils.register_class(yzk_set_screen)
    bpy.utils.register_class(yzk_CustomPanel1)
    bpy.utils.register_class(yzk_CustomPanel2)
    bpy.utils.register_class(yzk_tools_panel)
    bpy.utils.register_class(yzk2_CustomPanel1)
    bpy.utils.register_class(yzk_update_addon)

def unregister():
    bpy.utils.unregister_class(yzk_popup_window)
    bpy.utils.unregister_class(yzk_select_edit_mode)
    bpy.utils.unregister_class(yzk_object_mode)
    bpy.utils.unregister_class(yzk_delete)
    bpy.utils.unregister_class(yzk_duplicate)
    bpy.utils.unregister_class(yzk_instance)
    bpy.utils.unregister_class(yzk_edge_soft)
    bpy.utils.unregister_class(yzk_edge_hard)
    bpy.utils.unregister_class(yzk_snap_vertex_toggle)
    bpy.utils.unregister_class(yzk_snap_to_vertex_on)
    bpy.utils.unregister_class(yzk_snap_to_vertex_off)
    bpy.utils.unregister_class(yzk_3dcursor)
    bpy.utils.unregister_class(yzk_curve_new)
    bpy.utils.unregister_class(yzk_select_handle)
    bpy.utils.unregister_class(yzk_set_handle)
    bpy.utils.unregister_class(yzk_curve_dimensions)
    bpy.utils.unregister_class(yzk_set_screen)
    bpy.utils.unregister_class(yzk_CustomPanel1)
    bpy.utils.unregister_class(yzk_CustomPanel2)
    bpy.utils.unregister_class(yzk_tools_panel)
    bpy.utils.unregister_class(yzk2_CustomPanel1)
    bpy.utils.unregister_class(yzk_update_addon)

if __name__ == "__main__":
    register()
