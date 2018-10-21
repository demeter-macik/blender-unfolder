from mathutils import Vector
from utils import createNewMesh
from shapely.geometry import Point, Polygon, LineString
from shapely import affinity
import math
import bpy


class Face:

    def __init__(self, vertices, angles, name, original_vertices, original_polygon):

        if len(vertices) != len(angles):
            raise Exception('vertice len should == angles len')

        self.original_vertices = original_vertices
        self.original_polygon = original_polygon
        self.polygon = Polygon(vertices)
        self.angles = angles
        self.name = name
        longest = self.getLongestEdgeData()
        self.longest_edge_index = longest[0]
        self.longest_edge_length = longest[1]
        self.font = bpy.data.fonts.load(
            '/home/dima/.local/share/fonts/PressStart2P.ttf')

    def getLongestEdge(self):

        start = self.polygon.exterior.coords[self.longest_edge_index]

        end_index = self.longest_edge_index + 1
        if self.longest_edge_index == (len(self.polygon.exterior.coords) - 1):
            end_index = 0

        end = self.polygon.exterior.coords[end_index]

        return (start, end)

    def getVertices(self):

        vertices = [Vector((coord[0], coord[1], 0))
                    for coord in self.polygon.exterior.coords]

        vertices.pop(len(vertices) - 1)

        return vertices

    def draw(self, context):

        object = createNewMesh(
            context,
            self.name,
            self.getVertices(),
            [range(0, len(self.polygon.exterior.coords) - 1)]
        )

        return object

    def getCenter(self):
        vertices = self.getVertices()

        center = [0, 0, 0]
        counter = 0
        for vertex in vertices:

            center[0] += vertex.x
            center[1] += vertex.y
            counter += 1

        center[0] /= counter
        center[1] /= counter
        return center

    def rotate(self, angle, origin, use_radians=True):

        self.polygon = affinity.rotate(
            self.polygon, angle, origin, use_radians)

    def translate(self, source, target):

        diff = target - source
        self.polygon = affinity.translate(
            self.polygon, diff.x, diff.y, 0)

    def copy(self):

        return Face(self.polygon.exterior.coords, self.angles, self.name)

    def getEdgeByIndex(self, edge_index):

        if edge_index < 0 or edge_index > (len(self.polygon.exterior.coords) - 1):
            raise Exception('Edge index out of range', edge_index)

        coord1 = self.polygon.exterior.coords[edge_index]

        index2 = edge_index + 1
        if index2 > len(self.polygon.exterior.coords) - 2:
            index2 = 0

        coord2 = self.polygon.exterior.coords[index2]

        return (coord1, coord2)

    def getLongestEdgeData(self):

        edges = []
        for index in range(0, len(self.polygon.exterior.coords) - 2):
            coord1 = self.polygon.exterior.coords[index]
            coord2 = self.polygon.exterior.coords[index + 1]
            edges.append(LineString([coord1, coord2]))

        coord1 = self.polygon.exterior.coords[index+1]
        coord2 = self.polygon.exterior.coords[0]
        edges.append(LineString([coord1, coord2]))

        max_len = None
        longest_edge_index = None
        for edge_index in range(0, len(edges)):
            edge = edges[edge_index]

            if max_len == None or max_len < edge.length:
                max_len = edge.length
                longest_edge_index = edge_index

        return (longest_edge_index, max_len)

    def isPointInside(self, point):

        return self.polygon.contains(Point(point.x, point.y))

    def getLabelPoint(self, edge_index, label_indent):

        edge = self.getEdgeByIndex(edge_index)

        start = Vector(edge[0])
        end = Vector(edge[1])
        center = Vector(((start.x + end.x)/2, (start.y + end.y)/2))

        v = start - center
        v90 = Vector((-v.y, v.x))
        v90.normalize()
        labelPoint0 = center + v90 * label_indent
        labelPoint1 = center - v90 * label_indent

        if self.isPointInside(labelPoint0):
            return Vector((labelPoint0[0], labelPoint0[1], 0))
        elif self.isPointInside(labelPoint1):
            return Vector((labelPoint1[0], labelPoint1[1], 0))
        else:
            raise Exception("Can't find label point!")

    def createLabels(self, context, font_size, label_indent):

        for i in range(0, len(self.angles)):
            angle = self.angles[i]
            a = int(round(math.degrees(angle/2)))

            label = self.createLable(a, self.getLabelPoint(
                i, label_indent), context, font_size)
            context.scene.objects.link(label)

        label = self.createLable(
            self.name, self.getCenter(), context, font_size)
        context.scene.objects.link(label)

    def createLable(self, string, position, context, font_size):

        fontCurve = bpy.data.curves.new(type="FONT", name="myFontCurve")

        text = bpy.data.objects.new("f", fontCurve)
        text.data.body = str(string)
        text.data.font = self.font

        mesh = text.to_mesh(context.scene, True,  'PREVIEW')

        obj = bpy.data.objects.new("f", mesh)
        obj.location = position
        for vertex in obj.data.vertices:
            vertex.co = vertex.co * font_size

        return obj

    def drawOriginal(self, context):        

        
        indices = self.original_polygon.vertices

        new_vertices = []
        new_indices = []

        for i in range(0, len(self.original_polygon.vertices)):
            index = self.original_polygon.vertices[i]
            vertex = self.original_vertices[index]
            new_indices.append(i)
            new_vertices.append(vertex)
        
        object = createNewMesh(
            context,
            'c' + self.name,
            new_vertices,
            [new_indices] 
        )

        return object