import numpy as np
import os


# ===============================
# Input AMASS motion file
# ===============================

amass_file = r"F:\latent-objective-humanoid\03_human_motion\data\AMASS\raw\CMU\31\31_01_poses.npz"


# ===============================
# Output directory
# ===============================

output_dir = r"F:\latent-objective-humanoid\03_human_motion\results\poses"

os.makedirs(output_dir, exist_ok=True)



# ===============================
# Load AMASS
# ===============================

data = np.load(amass_file, allow_pickle=True)


poses = data["poses"]


print("Original pose shape:")
print(poses.shape)



# ===============================
# Convert:
# (frames,156)
# to
# (frames,52,3)
# ===============================

num_frames = poses.shape[0]

num_joints = 52


pose_reshaped = poses.reshape(
    num_frames,
    num_joints,
    3
)


print("\nConverted pose shape:")
print(pose_reshaped.shape)



# ===============================
# Save extracted pose
# ===============================

output_file = os.path.join(
    output_dir,
    "CMU_31_01_pose.npy"
)


np.save(
    output_file,
    pose_reshaped
)


print("\nSaved:")
print(output_file)