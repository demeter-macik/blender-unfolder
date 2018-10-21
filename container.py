from mathutils import Vector
from face import Face
import random
import time
import math


class Container:

    def __init__(self, x, y, length):

        self.x = x
        self.y = y
        self.length = length
        self.faces = []

    def addFaces(self, faces):

        sorted_faces = sorted(
            faces, key=lambda k: k.longest_edge_length, reverse=False)

        self.faces = sorted_faces

    def sort(self):

        # align to Y axis
        align_axis = Vector((0, 1))

        rotated_faces = []
        for face in self.faces:
            edge = face.getLongestEdge()
            edge_vector = Vector(edge[1]) - Vector(edge[0])

            # change vector direction to positive
            if edge[0][0] > edge[1][0]:
                edge_vector = Vector(edge[0]) - Vector(edge[1])

            angle = align_axis.angle(edge_vector)
            face.rotate(angle, 'center')
            center = face.getCenter()
            edge = face.getLongestEdge()

            # rotate the way that all other vertices is on the right side
            if edge[0][0] > center[0]:
                face.rotate(math.radians(180), 'center')

            # aligh to Y axis
            edge = face.getLongestEdge()
            point = Vector(edge[1])
            target = Vector((self.x, self.y))
            face.translate(point, target)

            rotated_faces.append(face)

        self.faces = rotated_faces

    def place(self, distance_x, distance_y):

        pos_x = self.x
        pos_y = self.y
        max_y = self.y + self.length
        max_x = 0       

        for face in self.faces:
            len = face.longest_edge_length

            edge = face.getLongestEdge()
            point = Vector(edge[1])

            new_x = point.x + pos_x
            new_y = pos_y            

            target = Vector((new_x, new_y))
            face.translate(point, target)

            vertices = face.getVertices()

            for vertex in vertices:
                if max_x < vertex.x:
                    max_x = vertex.x

            pos_y += len + distance_y

            edge = face.getLongestEdge()
            point = Vector(edge[1])

            if pos_y > max_y:
                pos_y = self.y
                pos_x += (max_x - (point.x )) + distance_x
                max_x = 0
                

    def draw(self, context):

        for face in self.faces:
            face.draw(context)
            # face.drawOriginal(context)
