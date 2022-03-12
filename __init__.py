
# (GNU GPL) <2022> <Taiseibutsu>" Developed for Blender 3.2
# This program is free software: you can redistribute it and/or modify it, WITHOUT ANY WARRANTY that you wont wake up on the backrooms.

bl_info = {
    "name": "File_Browser_Scroll_Resizer", "author": "Taiseibutsu",
    "version": (0, 1), "blender": (2, 80, 0), "location": "General UI Changes",
    "description": "Custom operation to resize content in the file browser using Alt + Scroll Mouse",
    "wiki_url": "",
    "category": "TB"}

import bpy 

class TB_WheelUp(bpy.types.Operator):
    """Increase the size of file Viewer"""
    bl_idname = "tbcontext.filesizeincrease"
    bl_label = "Increase file explorer size"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        type = context.space_data.params.display_type
        if type == 'LIST_VERTICAL':
            bpy.context.space_data.params.display_type = 'LIST_HORIZONTAL'               
        elif type == 'LIST_HORIZONTAL':
            bpy.context.space_data.params.display_type = 'THUMBNAIL' 
            bpy.context.space_data.params.display_size = 'TINY'          
        elif type == 'THUMBNAIL':
            size = context.space_data.params.display_size
            if size == 'TINY':      
                bpy.context.space_data.params.display_size = 'SMALL'
            elif size == 'SMALL':
                bpy.context.space_data.params.display_size = 'NORMAL'
            elif size == 'NORMAL':
                bpy.context.space_data.params.display_size = 'LARGE'
        return {'FINISHED'}
class TB_WheelDown(bpy.types.Operator):
    """Decrease the size of file Viewer"""
    bl_idname = "tbcontext.filesizedecrease"
    bl_label = "Decrease file explorer size"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        type = context.space_data.params.display_type
        if type == 'THUMBNAIL':
            size = context.space_data.params.display_size
            if size == 'LARGE':
                bpy.context.space_data.params.display_size = 'NORMAL'
            if size == 'NORMAL':
                bpy.context.space_data.params.display_size = 'SMALL'
            if size == 'SMALL':
                bpy.context.space_data.params.display_size = 'TINY'
            if size == 'TINY':      
                bpy.context.space_data.params.display_type = 'LIST_HORIZONTAL'
        if type == 'LIST_HORIZONTAL':
            bpy.context.space_data.params.display_type = 'LIST_VERTICAL'                                
        return {'FINISHED'}
classes = (TB_WheelDown,TB_WheelUp)
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
if __name__ == "__main__":
    register()
