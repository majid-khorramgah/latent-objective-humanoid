from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

import numpy as np


# ============================================================
# Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_ROOT = PROJECT_ROOT / "data" / "processed" / "smplx"
OUTPUT_ROOT = PROJECT_ROOT / "data" / "processed" / "joints"

METADATA_DIR = PROJECT_ROOT / "results" / "statistics"

JOINT_METADATA_FILE = METADATA_DIR / "smplx_joint_structure.json"


# ============================================================
# SMPL-X 127-joint structure
#
# The structure is derived from the actual SMPL-X model output:
#
#   55 LBS/regressed joints
#   + 21 extra vertex joints
#   + 51 facial landmarks
#   = 127 joints
#
# ============================================================


# ------------------------------------------------------------
# 1. Core body joints
# ------------------------------------------------------------
#
# These are the 22 joints used as the main human motion skeleton.
#
# They represent:
# pelvis
# lower body
# spine
# neck/head
# shoulders
# elbows
# wrists
#
# No eyes, jaw, fingers, or facial landmarks are included.
# ------------------------------------------------------------

BODY_CORE_NAMES = [
    "pelvis",
    "left_hip",
    "right_hip",
    "spine1",
    "left_knee",
    "right_knee",
    "spine2",
    "left_ankle",
    "right_ankle",
    "spine3",
    "left_foot",
    "right_foot",
    "neck",
    "left_collar",
    "right_collar",
    "head",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
]


# ------------------------------------------------------------
# 2. Foot contact joints
# ------------------------------------------------------------
#
# These are additional anatomical points useful for:
#
#   - foot-ground contact
#   - stance detection
#   - heel strike
#   - toe-off
#   - balance
#
# They are deliberately kept separate from BODY_CORE.
# ------------------------------------------------------------

BODY_CONTACT_NAMES = [
    "left_big_toe",
    "left_small_toe",
    "left_heel",
    "right_big_toe",
    "right_small_toe",
    "right_heel",
]


# ------------------------------------------------------------
# 3. Hand joints
# ------------------------------------------------------------
#
# 30 articulated finger joints:
#
#   left/right
#   index/middle/pinky/ring/thumb
#   three joints per finger
#
# + 10 fingertip points.
# ------------------------------------------------------------

HAND_JOINT_NAMES = [
    # Left index
    "left_index1",
    "left_index2",
    "left_index3",

    # Left middle
    "left_middle1",
    "left_middle2",
    "left_middle3",

    # Left pinky
    "left_pinky1",
    "left_pinky2",
    "left_pinky3",

    # Left ring
    "left_ring1",
    "left_ring2",
    "left_ring3",

    # Left thumb
    "left_thumb1",
    "left_thumb2",
    "left_thumb3",

    # Right index
    "right_index1",
    "right_index2",
    "right_index3",

    # Right middle
    "right_middle1",
    "right_middle2",
    "right_middle3",

    # Right pinky
    "right_pinky1",
    "right_pinky2",
    "right_pinky3",

    # Right ring
    "right_ring1",
    "right_ring2",
    "right_ring3",

    # Right thumb
    "right_thumb1",
    "right_thumb2",
    "right_thumb3",

    # Fingertips
    "left_thumb",
    "left_index",
    "left_middle",
    "left_ring",
    "left_pinky",

    "right_thumb",
    "right_index",
    "right_middle",
    "right_ring",
    "right_pinky",
]


# ------------------------------------------------------------
# 4. Face joints
# ------------------------------------------------------------
#
# Face information is preserved but separated from the main
# motion representation.
#
# This includes:
#
#   jaw
#   SMPL-X eye joints
#   nose
#   ears
#   51 facial landmarks
# ------------------------------------------------------------

FACE_BASE_NAMES = [
    "jaw",
    "left_eye_smplhf",
    "right_eye_smplhf",
    "nose",
    "right_eye",
    "left_eye",
    "right_ear",
    "left_ear",
]


# SMPL-X provides 51 facial landmarks.
#
# The actual semantic landmark names are model-version dependent.
# Therefore we keep their stable numerical identities rather than
# inventing anatomical names for them.

FACE_LANDMARK_NAMES = [
    f"face_landmark_{i:02d}"
    for i in range(51)
]


# ============================================================
# SMPL-X canonical 127 names
# ============================================================

SMPLX_55_NAMES = [
    "pelvis",
    "left_hip",
    "right_hip",
    "spine1",
    "left_knee",
    "right_knee",
    "spine2",
    "left_ankle",
    "right_ankle",
    "spine3",
    "left_foot",
    "right_foot",
    "neck",
    "left_collar",
    "right_collar",
    "head",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "jaw",
    "left_eye_smplhf",
    "right_eye_smplhf",
    "left_index1",
    "left_index2",
    "left_index3",
    "left_middle1",
    "left_middle2",
    "left_middle3",
    "left_pinky1",
    "left_pinky2",
    "left_pinky3",
    "left_ring1",
    "left_ring2",
    "left_ring3",
    "left_thumb1",
    "left_thumb2",
    "left_thumb3",
    "right_index1",
    "right_index2",
    "right_index3",
    "right_middle1",
    "right_middle2",
    "right_middle3",
    "right_pinky1",
    "right_pinky2",
    "right_pinky3",
    "right_ring1",
    "right_ring2",
    "right_ring3",
    "right_thumb1",
    "right_thumb2",
    "right_thumb3",
]


# ------------------------------------------------------------
# Extra joints added by VertexJointSelector
#
# Order is determined by the actual SMPL-X implementation.
# ------------------------------------------------------------

EXTRA_21_NAMES = [
    "nose",
    "right_eye",
    "left_eye",
    "right_ear",
    "left_ear",

    "left_big_toe",
    "left_small_toe",
    "left_heel",
    "right_big_toe",
    "right_small_toe",
    "right_heel",

    "left_thumb",
    "left_index",
    "left_middle",
    "left_ring",
    "left_pinky",

    "right_thumb",
    "right_index",
    "right_middle",
    "right_ring",
    "right_pinky",
]


# ============================================================
# Build canonical 127-joint list
# ============================================================

JOINT_NAMES_127 = (
    SMPLX_55_NAMES
    + EXTRA_21_NAMES
    + FACE_LANDMARK_NAMES
)

assert len(JOINT_NAMES_127) == 127


# ============================================================
# Index definitions
# ============================================================

# First 22 joints
BODY_CORE_INDICES = list(range(0, 22))

# Foot contact points inside the 127-joint output
#
# 55 + first 6 extra joints:
#   55 nose
#   56 right_eye
#   57 left_eye
#   58 right_ear
#   59 left_ear
#   60 left_big_toe
#   61 left_small_toe
#   62 left_heel
#   63 right_big_toe
#   64 right_small_toe
#   65 right_heel
#
BODY_CONTACT_INDICES = list(range(60, 66))

# Hand articulated joints:
# 25-54
HAND_ARTICULATED_INDICES = list(range(25, 55))

# Fingertips:
# 66-75
HAND_TIP_INDICES = list(range(66, 76))

HAND_INDICES = HAND_ARTICULATED_INDICES + HAND_TIP_INDICES

# Face:
#
# 22      jaw
# 23-24   SMPL-HF eyes
# 55-59   nose/eyes/ears
# 76-126  51 facial landmarks
#
FACE_INDICES = (
    [22, 23, 24]
    + list(range(55, 60))
    + list(range(76, 127))
)


# ============================================================
# Validation
# ============================================================

def validate_partition() -> None:
    """
    Verify that all 127 joints belong to exactly one category.
    """

    groups = {
        "body_core": set(BODY_CORE_INDICES),
        "body_contact": set(BODY_CONTACT_INDICES),
        "hands": set(HAND_INDICES),
        "face": set(FACE_INDICES),
    }

    all_indices = set()

    for name, indices in groups.items():

        overlap = all_indices.intersection(indices)

        if overlap:
            raise RuntimeError(
                f"Joint partition overlap in {name}: {sorted(overlap)}"
            )

        all_indices.update(indices)

    expected = set(range(127))

    missing = expected - all_indices
    extra = all_indices - expected

    if missing:
        raise RuntimeError(
            f"Missing joint indices: {sorted(missing)}"
        )

    if extra:
        raise RuntimeError(
            f"Invalid joint indices: {sorted(extra)}"
        )

    if len(all_indices) != 127:
        raise RuntimeError(
            f"Partition contains {len(all_indices)} joints, "
            f"expected 127."
        )


# ============================================================
# Metadata
# ============================================================

def build_metadata() -> Dict:

    validate_partition()

    groups = {
        "body_core": {
            "description": (
                "Primary whole-body motion skeleton. "
                "Used as the default motion representation."
            ),
            "indices": BODY_CORE_INDICES,
            "names": [
                JOINT_NAMES_127[i]
                for i in BODY_CORE_INDICES
            ],
        },

        "body_contact": {
            "description": (
                "Toe and heel points reserved for "
                "contact and locomotion analysis."
            ),
            "indices": BODY_CONTACT_INDICES,
            "names": [
                JOINT_NAMES_127[i]
                for i in BODY_CONTACT_INDICES
            ],
        },

        "hands": {
            "description": (
                "Articulated finger joints and fingertips. "
                "Preserved for future manipulation and "
                "hand-object interaction objectives."
            ),
            "indices": HAND_INDICES,
            "names": [
                JOINT_NAMES_127[i]
                for i in HAND_INDICES
            ],
        },

        "face": {
            "description": (
                "Facial joints and facial landmarks. "
                "Preserved but excluded from the default "
                "body-motion representation."
            ),
            "indices": FACE_INDICES,
            "names": [
                JOINT_NAMES_127[i]
                for i in FACE_INDICES
            ],
        },
    }

    metadata = {
        "schema_version": "stage03-joint-extraction-v1",

        "model": "SMPL-X",

        "total_joints": 127,

        "source_structure": {
            "smplx_regressed_joints": 55,
            "vertex_selector_extra_joints": 21,
            "facial_landmarks": 51,
            "total": 127,
        },

        "partition": {
            "body_core": 22,
            "body_contact": 6,
            "hands": 40,
            "face": 59,
            "total": 127,
        },

        "groups": groups,

        "joint_names": JOINT_NAMES_127,

        "future_ablation_options": {
            "core_only": BODY_CORE_INDICES,
            "core_plus_contact": (
                BODY_CORE_INDICES
                + BODY_CONTACT_INDICES
            ),
            "core_plus_hands": (
                BODY_CORE_INDICES
                + HAND_INDICES
            ),
            "core_plus_contact_plus_hands": (
                BODY_CORE_INDICES
                + BODY_CONTACT_INDICES
                + HAND_INDICES
            ),
            "full_body_127": list(range(127)),
        },
    }

    return metadata


# ============================================================
# Save metadata
# ============================================================

def save_metadata() -> None:

    METADATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    metadata = build_metadata()

    with open(
        JOINT_METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            metadata,
            f,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"[OK] Joint metadata saved: "
        f"{JOINT_METADATA_FILE}"
    )


# ============================================================
# NPZ loading
# ============================================================

def load_joints(npz_path: Path) -> np.ndarray:
    """
    Load reconstructed SMPL-X joints.

    The reconstruction stage may store joints under:
        joints
        joint_positions
        joint_xyz

    This function accepts these common names.
    """

    data = np.load(
        npz_path,
        allow_pickle=False
    )

    possible_keys = [
        "joints",
        "joint_positions",
        "joint_xyz",
    ]

    for key in possible_keys:

        if key in data:

            joints = data[key]

            break

    else:

        raise KeyError(
            f"No joint array found in {npz_path}. "
            f"Available keys: {data.files}"
        )

    joints = np.asarray(
        joints,
        dtype=np.float32
    )

    if joints.ndim != 3:
        raise ValueError(
            f"Expected [T, J, 3], got {joints.shape} "
            f"in {npz_path}"
        )

    if joints.shape[1] != 127:
        raise ValueError(
            f"Expected 127 joints, got "
            f"{joints.shape[1]} in {npz_path}"
        )

    if joints.shape[2] != 3:
        raise ValueError(
            f"Expected XYZ coordinates, got "
            f"{joints.shape} in {npz_path}"
        )

    return joints


# ============================================================
# Extract groups
# ============================================================

def extract_groups(
    joints: np.ndarray
) -> Dict[str, np.ndarray]:

    return {
        "body_core": joints[:, BODY_CORE_INDICES, :],

        "body_contact": joints[:, BODY_CONTACT_INDICES, :],

        "hands": joints[:, HAND_INDICES, :],

        "face": joints[:, FACE_INDICES, :],

        "full": joints,
    }


# ============================================================
# Process one file
# ============================================================

def process_file(
    input_path: Path,
    output_path: Path
) -> None:

    joints = load_joints(input_path)

    groups = extract_groups(joints)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    np.savez_compressed(
        output_path,

        # Complete original representation
        full=groups["full"],

        # Main motion representation
        body_core=groups["body_core"],

        # Contact-related points
        body_contact=groups["body_contact"],

        # Hands
        hands=groups["hands"],

        # Face
        face=groups["face"],
    )

    print(
        f"[OK] {input_path} -> {output_path}"
    )


# ============================================================
# Process dataset
# ============================================================

def process_all() -> None:

    if not INPUT_ROOT.exists():

        raise FileNotFoundError(
            f"Input directory does not exist:\n"
            f"{INPUT_ROOT}"
        )

    files = sorted(
        INPUT_ROOT.rglob("*.npz")
    )

    print(
        f"Found {len(files)} reconstructed files."
    )

    success = 0
    failed = 0

    for input_path in files:

        relative = input_path.relative_to(
            INPUT_ROOT
        )

        output_path = (
            OUTPUT_ROOT / relative
        )

        try:

            process_file(
                input_path,
                output_path
            )

            success += 1

        except Exception as exc:

            failed += 1

            print(
                f"[FAILED] {input_path}\n"
                f"         {type(exc).__name__}: {exc}"
            )

    print()
    print("=" * 70)
    print("JOINT EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"Input files : {len(files)}")
    print(f"Successful  : {success}")
    print(f"Failed      : {failed}")
    print(f"Output      : {OUTPUT_ROOT}")
    print(f"Metadata    : {JOINT_METADATA_FILE}")
    print("=" * 70)


# ============================================================
# Main
# ============================================================

if __name__ == "__main__":

    save_metadata()

    process_all()