bl_info = {
    "name": "Unfolder",
    "description": "Unfold (unwrap) mesh, create new meshes from faces and align them to XY plane.",
    "author": "Demeter Macik",
    "version": (0, 1, 0),
    "blender": (2, 79, 0),
    "location": "3D View > Tools, and Properties > Scene > Unfolder",
    "warning": "Requires Shapely to be installed (https://pypi.org/project/Shapely/)",
    "wiki_url": "https://github.com/demeter-macik/blender-unfolder/blob/master/README.md",
    "tracker_url": "https://github.com/demeter-macik/blender-unfolder/issues",
    "support": "TESTING",
    "category": "Mesh"
}

import bpy
import sys
import os
from mathutils import Vector
from shapely.geometry import Polygon
from shapely import affinity
from bpy.props import BoolProperty, FloatProperty, StringProperty

# check if we have our path in sys path
dir = os.path.dirname(os.path.realpath(__file__))
if not dir in sys.path:
    sys.path.append(dir)

import container
import face
import unwrapper
import utils
import importlib

importlib.reload(container)
importlib.reload(face)
importlib.reload(unwrapper)
importlib.reload(utils)

from container import Container
from face import Face
from unwrapper import Unwrapper
from utils import *

bpy.types.Object.group = StringProperty(name="group", default="unfolded",
    description="Mesh name prefix")
bpy.types.Object.only_selected = BoolProperty(
    name="only_selected", default=False,
    description="Unfold only selected faces")
bpy.types.Object.x_margin = FloatProperty(
    name="x_margin", default=0.005, precision=3, step=0.1,
    description="Distance between meshes")
bpy.types.Object.y_margin = FloatProperty(
    name="y_margin", default=0.005, precision=3, step=0.1,
    description="Distance between meshes")
bpy.types.Object.x_pos = FloatProperty(
    name="x_pos", default=.0, precision=3, step=0.1,
    description="Start placing meshes at this point")
bpy.types.Object.y_pos = FloatProperty(
    name="y_pos", default=.0, precision=3, step=0.1,
    description="Start placing meshes at this point")
bpy.types.Object.column_height = FloatProperty(
    name="column_height", default=.27, precision=3, step=0.1,
    description="Height of the placing box")

class UnfolderPanel(bpy.types.Panel):
    bl_idname = "panel.unfolder"
    bl_label = "Unfolder"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "Unfolder"

    @classmethod
    def poll(self, context):
        if context.object and context.object.type == 'MESH':
            return True

    def draw(self, context):

        object = context.object
        layout = self.layout

        box = layout.box()
        box.label("Placing")

        box.prop(object, 'column_height', 'Height')

        row = box.row()
        box.label('Position:')
        box.prop(object, 'x_pos', 'x')
        box.prop(object, 'y_pos', 'y')

        row = box.row()
        box.label('Margins:')
        box.prop(object, 'x_margin', 'x')
        box.prop(object, 'y_margin', 'y')

        box = layout.box()
        box.label("Unfold")       
                
        box.prop(object, 'group', 'Name prefix')
        box.prop(object, 'only_selected', 'Only selected')
        
        row = layout.row()
        row.operator("operator.test", text="Test")
        row.operator("operator.unfold", text="Unfold")


class UnfolderOperator(bpy.types.Operator):
    """Unfold mesh"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "operator.unfold"        # unique identifier for buttons and menu items to reference.
    bl_label = "Unfold mesh"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):

        object = bpy.data.objects[context.object.name]
        unwrapper = Unwrapper()

        if(unwrapper.isValid(object, context)):

            faces = unwrapper.unwrap(object)
            container = Container(
                object.x_pos, 
                object.y_pos, 
                object.column_height * 0.95)
            container.addFaces(faces)
            container.sort()
            container.place(object.x_margin, object.y_margin)
            container.draw(context)

        return {'FINISHED'}


class TestOperator(bpy.types.Operator):
    """Test if mesh has not flat faces""" # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "operator.test"        # unique identifier for buttons and menu items to reference.
    bl_label = "Test"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.

    def execute(self, context):

        object = bpy.data.objects[context.object.name]
        unwrapper = Unwrapper()
        unwrapper.isValid(object, context)

        return {'FINISHED'}


def register():
    print("Registering ", __name__)
    bpy.utils.register_module(__name__)


def unregister():
    print("Unregistering ", __name__)
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
