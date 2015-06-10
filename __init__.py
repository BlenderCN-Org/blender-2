import os, csv, codecs

bl_info = {
	"name" : "YZK_addon",
	"author" : "YZK",
	"version" : (1,0),
	"blender" : (2, 7),
	"location" : "tools",
	"description" : "モデリングに有用なコマンドをtoolsへ追加するアドオン",
	"warning" : "",
	"wiki_url" : "https://github.com/coverman03/blender",
	"tracker_url" : "https://github.com/coverman03/blender/issues",
	"category" : "3D View"
}

if "bpy" in locals():
	import imp
	imp.reload(yzk_panel)
	imp.reload(yzk_panel_uv)

else:
	from . import yzk_panel
	from . import yzk_panel_uv

import bpy
import os

def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)

# メイン関数
if __name__ == "__main__":
	register()
