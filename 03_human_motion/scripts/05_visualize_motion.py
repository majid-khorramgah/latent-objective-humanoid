import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import imageio


# ===============================
# Paths
# ===============================

MOTION_FILE = (
    r"F:\latent-objective-humanoid\03_human_motion\results\motions\CMU_31_01_motion.npz"
)


OUTPUT_VIDEO = (
    r"F:\latent-objective-humanoid\03_human_motion\media\videos\CMU_31_01_motion.mp4"
)



# ===============================
# Load motion
# ===============================

data = np.load(
    MOTION_FILE
)


joints = data["joints"]

fps = float(data["fps"])


print("Motion loaded")

print("Joints shape:")
print(joints.shape)

print("FPS:")
print(fps)



# ===============================
# SMPL-X skeleton connections
# ===============================

connections = [

    # spine
    (0,1),
    (1,2),
    (2,3),

    # left leg
    (0,7),
    (7,10),
    (10,11),

    # right leg
    (0,8),
    (8,12),
    (12,13),

    # left arm
    (3,20),
    (20,25),
    (25,27),

    # right arm
    (3,21),
    (21,26),
    (26,28),

    # head
    (3,15),
    (15,22)

]



# ===============================
# Create figure
# ===============================

fig = plt.figure(
    figsize=(6,8)
)

ax = fig.add_subplot(
    111,
    projection="3d"
)



# ===============================
# Animation update
# ===============================

def update(frame):

    ax.clear()


    pose = joints[frame]


    x = pose[:,0]
    y = pose[:,1]
    z = pose[:,2]


    # joints

    ax.scatter(
        x,
        y,
        z,
        s=10
    )


    # bones

    for start,end in connections:

        ax.plot(
            [
                x[start],
                x[end]
            ],
            [
                y[start],
                y[end]
            ],
            [
                z[start],
                z[end]
            ]
        )


    ax.set_title(
        f"SMPL-X Human Motion Frame {frame}"
    )


    ax.set_xlim(
        x.min()-0.5,
        x.max()+0.5
    )

    ax.set_ylim(
        y.min()-0.5,
        y.max()+0.5
    )

    ax.set_zlim(
        z.min()-0.5,
        z.max()+0.5
    )


    ax.view_init(
        elev=15,
        azim=-70
    )


    return ax



# ===============================
# Create animation
# ===============================

print("Creating animation...")


animation = FuncAnimation(
    fig,
    update,
    frames=len(joints),
    interval=1000/fps
)



# ===============================
# Save mp4
# ===============================

os.makedirs(
    os.path.dirname(OUTPUT_VIDEO),
    exist_ok=True
)


writer = imageio.get_writer(
    OUTPUT_VIDEO,
    fps=fps
)


for frame in range(len(joints)):

    update(frame)

    fig.canvas.draw()

    image = np.frombuffer(
        fig.canvas.buffer_rgba(),
        dtype=np.uint8
    )


    image = image.reshape(
        fig.canvas.get_width_height()[::-1] + (4,)
    )


    writer.append_data(
        image[:,:,:3]
    )


writer.close()


print("\nSaved video:")
print(OUTPUT_VIDEO)