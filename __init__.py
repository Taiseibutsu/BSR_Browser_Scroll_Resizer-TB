
# (GNU GPL) <2022> <Taiseibutsu>" Developed for Blender 3.2
# This program is free software: you can redistribute it and/or modify it, WITHOUT ANY WARRANTY that you wont wake up on the backrooms.

bl_info = {
    "name": "File_Browser_Scroll_Resizer", "author": "Taiseibutsu",
    "version": (0, 1), "blender": (2, 80, 0), "location": "General UI Changes",
    "description": "Custom operation to resize content in the file browser using Alt + Scroll Mouse",
    "wiki_url": "",
    "category": "TB"}

import bpy 
from bpy.types import AddonPreferences

class TB_FBSR_custom_prop(bpy.types.PropertyGroup):
    tb_multiplier_resize_factor: bpy.props.IntProperty(default=10)

class TB_WheelUp(bpy.types.Operator):
    """Increase the size of file Viewer"""
    bl_idname = "tbcontext.filesizeincrease"
    bl_label = "Increase file explorer size"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = bpy.context.window_manager
        cp = wm.TB_FBSR_custom_prop_wm
        mrf = cp.tb_multiplier_resize_factor
        
        type = context.space_data.params.display_type
        if type == 'LIST_VERTICAL':
            bpy.context.space_data.params.display_type = 'LIST_HORIZONTAL'               
        elif type == 'LIST_HORIZONTAL':
            bpy.context.space_data.params.display_type = 'THUMBNAIL'
            bpy.context.space_data.params.display_size = 24      
        elif type == 'THUMBNAIL':
            if bpy.context.space_data.params.display_size < 256:
                if (bpy.context.space_data.params.display_size + mrf) >= 256:
                    bpy.context.space_data.params.display_size = 256
                if bpy.context.space_data.params.display_size < 256:
                    bpy.context.space_data.params.display_size = bpy.context.space_data.params.display_size + mrf
        return {'FINISHED'}
class TB_WheelDown(bpy.types.Operator):
    """Decrease the size of file Viewer"""
    bl_idname = "tbcontext.filesizedecrease"
    bl_label = "Decrease file explorer size"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        wm = bpy.context.window_manager
        cp = wm.TB_FBSR_custom_prop_wm
        mrf = cp.tb_multiplier_resize_factor
        type = context.space_data.params.display_type

        if type == 'THUMBNAIL':
            if bpy.context.space_data.params.display_size > 16:
                if (bpy.context.space_data.params.display_size - mrf) <= 16:
                    bpy.context.space_data.params.display_size = 16
                else:                    
                    bpy.context.space_data.params.display_size = bpy.context.space_data.params.display_size - mrf
            if bpy.context.space_data.params.display_size <= 16:
                bpy.context.space_data.params.display_type = 'LIST_HORIZONTAL'
        if type == 'LIST_HORIZONTAL':
            bpy.context.space_data.params.display_type = 'LIST_VERTICAL'                                
        return {'FINISHED'}

class TB_Custom_Dimensions_PreferencesPanel(AddonPreferences):
    bl_idname = __name__
    def draw(self, context):
        layout = self.layout
        box=layout.box()
        cp = bpy.context.window_manager.TB_FBSR_custom_prop_wm
        box.prop(cp,"tb_multiplier_resize_factor",text="Multiplier_Factor")

classes = (TB_WheelDown,TB_WheelUp,TB_Custom_Dimensions_PreferencesPanel)
def register():
 #CLASS
    for cls in classes:
        bpy.utils.register_class(cls)
 #KEYMAP
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    
    if kc:    
    #3Dview
        km = kc.keymaps.new(name='File Browser', space_type='FILE_BROWSER')
        kmi = km.keymap_items.new("tbcontext.filesizedecrease", 'WHEELOUTMOUSE', 'PRESS', alt=True)
        kmi.active = True
        kmi = km.keymap_items.new("tbcontext.filesizeincrease", 'WHEELINMOUSE', 'PRESS', alt=True)
        kmi.active = True
    bpy.utils.register_class(TB_FBSR_custom_prop)
    bpy.types.WindowManager.TB_FBSR_custom_prop_wm = bpy.props.PointerProperty(type=TB_FBSR_custom_prop)
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls) 
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name='File Browser', space_type='FILE_BROWSER')
    kmi = km.keymap_items.new("tbcontext.filesizedecrease", 'WHEELOUTMOUSE', 'PRESS', alt=True)
    kmi.active = False
    kmi = km.keymap_items.new("tbcontext.filesizeincrease", 'WHEELINMOUSE', 'PRESS', alt=True)
    kmi.active = False           
    bpy.utils.unregister_class(TB_FBSR_custom_prop)
    bpy.types.WindowManager.TB_FBSR_custom_prop = bpy.props.PointerProperty(type=TB_FBSR_custom_prop)        
if __name__ == "__main__":
    register()
