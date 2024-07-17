import bpy
import numpy as np

from os import listdir

data_path = './Mixamo/Mark'
files = sorted([f for f in listdir(data_path) if f.endswith(".bvh")])
for f in files:
    sourcepath = data_path + "/" + f
    dumppath = data_path + "/" + f.split(".bvh")[0] + "_XYZ.bvh"

    bpy.ops.import_anim.bvh(filepath=sourcepath, 
                            #use_fps_scale=True,
                            axis_forward='Y',
                            axis_up='Z')

    frame_start = 9999
    frame_end = -9999
    action = bpy.data.actions[-1]
    if action.frame_range[1] > frame_end:
        frame_end = action.frame_range[1]
    if action.frame_range[0] < frame_start:
        frame_start = action.frame_range[0]

    frame_end = np.max([60, frame_end])
    bpy.ops.export_anim.bvh(filepath=dumppath,
                            rotate_mode='XYZ',
                            frame_start=int(frame_start),
                            frame_end=int(frame_end), root_transform_only=True)
    bpy.data.actions.remove(bpy.data.actions[-1])
    
    print(data_path + "/" + f + " processed.")
