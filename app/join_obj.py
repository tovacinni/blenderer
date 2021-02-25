import os
import sys

import bpy

# Example invocation:
# blender --background --python join_obj.py -- {OUT_PATH} {IN_PATH0} {IN_PATH1} ... {IN_PATHN}

outPath = sys.argv[sys.argv.index("--")+1]
meshPaths = sys.argv[sys.argv.index("--")+2:]

bpy.ops.wm.read_homefile()
bpy.ops.object.select_all(action = 'SELECT')
bpy.ops.object.delete()

for meshPath in meshPaths:
    bpy.ops.import_scene.obj(filepath=meshPath, split_mode='OFF')

# From https://blender.stackexchange.com/questions/13986/how-to-join-objects-with-python

ctx = bpy.context.copy()
ctx['active_object'] = bpy.context.scene.objects[0]
ctx['selected_editable_objects'] = bpy.context.scene.objects

bpy.ops.object.join(ctx)

bpy.ops.export_scene.obj(filepath=outPath)

