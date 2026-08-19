from pathlib import Path
import numpy as np


# ------------------------------------------------------------
# Project root
#
# scripts/
#     04_inspect_normalized_npz.py
#
# parent  -> 03_human_data
# parent  -> 04_latent_objective_learning
# ------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent


# ------------------------------------------------------------
# Normalized NPZ
# ------------------------------------------------------------

path = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "normalized"
    / "ACCAD"
    / "Female1General_c3d"
    / "A1 - Stand_poses.npz"
)


# ------------------------------------------------------------
# Check file
# ------------------------------------------------------------

print("=" * 70)
print("PROJECT ROOT:")
print(PROJECT_ROOT)

print("\nFILE:")
print(path)

print("=" * 70)


if not path.exists():
    raise FileNotFoundError(
        f"File not found:\n{path}"
    )


# ------------------------------------------------------------
# Inspect NPZ
# ------------------------------------------------------------

with np.load(path, allow_pickle=False) as data:

    print("\nKEYS:")

    for key in data.files:

        value = data[key]

        print(
            f"{key:40s}"
            f" shape={str(value.shape):20s}"
            f" dtype={value.dtype}"
        )

    print("\n" + "=" * 70)