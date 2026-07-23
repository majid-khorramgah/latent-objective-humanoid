import numpy as np


amass_file = r"F:\latent-objective-humanoid\03_human_motion\data\AMASS\raw\CMU\31\31_01_poses.npz"


data = np.load(amass_file, allow_pickle=True)


print("Available keys:")
print(data.files)


print("\nMotion information:")

for key in data.files:
    value = data[key]

    if hasattr(value, "shape"):
        print(f"{key}: {value.shape}")
    else:
        print(f"{key}: {value}")