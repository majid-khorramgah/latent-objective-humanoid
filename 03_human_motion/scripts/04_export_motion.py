import os
import numpy as np
import torch
import smplx
from tqdm import tqdm


# ===============================
# Paths
# ===============================

AMASS_FILE = (
    r"F:\latent-objective-humanoid\03_human_motion\data\AMASS\raw\CMU\31\31_01_poses.npz"
)


SMPLX_MODEL_PATH = (
    r"F:\latent-objective-humanoid\03_human_motion\external\smplx\models"
)


OUTPUT_PATH = (
    r"F:\latent-objective-humanoid\03_human_motion\results\motions\CMU_31_01_motion.npz"
)



# ===============================
# Load AMASS
# ===============================

data = np.load(
    AMASS_FILE,
    allow_pickle=True
)


poses = data["poses"]
betas = data["betas"]
trans = data["trans"]

fps = float(data["mocap_framerate"])



print("AMASS loaded")

print("Frames:", poses.shape[0])
print("Pose dimension:", poses.shape[1])
print("FPS:", fps)



# ===============================
# Load SMPL-X
# ===============================

model = smplx.create(
    SMPLX_MODEL_PATH,
    model_type="smplx",
    gender="neutral",
    use_pca=False,
    batch_size=1
)


print("SMPL-X loaded")

print(
    "Number of betas:",
    model.num_betas
)



# ===============================
# Prepare betas
# ===============================

num_betas = model.num_betas


beta_array = np.zeros(num_betas)


available = min(
    len(betas),
    num_betas
)


beta_array[:available] = betas[:available]


betas_tensor = torch.tensor(
    beta_array,
    dtype=torch.float32
).reshape(1,num_betas)



# ===============================
# Storage
# ===============================

all_vertices = []

all_joints = []



# ===============================
# Process all frames
# ===============================

print("\nProcessing motion...")


for frame_id in tqdm(range(len(poses))):


    pose = poses[frame_id]


    global_orient = torch.tensor(
        pose[:3],
        dtype=torch.float32
    ).reshape(1,3)



    body_pose = torch.tensor(
        pose[3:66],
        dtype=torch.float32
    ).reshape(1,63)



    left_hand = torch.tensor(
        pose[66:111],
        dtype=torch.float32
    ).reshape(1,45)



    right_hand = torch.tensor(
        pose[111:156],
        dtype=torch.float32
    ).reshape(1,45)



    output = model(
        betas=betas_tensor,
        global_orient=global_orient,
        body_pose=body_pose,
        left_hand_pose=left_hand,
        right_hand_pose=right_hand
    )



    vertices = (
        output.vertices
        .detach()
        .cpu()
        .numpy()[0]
    )


    joints = (
        output.joints
        .detach()
        .cpu()
        .numpy()[0]
    )


    all_vertices.append(vertices)

    all_joints.append(joints)



# ===============================
# Convert list to numpy
# ===============================

all_vertices = np.array(all_vertices)

all_joints = np.array(all_joints)



print("\nMotion generated")

print(
    "Vertices:",
    all_vertices.shape
)


print(
    "Joints:",
    all_joints.shape
)



# ===============================
# Save
# ===============================

os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)



np.savez(
    OUTPUT_PATH,
    vertices=all_vertices,
    joints=all_joints,
    fps=fps
)



print("\nSaved:")
print(OUTPUT_PATH)