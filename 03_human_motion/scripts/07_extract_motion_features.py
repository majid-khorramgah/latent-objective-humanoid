import os
import numpy as np


# ==========================================
# Paths
# ==========================================

MOTION_FILE = (
    r"F:\latent-objective-humanoid\03_human_motion\results\motions\CMU_31_01_motion.npz"
)


OUTPUT_FILE = (
    r"F:\latent-objective-humanoid\03_human_motion\results\features\CMU_31_01_features.npz"
)



os.makedirs(
    os.path.dirname(OUTPUT_FILE),
    exist_ok=True
)



# ==========================================
# Load SMPL-X motion
# ==========================================

data = np.load(
    MOTION_FILE
)


vertices = data["vertices"]

joints = data["joints"]


print("Motion loaded")

print("Vertices:")
print(vertices.shape)

print("Joints:")
print(joints.shape)



# Remove batch dimension if exists

if joints.ndim == 4:
    joints = joints[:,0]


# joints:

# frames x joints x xyz

frames = joints.shape[0]



print("Frames:", frames)



# ==========================================
# 1. Joint Positions
# ==========================================

joint_positions = joints



# ==========================================
# 2. Joint Velocity
# ==========================================

fps = 120.0


dt = 1.0 / fps



joint_velocity = np.gradient(
    joint_positions,
    dt,
    axis=0
)



# ==========================================
# 3. Joint Acceleration
# ==========================================

joint_acceleration = np.gradient(
    joint_velocity,
    dt,
    axis=0
)



# ==========================================
# 4. Root trajectory
# ==========================================

# SMPL-X pelvis joint

root_joint_id = 0


root_position = (
    joint_positions[:,root_joint_id,:]
)



root_velocity = np.gradient(
    root_position,
    dt,
    axis=0
)



# ==========================================
# 5. Motion energy proxy
# ==========================================

# approximate kinetic energy:
# sum velocity squared


motion_energy = np.sum(
    joint_velocity ** 2,
    axis=(1,2)
)



# ==========================================
# 6. Normalize features
# ==========================================


def normalize(x):

    mean = np.mean(
        x,
        axis=0
    )

    std = np.std(
        x,
        axis=0
    ) + 1e-8


    return (
        (x-mean)/std,
        mean,
        std
    )



joint_velocity_norm, vel_mean, vel_std = normalize(
    joint_velocity
)



joint_acceleration_norm, acc_mean, acc_std = normalize(
    joint_acceleration
)



# ==========================================
# Save
# ==========================================


np.savez(
    OUTPUT_FILE,

    joint_positions=joint_positions,

    joint_velocity=joint_velocity_norm,

    joint_acceleration=joint_acceleration_norm,

    root_position=root_position,

    root_velocity=root_velocity,

    motion_energy=motion_energy,

    fps=fps,

    velocity_mean=vel_mean,

    velocity_std=vel_std,

    acceleration_mean=acc_mean,

    acceleration_std=acc_std
)



print()
print("==============================")
print("Features extracted")
print("==============================")

print("Saved:")
print(OUTPUT_FILE)


print()
print("Feature summary:")

print(
    "Joint positions:",
    joint_positions.shape
)

print(
    "Velocity:",
    joint_velocity_norm.shape
)

print(
    "Acceleration:",
    joint_acceleration_norm.shape
)

print(
    "Energy:",
    motion_energy.shape
)