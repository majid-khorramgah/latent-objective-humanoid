import os
import numpy as np
import torch
import smplx

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import imageio
from tqdm import tqdm



# ==================================================
# PATHS
# ==================================================

MOTION_FILE = (
    r"F:\latent-objective-humanoid\03_human_motion\results\motions\CMU_31_01_motion.npz"
)


SMPLX_MODEL_PATH = (
    r"F:\latent-objective-humanoid\03_human_motion\external\smplx\models"
)


OUTPUT_VIDEO = (
    r"F:\latent-objective-humanoid\03_human_motion\results\videos\CMU_31_01_body.mp4"
)



os.makedirs(
    os.path.dirname(OUTPUT_VIDEO),
    exist_ok=True
)



# ==================================================
# LOAD MOTION
# ==================================================

data = np.load(
    MOTION_FILE
)


vertices = data["vertices"]


print("Motion loaded")

print(
    "Vertices:",
    vertices.shape
)



# vertices:
# (frames, 10475, 3)


frames = vertices.shape[0]



# ==================================================
# LOAD SMPL-X MODEL
# ==================================================

model = smplx.create(
    SMPLX_MODEL_PATH,
    model_type="smplx",
    gender="neutral"
)


faces = model.faces


print(
    "Faces:",
    faces.shape
)



# ==================================================
# VIDEO WRITER
# ==================================================

writer = imageio.get_writer(
    OUTPUT_VIDEO,
    fps=30
)



# ==================================================
# RENDER
# ==================================================

print("Rendering...")


for frame in tqdm(range(0, frames, 4)):


    verts = vertices[frame]


    fig = plt.figure(
        figsize=(6,6)
    )


    ax = fig.add_subplot(
        111,
        projection="3d"
    )


    # Mesh triangles

    mesh = verts[faces]


    body = Poly3DCollection(
        mesh,
        alpha=0.9
    )


    body.set_edgecolor(
        "none"
    )


    ax.add_collection3d(
        body
    )



    # axis limits

    center = verts.mean(axis=0)


    scale = 1.2


    ax.set_xlim(
        center[0]-scale,
        center[0]+scale
    )


    ax.set_ylim(
        center[1]-scale,
        center[1]+scale
    )


    ax.set_zlim(
        center[2]-scale,
        center[2]+scale
    )



    ax.view_init(
        elev=15,
        azim=-70
    )


    ax.set_title(
        f"SMPL-X Human Motion Frame {frame}"
    )


    ax.axis(
        "off"
    )



    # convert figure to image


    fig.canvas.draw()


    image = np.asarray(
        fig.canvas.buffer_rgba()
    )


    image = image[:,:,:3]


    writer.append_data(
        image
    )


    plt.close(fig)



writer.close()



print()
print("================================")
print("Video saved:")
print(OUTPUT_VIDEO)
print("================================")