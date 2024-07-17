"""
This script splits three joints as we describe in the paper.
It automatically detects all the dirs in "./datasets/Mixamo" and
finds these can be split then create a new dir with an extra _m
as suffix to store the split files in the new dir.
"""

import sys
import os
from option_parser import try_mkdir
import numpy as np
from tqdm import tqdm
from datasets.bvh_parser import BVH_file

sys.path.append("../utils")
import BVH_mod as BVH


def reorder_joints(file_name, save_file=None):
    if save_file is None:
        save_file = file_name

    anim, names, ftime = BVH.load(file_name)
    n_joint = len(anim.parents)
    split_idx_gen = (i for i,n in enumerate(names) if n == 'LeftUpLeg')
    split_idx = next(split_idx_gen)

    new_anim = anim.copy()
    new_anim.parents = [-1, 0, 1, 2, 3, 4, 1, 6, 7, 8, 0, 10, 11, 12, 13, 12, 15, 16, 17, 12, 19, 20, 21]
    new_anim.offsets = np.concatenate((anim.offsets[0:2], anim.offsets[split_idx:n_joint], anim.offsets[2:split_idx]), axis=0)
    new_anim.rotations = np.concatenate((anim.rotations[:, 0:2], anim.rotations[:, split_idx:n_joint], anim.rotations[:, 2:split_idx]), axis=1)
    new_names = [*names[0:2], *names[split_idx:n_joint], *names[2:split_idx]]

    # Treat as cm
    new_anim.offsets = new_anim.offsets * 100
    new_anim.positions[:, 0] = anim.positions[:, 0] * 100

    try_mkdir(os.path.split(save_file)[0])
    BVH.save(save_file, new_anim, names=new_names, frametime=ftime, order='xyz')


def batch_reorder(source, dest):
    print("Working on {}".format(os.path.split(source)[-1]))
    try_mkdir(dest)
    files = [f for f in os.listdir(source) if f.endswith('.bvh')]
    for i, file in tqdm(enumerate(files), total=len(files)):
        in_file = os.path.join(source, file)
        out_file = os.path.join(dest, file)
        reorder_joints(in_file, out_file)


if __name__ == '__main__':
    prefix = './datasets/Mixamo'
    names = [f for f in os.listdir(prefix) if os.path.isdir(os.path.join(prefix, f))]
    print(names)

    for name in names:
        if name == 'Mark_split':
            batch_reorder(os.path.join(prefix, name), os.path.join(prefix, name + '_ordscale'))
