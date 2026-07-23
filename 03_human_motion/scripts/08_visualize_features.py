import os
import numpy as np
import matplotlib.pyplot as plt


# ==========================================
# PATH
# ==========================================

FEATURE_FILE = (
    r"C:\latent-objective-humanoid\03_human_motion"
    r"\results\features\CMU"
    r"\31_01_features.npz"
)


OUTPUT = (
    r"C:\latent-objective-humanoid\03_human_motion"
    r"\media\screenshots"
    r"\04_motion_features.png"
)


os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)


# ==========================================
# LOAD FEATURES
# ==========================================

data = np.load(
    FEATURE_FILE
)


velocity = data["velocity"]

acceleration = data["acceleration"]

energy = data["energy"]


print("Loaded features")

print("Velocity:", velocity.shape)

print("Acceleration:", acceleration.shape)

print("Energy:", energy.shape)



# ==========================================
# Reduce dimensions
# ==========================================

# average movement of all joints

velocity_mag = np.linalg.norm(
    velocity,
    axis=2
).mean(axis=1)



acceleration_mag = np.linalg.norm(
    acceleration,
    axis=2
).mean(axis=1)



# ==========================================
# Plot
# ==========================================


plt.figure(
    figsize=(10,8)
)


# Velocity

plt.subplot(
    3,
    1,
    1
)

plt.plot(
    velocity_mag
)

plt.title(
    "Joint Velocity"
)

plt.ylabel(
    "Magnitude"
)


# Acceleration

plt.subplot(
    3,
    1,
    2
)

plt.plot(
    acceleration_mag
)

plt.title(
    "Joint Acceleration"
)

plt.ylabel(
    "Magnitude"
)



# Energy

plt.subplot(
    3,
    1,
    3
)

plt.plot(
    energy
)

plt.title(
    "Motion Energy"
)

plt.xlabel(
    "Frame"
)

plt.ylabel(
    "Energy"
)



plt.suptitle(
    "AMASS Human Motion Feature Representation",
    fontsize=14
)


plt.tight_layout()



plt.savefig(
    OUTPUT,
    dpi=300,
    bbox_inches="tight"
)


plt.close()



print("Saved:")
print(OUTPUT)