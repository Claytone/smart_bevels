bl_info = {
    "name": "Smart Bevels",
    "author": "brujo.3d",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > S. Bevels tab",
    "description": "Bevel workflow tool."
                   "\n1. Open the sidebar (N menu) and go to the S. Bevels tab. "
                   "\n2. If it is your first time using smart bevels on this project, you will need to click the initialize button."
                   "\n3. Choose objects to add Smart Bevel modifiers to."
                   "\n4. In the sidebar, click Add SB to Selected Objs."
                   "\n5. Tweak the settings as desired."
                   "\n6. Choose Apply Settings.",
    "warning": "",
    "wiki_url": "",
    "category": "3D View"}

import bpy
from bpy.types import Operator
from bpy.utils import register_class, unregister_class

class Smart_Bevel_PT_panel(bpy.types.Panel):
    bl_label = "Smart Bevels"
    bl_category = "S. Bevels"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        if 'sb_amt' not in dir(bpy.context.scene) or 'sb_seg' not in dir(bpy.context.scene):
            layout.operator('smartbevels.init', text='Init Smart Bevels')
        else:
            layout.operator('object.addsmartbevel', text='Add SB to Selected Objs')
            layout.label(text='Settings')
            layout.prop(bpy.context.scene, 'sb_amt', text='Amount')
            layout.prop(bpy.context.scene, 'sb_seg', text='Segments')
            layout.operator('smartbevels.propagate', text='Apply Settings')


class InitSmartBevel(Operator):
    bl_idname = "smartbevels.init"
    bl_label = "Initialize Smart Bevels"
    bl_description = "Set up variables needed for Smart Bevels."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.types.Scene.sb_amt = bpy.props.FloatProperty()
        bpy.context.scene.sb_amt = 3
        bpy.types.Scene.sb_seg = bpy.props.IntProperty()
        bpy.context.scene.sb_seg = 3
        return {'FINISHED'}

class PropagateSmartBevel(Operator):
    bl_idname = "smartbevels.propagate"
    bl_label = "Propagate Smart Bevel Amount"
    bl_description = "Set amount for Smart Bevels to the value in Sidebar > S. Bevels > Amount"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.data.objects:
            for mod in obj.modifiers:
                if mod.name.startswith('Smart Bevel'):
                    mod.width = bpy.context.scene.sb_amt
                    mod.segments = bpy.context.scene.sb_seg
        return {'FINISHED'}

class AddSmartBevel(Operator):
    bl_idname = "object.addsmartbevel"
    bl_label = "Add Smart Bevel"
    bl_description = "Adds a Smart Bevel modifier all selected objects."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in context.selected_objects:
            context.view_layer.objects.active = obj
            if 'Smart Bevel' in obj.modifiers.keys():
                obj.modifiers.remove(bpy.context.object.modifiers["Smart Bevel"])
            bpy.ops.object.modifier_add(type='BEVEL')
            bpy.context.object.modifiers[-1].name = 'Smart Bevel'
            bpy.context.object.modifiers['Smart Bevel'].width = bpy.context.scene.sb_amt
            bpy.context.object.modifiers['Smart Bevel'].segments = bpy.context.scene.sb_seg
            bpy.context.object.modifiers['Smart Bevel'].offset_type = 'PERCENT'
            bpy.context.object.modifiers['Smart Bevel'].use_clamp_overlap = True
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddSmartBevel.bl_idname)

classes = (Smart_Bevel_PT_panel, InitSmartBevel, PropagateSmartBevel, AddSmartBevel)
# cls = SmartBevelPanel

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    # bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    # bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()