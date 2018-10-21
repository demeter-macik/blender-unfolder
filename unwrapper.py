import bpy
import math
import random
from utils import roundVector, getNormal, rotateVetricesToVector
from container import Container
from face import Face
from mathutils import Vector


class Unwrapper:

    def __init__(self):
        self.object = None
        self.faces = []
        self.vertices = []
        self.container = None

    def __str__(self):
        str = "object: {0}, vertices: {1}, faces: {2}"
        if(self.object != None):
            str = str.format(self.object.name, len(
                self.vertices), len(self.faces))
        else:
            str = "object: None"
        return str

    def areVerticesFlat(self, vertices):
        normals = []
        for i in range(0, len(vertices) - 2):
            normals.append(
                roundVector(
                    getNormal([vertices[i], vertices[i+1], vertices[i+2]]), 3)
            )
            normals.append(
                roundVector(
                    getNormal([vertices[i+1], vertices[i+2], vertices[0]]), 3)
            )
            normals.append(
                roundVector(
                    getNormal([vertices[i+2], vertices[0], vertices[1]]), 3)
            )
        for i in range(0, len(normals) - 1):
            if(normals[i] != normals[i+1]):
                return False
        return True

    def addFace(self, face):
        self.faces.append(face)
        face.index = len(self.faces) - 1
        return face.index

    def removeFace(self, face):
        return None

    def isValid(self, object, context):
        if(not object or object.type != 'MESH'):
            raise Exception('Expected object to be MESH')

        vertices = [face_vertex.co for face_vertex in object.data.vertices]

        not_flat = []

        for poly_index in range(0, len(object.data.polygons)):
            poly = object.data.polygons[poly_index]
            poly_vertices = [vertices[vertex] for vertex in poly.vertices]

            # skip if not selected
            if object.only_selected == True and poly.select == False:
                continue

            if(not self.areVerticesFlat(poly_vertices)):
                not_flat.append(poly_index)

        if(len(not_flat) > 0):
            bpy.context.scene.objects.active = object
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            bpy.context.tool_settings.mesh_select_mode = (False, False, True)
            for poly_index in not_flat:
                object.data.polygons[poly_index].select = True
            bpy.ops.object.mode_set(mode='EDIT')

        return len(not_flat) == 0

    def showPolygons(self, object, polygon_indices):

        if(len(polygon_indices) > 0):
            bpy.context.scene.objects.active = object
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
            bpy.context.tool_settings.mesh_select_mode = (False, False, True)
            for poly_index in polygon_indices:
                object.data.polygons[poly_index].select = True
            bpy.ops.object.mode_set(mode='EDIT')

    def unwrap(self, object):

        if(object and object.type == 'MESH'):
            self.object = object
        else:
            raise Exception('Expected object to be Mesh')

        vertices = [vertex.co for vertex in object.data.vertices]

        wrong_polygons = []

        faces = []

        for i in range(0, len(object.data.polygons)):

            polygon = object.data.polygons[i]

            # skip if not selected
            if object.only_selected == True and polygon.select == False:
                continue

            ploygon_indices = [index for index in polygon.vertices]
            ploygon_vertices = [vertices[index] for index in ploygon_indices]

            angles = []

            for polygon_edge in polygon.edge_keys:

                found = []

                for j in range(0, len(object.data.polygons)):

                    if i == j:
                        continue

                    neighbour = object.data.polygons[j]

                    for neighbour_edge in neighbour.edge_keys:
                        if polygon_edge == neighbour_edge:
                            found.append((i, j))

                if len(found) > 1:
                    wrong_polygons.append(i)

                angle = 0
                if len(found) == 1:
                    angle = polygon.normal.angle(
                        object.data.polygons[found[0][1]].normal)

                print('ANGLE', angle)
                angles.append(angle)

            # move all vertices to XY
            rotated_vertices = rotateVetricesToVector(
                ploygon_vertices,
                getNormal(ploygon_vertices),
                Vector((0, 0, 1))  # Z axis
            )
            for vertex in rotated_vertices:
                vertex.z = 0
                roundVector(vertex, 5)

            # create new face
            vs = [(v.x, v.y) for v in rotated_vertices]
            face = Face(vs, angles, object.group + str(i), vertices, polygon)

            faces.append(face)

        if len(wrong_polygons) > 0:
            self.showPolygons(object, wrong_polygons)
            raise Exception('We have wrong polygons', len(wrong_polygons))

        return faces

    def pack(self, context):

        self.container = Container(0, 0, 5)
        self.container.draw(context)
