import os
import numpy as np
import torch
import smplx


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
    r"F:\latent-objective-humanoid\03_human_motion\results\meshes\CMU_31_01_mesh.npz"
)



# ===============================
# Load AMASS motion
# ===============================

data = np.load(
    AMASS_FILE,
    allow_pickle=True
)


poses = data["poses"]
betas = data["betas"]
trans = data["trans"]


print("\nAMASS loaded")

print("poses:", poses.shape)
print("betas:", betas.shape)
print("trans:", trans.shape)



# ===============================
# Create SMPL-X model
# ===============================

model = smplx.create(
    SMPLX_MODEL_PATH,
    model_type="smplx",
    gender="neutral",
    use_pca=False,
    batch_size=1
)


print("\nSMPL-X model loaded")

print(
    "Model requires betas:",
    model.num_betas
)



# ===============================
# Select frame
# ===============================

frame_id = 0


pose = poses[frame_id]



# ===============================
# Split AMASS pose
# ===============================

global_orient = pose[:3]

body_pose = pose[3:66]

left_hand = pose[66:111]

right_hand = pose[111:156]



# ===============================
# Convert pose to tensors
# ===============================


global_orient = torch.tensor(
    global_orient,
    dtype=torch.float32
).reshape(1,3)



body_pose = torch.tensor(
    body_pose,
    dtype=torch.float32
).reshape(1,63)



left_hand = torch.tensor(
    left_hand,
    dtype=torch.float32
).reshape(1,45)



right_hand = torch.tensor(
    right_hand,
    dtype=torch.float32
).reshape(1,45)



# ===============================
# Prepare betas
# Compatible with SMPL-X versions
# ===============================


num_betas = model.num_betas


beta_array = np.zeros(num_betas)


available_betas = min(
    len(betas),
    num_betas
)


beta_array[:available_betas] = betas[:available_betas]


betas_tensor = torch.tensor(
    beta_array,
    dtype=torch.float32
).reshape(1, num_betas)



print(
    "Final beta tensor:",
    betas_tensor.shape
)



# ===============================
# SMPL-X Forward
# ===============================


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
    .numpy()
)


joints = (
    output.joints
    .detach()
    .cpu()
    .numpy()
)



print("\nGenerated mesh")

print(
    "Vertices:",
    vertices.shape
)


print(
    "Joints:",
    joints.shape
)



# ===============================
# Save result
# ===============================


os.makedirs(
    os.path.dirname(OUTPUT_PATH),
    exist_ok=True
)



np.savez(
    OUTPUT_PATH,
    vertices=vertices,
    joints=joints
)



print("\nSaved successfully:")
print(OUTPUT_PATH)