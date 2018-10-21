import bpy
from mathutils import Matrix, Vector
import math


def getMeshCenter(object):
    center = [0, 0, 0]
    matrix = object.matrix_world
    count = 0
    for vertex in object.data.vertices:
        worl_co = matrix * vertex.co
        center[0] += worl_co[0]
        center[1] += worl_co[1]
        center[2] += worl_co[2]
        count += 1
    center[0] /= count
    center[1] /= count
    center[2] /= count
    return center


def setOrigin(object, origin):
    location = object.location
    for vert in object.data.vertices:
        vert.co[0] -= origin[0] - location[0]
        vert.co[1] -= origin[1] - location[1]
        vert.co[2] -= origin[2] - location[2]

    print('origin', origin)

    object.location = origin


def getNormal(vertices):
    v0 = vertices[1] - vertices[0]
    v1 = vertices[2] - vertices[0]
    normal = v0.cross(v1)
    normal.normalize()
    return normal


def rotateVetricesToVector(vertices, up, vector):
    rot = up.rotation_difference(vector)
    new_vertices = []
    for vertex in vertices:
        v = vertex.copy()
        v.rotate(rot)
        new_vertices.append(v)
    return new_vertices


def roundVector(vector, roundTo):
    vector.x = round(vector.x, 3)
    vector.y = round(vector.y, 3)
    vector.z = round(vector.z, 3)
    return vector


def getCenter(vertices):
    center = [0, 0, 0]
    count = 0
    for v in vertices:
        center[0] += v[0]
        center[1] += v[1]
        center[2] += v[2]
        count += 1
    center[0] /= count
    center[1] /= count
    center[2] /= count
    return Vector((center))


def getDistance(a, b):
    return math.sqrt(math.pow((b.x - a.x), 2) + math.pow((b.y - a.y), 2))


def createNewMesh(context, name, vertices, faces):

    mesh = bpy.data.meshes.new("mesh")
    object = bpy.data.objects.new(name, mesh)
    object.show_name = True
    scene = context.scene
    scene.objects.link(object)
    mesh.from_pydata(vertices, [], faces)
    mesh.update(calc_edges=True)
    setOrigin(object, getMeshCenter(object))

    return object
