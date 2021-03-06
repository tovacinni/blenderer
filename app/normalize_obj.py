import os
import sys
from mathutils import Vector
import math

import bpy

# Example invocation:
# blender --background --python normalize_obj.py -- {OUT_PATH} {IN_PATH}

outPath = sys.argv[sys.argv.index("--")+1]
meshPath = sys.argv[sys.argv.index("--")+2]

bpy.ops.wm.read_homefile()
bpy.ops.object.select_all(action = 'SELECT')
bpy.ops.object.delete()
bpy.ops.import_scene.obj(filepath=meshPath, split_mode='OFF')

# From: https://blender.stackexchange.com/questions/58029/how-to-make-an-object-fit-in-a-unit-cube

#obj = bpy.context.object

#Eventually apply transforms (comment if unwanted)
#bpy.ops.object.transform_apply( rotation = True, scale = True )

ctx = bpy.context.copy()
ctx['active_object'] = bpy.context.scene.objects[0]

minX = min( [vertex.co[0] for vertex in ctx['active_object'].data.vertices] )
minY = min( [vertex.co[1] for vertex in ctx['active_object'].data.vertices] )
minZ = min( [vertex.co[2] for vertex in ctx['active_object'].data.vertices] )

maxX = max( [vertex.co[0] for vertex in ctx['active_object'].data.vertices] )
maxY = max( [vertex.co[1] for vertex in ctx['active_object'].data.vertices] )
maxZ = max( [vertex.co[2] for vertex in ctx['active_object'].data.vertices] )

centerX = (minX + maxX) / 2.0
centerY = (minY + maxY) / 2.0
centerZ = (minZ + maxZ) / 2.0

centerV = Vector( [centerX, centerY, centerZ] )

dists = []

# New code: Fit in unit sphere
for v in ctx['active_object'].data.vertices:
    v.co -= centerV
    dists.append(math.sqrt(v.co.x**2 + v.co.y**2 + v.co.z**2))
max_dist = max(dists)
for v in ctx['active_object'].data.vertices:
    v.co /= max_dist

# Old code: Fit in Unit Cube

#vMin = Vector( [minX, minY, minZ] )
#maxDim = max(ctx['active_object'].dimensions)
#if maxDim != 0:
#    for v in ctx['active_object'].data.vertices:
#        v.co -= vMin #Set all coordinates start from (0, 0, 0)
#        v.co /= maxDim #Set all coordinates between 0 and 1
#        v.co *= Vector( [2.0, 2.0, 2.0] )
#        v.co -= Vector( [1.0, 1.0, 1.0] )
#else:
#    for v in ctx['active_object'].data.vertices:
#        v.co -= vMin

bpy.ops.export_scene.obj(filepath=outPath)

