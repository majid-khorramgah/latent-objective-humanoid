#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
04_visualize_normalization.py

Visual validation of SMPL-X 127-joint normalization.

Purpose
-------
Compare:
    raw canonical SMPL-X 127
vs.
    normalized canonical SMPL-X 127

The script does NOT modify any input files.

Expected input structure
------------------------
data/
└── processed/
    ├── joints/
    │   └── <dataset>/<sequence>.npz
    │
    └── normalized/
        └── <dataset>/<sequence>.npz

Expected NPZ keys
-----------------
Input joints:
    full         -> (T, 127, 3)

Normalized:
    full         -> (T, 127, 3)

Outputs
-------
data/processed/normalization_visualization/
    <dataset>/<sequence>/
        frame_XXXX_original.png
        frame_XXXX_normalized.png
        frame_XXXX_comparison.png
        frame_XXXX_overlay.png
        animation_original.gif
        animation_normalized.gif
        animation_comparison.gif
        bone_length_comparison.png
        validation_report.json
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

import matplotlib

# Headless-safe backend.
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# ============================================================================
# PROJECT CONFIGURATION
# ============================================================================

SCRIPT_NAME = "04_visualize_normalization"

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_ROOT = PROJECT_ROOT / "data" / "processed"

JOINTS_ROOT = DATA_ROOT / "joints"

NORMALIZED_ROOT = DATA_ROOT / "normalized"

OUTPUT_ROOT = DATA_ROOT / "normalization_visualization"


# ============================================================================
# SMPL-X 127 STRUCTURE
# ============================================================================

NUM_JOINTS = 127


# ---------------------------------------------------------------------------
# Kinematic joints: 0 ... 54
# ---------------------------------------------------------------------------

JOINT_NAMES = {
    0: "Pelvis",

    1: "L_Hip",
    2: "R_Hip",

    3: "Spine1",

    4: "L_Knee",
    5: "R_Knee",

    6: "Spine2",

    7: "L_Ankle",
    8: "R_Ankle",

    9: "Spine3",

    10: "L_Foot",
    11: "R_Foot",

    12: "Neck",

    13: "L_Collar",
    14: "R_Collar",

    15: "Head",

    16: "L_Shoulder",
    17: "R_Shoulder",

    18: "L_Elbow",
    19: "R_Elbow",

    20: "L_Wrist",
    21: "R_Wrist",

    22: "Jaw",
    23: "L_Eye",
    24: "R_Eye",

    25: "L_Index1",
    26: "L_Index2",
    27: "L_Index3",

    28: "L_Middle1",
    29: "L_Middle2",
    30: "L_Middle3",

    31: "L_Pinky1",
    32: "L_Pinky2",
    33: "L_Pinky3",

    34: "L_Ring1",
    35: "L_Ring2",
    36: "L_Ring3",

    37: "L_Thumb1",
    38: "L_Thumb2",
    39: "L_Thumb3",

    40: "R_Index1",
    41: "R_Index2",
    42: "R_Index3",

    43: "R_Middle1",
    44: "R_Middle2",
    45: "R_Middle3",

    46: "R_Pinky1",
    47: "R_Pinky2",
    48: "R_Pinky3",

    49: "R_Ring1",
    50: "R_Ring2",
    51: "R_Ring3",

    52: "R_Thumb1",
    53: "R_Thumb2",
    54: "R_Thumb3",
}


# ---------------------------------------------------------------------------
# Extra vertex joints: 55 ... 75
# ---------------------------------------------------------------------------

EXTRA_JOINT_NAMES = {
    55: "Nose",
    56: "R_Eye_Keypoint",
    57: "L_Eye_Keypoint",
    58: "R_Ear",
    59: "L_Ear",

    60: "L_BigToe",
    61: "L_SmallToe",
    62: "L_Heel",

    63: "R_BigToe",
    64: "R_SmallToe",
    65: "R_Heel",

    66: "L_Thumb_Tip",
    67: "L_Index_Tip",
    68: "L_Middle_Tip",
    69: "L_Ring_Tip",
    70: "L_Pinky_Tip",

    71: "R_Thumb_Tip",
    72: "R_Index_Tip",
    73: "R_Middle_Tip",
    74: "R_Ring_Tip",
    75: "R_Pinky_Tip",
}


# ---------------------------------------------------------------------------
# Facial landmarks: 76 ... 126
# ---------------------------------------------------------------------------

FACE_LANDMARK_NAMES = {
    76: "right_eye_brow1",
    77: "right_eye_brow2",
    78: "right_eye_brow3",
    79: "right_eye_brow4",
    80: "right_eye_brow5",

    81: "left_eye_brow5",
    82: "left_eye_brow4",
    83: "left_eye_brow3",
    84: "left_eye_brow2",
    85: "left_eye_brow1",

    86: "nose1",
    87: "nose2",
    88: "nose3",
    89: "nose4",

    90: "right_nose_2",
    91: "right_nose_1",
    92: "nose_middle",
    93: "left_nose_1",
    94: "left_nose_2",

    95: "right_eye1",
    96: "right_eye2",
    97: "right_eye3",
    98: "right_eye4",
    99: "right_eye5",
    100: "right_eye6",

    101: "left_eye4",
    102: "left_eye3",
    103: "left_eye2",
    104: "left_eye1",
    105: "left_eye6",
    106: "left_eye5",

    107: "right_mouth_1",
    108: "right_mouth_2",
    109: "right_mouth_3",
    110: "mouth_top",
    111: "left_mouth_3",
    112: "left_mouth_2",
    113: "left_mouth_1",

    114: "left_mouth_5",
    115: "left_mouth_4",
    116: "mouth_bottom",

    117: "right_mouth_4",
    118: "right_mouth_5",

    119: "right_lip_1",
    120: "right_lip_2",
    121: "lip_top",
    122: "left_lip_2",
    123: "left_lip_1",
    124: "left_lip_3",
    125: "lip_bottom",
    126: "right_lip_3",
}


ALL_JOINT_NAMES = {}

ALL_JOINT_NAMES.update(JOINT_NAMES)
ALL_JOINT_NAMES.update(EXTRA_JOINT_NAMES)
ALL_JOINT_NAMES.update(FACE_LANDMARK_NAMES)


# ============================================================================
# KINEMATIC PARENTS
# ============================================================================

PARENTS = np.array(
    [
        -1,
        0,
        0,
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        9,
        9,
        12,
        13,
        14,
        16,
        17,
        18,
        19,
        15,
        15,
        15,
        20,
        25,
        26,
        20,
        28,
        29,
        20,
        31,
        32,
        20,
        34,
        35,
        20,
        37,
        38,
        21,
        40,
        41,
        21,
        43,
        44,
        21,
        46,
        47,
        21,
        49,
        50,
        21,
        52,
        53,
    ],
    dtype=np.int64,
)


# ============================================================================
# REPRESENTATION GROUPS
# ============================================================================

BODY_CORE = [
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
    16,
    17,
    18,
    19,
    20,
    21,
]


BODY_CONTACT = [
    60,
    61,
    62,
    63,
    64,
    65,
]


HAND_INDICES = (
    list(range(25, 40))
    + list(range(40, 55))
    + list(range(66, 76))
)


FACE_INDICES = (
    [22, 23, 24]
    + [55, 56, 57, 58, 59]
    + list(range(76, 127))
)


# ============================================================================
# VISUALIZATION EDGES
# ============================================================================

# Core body skeleton.
BODY_EDGES = [
    (0, 1),   # pelvis -> L hip
    (0, 2),   # pelvis -> R hip
    (0, 3),   # pelvis -> spine1

    (1, 4),   # L hip -> L knee
    (4, 7),   # L knee -> L ankle
    (7, 10),  # L ankle -> L foot

    (2, 5),   # R hip -> R knee
    (5, 8),   # R knee -> R ankle
    (8, 11),  # R ankle -> R foot

    (3, 6),   # spine1 -> spine2
    (6, 9),   # spine2 -> spine3
    (9, 12),  # spine3 -> neck
    (12, 15), # neck -> head

    (9, 13),  # spine3 -> L collar
    (13, 16), # L collar -> L shoulder
    (16, 18), # L shoulder -> L elbow
    (18, 20), # L elbow -> L wrist

    (9, 14),  # spine3 -> R collar
    (14, 17), # R collar -> R shoulder
    (17, 19), # R shoulder -> R elbow
    (19, 21), # R elbow -> R wrist

    (15, 22), # head -> jaw
    (15, 23), # head -> L eye
    (15, 24), # head -> R eye
]


# Fingers.
HAND_EDGES = [
    # Left index
    (20, 25),
    (25, 26),
    (26, 27),
    (27, 67),

    # Left middle
    (20, 28),
    (28, 29),
    (29, 30),
    (30, 68),

    # Left pinky
    (20, 31),
    (31, 32),
    (32, 33),
    (33, 70),

    # Left ring
    (20, 34),
    (34, 35),
    (35, 36),
    (36, 69),

    # Left thumb
    (20, 37),
    (37, 38),
    (38, 39),
    (39, 66),

    # Right index
    (21, 40),
    (40, 41),
    (41, 42),
    (42, 72),

    # Right middle
    (21, 43),
    (43, 44),
    (44, 45),
    (45, 73),

    # Right pinky
    (21, 46),
    (46, 47),
    (47, 48),
    (48, 75),

    # Right ring
    (21, 49),
    (49, 50),
    (50, 51),
    (51, 74),

    # Right thumb
    (21, 52),
    (52, 53),
    (53, 54),
    (54, 71),
]


# Feet/contact edges.
FOOT_EDGES = [
    (10, 60),
    (10, 61),
    (10, 62),

    (11, 63),
    (11, 64),
    (11, 65),
]


# Face keypoint edges.
FACE_EDGES = [
    (15, 55),
    (23, 57),
    (24, 56),
    (55, 58),
    (55, 59),
]


# All visualization edges.
ALL_EDGES = BODY_EDGES + HAND_EDGES + FOOT_EDGES + FACE_EDGES


# ============================================================================
# LOGGING
# ============================================================================

def log(message: str) -> None:
    print(f"[{SCRIPT_NAME}] {message}")


def warn(message: str) -> None:
    print(f"[WARNING] {message}")


def error(message: str) -> None:
    print(f"[ERROR] {message}")


# ============================================================================
# ARGUMENTS
# ============================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Visually validate SMPL-X 127 normalization."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of NPZ sequences to inspect.",
    )

    parser.add_argument(
        "--frames",
        type=int,
        default=5,
        help="Number of representative frames per sequence.",
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=20,
        help="GIF frame rate.",
    )

    parser.add_argument(
        "--animation-frames",
        type=int,
        default=80,
        help="Maximum number of frames used in GIF animation.",
    )

    parser.add_argument(
        "--no-gif",
        action="store_true",
        help="Do not create GIF animations.",
    )

    parser.add_argument(
        "--no-face",
        action="store_true",
        help="Do not visualize facial landmarks.",
    )

    parser.add_argument(
        "--no-hands",
        action="store_true",
        help="Do not visualize hand joints.",
    )

    parser.add_argument(
        "--show-all-joints",
        action="store_true",
        help="Draw all 127 joints as points.",
    )

    return parser.parse_args()


# ============================================================================
# FILE DISCOVERY
# ============================================================================

def find_input_files(limit: int) -> List[Path]:
    files = sorted(JOINTS_ROOT.rglob("*.npz"))

    # Do not treat summaries or unrelated files as sequence files.
    files = [
        p
        for p in files
        if p.name != "_normalization_summary.json"
    ]

    if limit > 0:
        files = files[:limit]

    return files


def normalized_path_for(input_path: Path) -> Path:
    relative = input_path.relative_to(JOINTS_ROOT)
    return NORMALIZED_ROOT / relative


def output_dir_for(input_path: Path) -> Path:
    relative = input_path.relative_to(JOINTS_ROOT)
    return OUTPUT_ROOT / relative.parent / relative.stem


# ============================================================================
# NPZ LOADING
# ============================================================================

def load_full_tensor(path: Path) -> np.ndarray:
    with np.load(path, allow_pickle=True) as data:
        if "full" not in data.files:
            raise KeyError(
                f"Canonical key 'full' not found. "
                f"Available keys: {data.files}"
            )

        joints = np.asarray(data["full"])

    if joints.ndim != 3:
        raise ValueError(
            f"Expected 3D tensor (T,J,3), got shape={joints.shape}"
        )

    if joints.shape[1] != NUM_JOINTS:
        raise ValueError(
            f"Expected {NUM_JOINTS} joints, got {joints.shape[1]}"
        )

    if joints.shape[2] != 3:
        raise ValueError(
            f"Expected XYZ dimension of 3, got {joints.shape[2]}"
        )

    return joints.astype(np.float64, copy=False)


# ============================================================================
# REPRESENTATIVE FRAMES
# ============================================================================

def representative_frames(
    num_frames: int,
    requested: int,
) -> List[int]:

    if num_frames <= 0:
        return []

    if requested <= 1:
        return [0]

    if num_frames == 1:
        return [0]

    # Evenly distributed frames including first and last.
    values = np.linspace(
        0,
        num_frames - 1,
        requested,
    )

    indices = sorted(
        set(int(round(v)) for v in values)
    )

    return indices


# ============================================================================
# GEOMETRY
# ============================================================================

def pelvis_center(joints: np.ndarray) -> np.ndarray:
    """
    Returns pelvis position for every frame.

    Shape:
        (T, 3)
    """
    return joints[:, 0, :]


def root_centered_copy(joints: np.ndarray) -> np.ndarray:
    """
    Root-center an already normalized/raw sequence.

    This is only used for diagnostics.
    """
    root = pelvis_center(joints)

    return joints - root[:, None, :]


def compute_bone_lengths(
    joints: np.ndarray,
    edges: List[Tuple[int, int]],
) -> np.ndarray:

    if not edges:
        return np.empty((joints.shape[0], 0))

    lengths = []

    for a, b in edges:
        delta = joints[:, a, :] - joints[:, b, :]
        length = np.linalg.norm(delta, axis=-1)
        lengths.append(length)

    return np.stack(lengths, axis=1)


def compute_scale_ratio(
    original: np.ndarray,
    normalized: np.ndarray,
) -> np.ndarray:

    orig_lengths = compute_bone_lengths(
        original,
        BODY_EDGES,
    )

    norm_lengths = compute_bone_lengths(
        normalized,
        BODY_EDGES,
    )

    valid = orig_lengths > 1e-12

    ratios = np.full_like(
        norm_lengths,
        np.nan,
        dtype=np.float64,
    )

    ratios[valid] = (
        norm_lengths[valid]
        / orig_lengths[valid]
    )

    return ratios


# ============================================================================
# AXIS LIMITS
# ============================================================================

def calculate_equal_limits(
    points: np.ndarray,
    padding: float = 0.08,
) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:

    finite = points[np.isfinite(points).all(axis=1)]

    if len(finite) == 0:
        return (
            (-1.0, 1.0),
            (-1.0, 1.0),
            (-1.0, 1.0),
        )

    minimum = finite.min(axis=0)
    maximum = finite.max(axis=0)

    center = (minimum + maximum) / 2.0

    radius = np.max(maximum - minimum) / 2.0

    if radius < 1e-8:
        radius = 1.0

    radius *= (1.0 + padding)

    return (
        (center[0] - radius, center[0] + radius),
        (center[1] - radius, center[1] + radius),
        (center[2] - radius, center[2] + radius),
    )


def set_equal_3d_axes(
    ax,
    points: np.ndarray,
) -> None:

    xlim, ylim, zlim = calculate_equal_limits(points)

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_zlim(*zlim)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Equal physical aspect ratio.
    try:
        ax.set_box_aspect(
            (
                xlim[1] - xlim[0],
                ylim[1] - ylim[0],
                zlim[1] - zlim[0],
            )
        )
    except Exception:
        pass


# ============================================================================
# SKELETON DRAWING
# ============================================================================

def draw_skeleton(
    ax,
    joints: np.ndarray,
    *,
    draw_hands: bool = True,
    draw_face: bool = True,
    draw_all_joints: bool = False,
) -> None:

    # ------------------------------------------------------------------------
    # Body
    # ------------------------------------------------------------------------

    for a, b in BODY_EDGES:

        ax.plot(
            [joints[a, 0], joints[b, 0]],
            [joints[a, 1], joints[b, 1]],
            [joints[a, 2], joints[b, 2]],
            linewidth=1.8,
        )

    # Core body points.
    body_points = joints[BODY_CORE]

    ax.scatter(
        body_points[:, 0],
        body_points[:, 1],
        body_points[:, 2],
        s=14,
    )

    # ------------------------------------------------------------------------
    # Feet
    # ------------------------------------------------------------------------

    for a, b in FOOT_EDGES:

        ax.plot(
            [joints[a, 0], joints[b, 0]],
            [joints[a, 1], joints[b, 1]],
            [joints[a, 2], joints[b, 2]],
            linewidth=1.5,
        )

    feet = joints[BODY_CONTACT]

    ax.scatter(
        feet[:, 0],
        feet[:, 1],
        feet[:, 2],
        s=22,
    )

    # ------------------------------------------------------------------------
    # Hands
    # ------------------------------------------------------------------------

    if draw_hands:

        for a, b in HAND_EDGES:

            ax.plot(
                [joints[a, 0], joints[b, 0]],
                [joints[a, 1], joints[b, 1]],
                [joints[a, 2], joints[b, 2]],
                linewidth=0.9,
            )

        hands = joints[HAND_INDICES]

        ax.scatter(
            hands[:, 0],
            hands[:, 1],
            hands[:, 2],
            s=7,
        )

    # ------------------------------------------------------------------------
    # Face
    # ------------------------------------------------------------------------

    if draw_face:

        for a, b in FACE_EDGES:

            ax.plot(
                [joints[a, 0], joints[b, 0]],
                [joints[a, 1], joints[b, 1]],
                [joints[a, 2], joints[b, 2]],
                linewidth=1.0,
            )

        face_points = joints[FACE_INDICES]

        ax.scatter(
            face_points[:, 0],
            face_points[:, 1],
            face_points[:, 2],
            s=5,
        )

    # ------------------------------------------------------------------------
    # Optional all 127 points
    # ------------------------------------------------------------------------

    if draw_all_joints:

        ax.scatter(
            joints[:, 0],
            joints[:, 1],
            joints[:, 2],
            s=4,
        )


# ============================================================================
# STATIC FRAME VISUALIZATION
# ============================================================================

def save_frame_comparison(
    original: np.ndarray,
    normalized: np.ndarray,
    frame_index: int,
    output_dir: Path,
    *,
    draw_hands: bool,
    draw_face: bool,
    draw_all_joints: bool,
) -> None:

    orig = original[frame_index]
    norm = normalized[frame_index]

    combined = np.concatenate(
        [orig, norm],
        axis=0,
    )

    limits = calculate_equal_limits(combined)

    # ------------------------------------------------------------------------
    # Original
    # ------------------------------------------------------------------------

    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(111, projection="3d")

    draw_skeleton(
        ax,
        orig,
        draw_hands=draw_hands,
        draw_face=draw_face,
        draw_all_joints=draw_all_joints,
    )

    ax.set_title(
        f"Original SMPL-X 127 | Frame {frame_index}"
    )

    ax.set_xlim(*limits[0])
    ax.set_ylim(*limits[1])
    ax.set_zlim(*limits[2])

    fig.tight_layout()

    fig.savefig(
        output_dir / f"frame_{frame_index:04d}_original.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    # ------------------------------------------------------------------------
    # Normalized
    # ------------------------------------------------------------------------

    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(111, projection="3d")

    draw_skeleton(
        ax,
        norm,
        draw_hands=draw_hands,
        draw_face=draw_face,
        draw_all_joints=draw_all_joints,
    )

    ax.set_title(
        f"Normalized SMPL-X 127 | Frame {frame_index}"
    )

    ax.set_xlim(*limits[0])
    ax.set_ylim(*limits[1])
    ax.set_zlim(*limits[2])

    fig.tight_layout()

    fig.savefig(
        output_dir / f"frame_{frame_index:04d}_normalized.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    # ------------------------------------------------------------------------
    # Side-by-side
    # ------------------------------------------------------------------------

    fig = plt.figure(figsize=(16, 8))

    ax1 = fig.add_subplot(
        121,
        projection="3d",
    )

    ax2 = fig.add_subplot(
        122,
        projection="3d",
    )

    draw_skeleton(
        ax1,
        orig,
        draw_hands=draw_hands,
        draw_face=draw_face,
        draw_all_joints=draw_all_joints,
    )

    draw_skeleton(
        ax2,
        norm,
        draw_hands=draw_hands,
        draw_face=draw_face,
        draw_all_joints=draw_all_joints,
    )

    ax1.set_title(
        f"Original | Frame {frame_index}"
    )

    ax2.set_title(
        f"Normalized | Frame {frame_index}"
    )

    for ax in (ax1, ax2):

        ax.set_xlim(*limits[0])
        ax.set_ylim(*limits[1])
        ax.set_zlim(*limits[2])

    fig.suptitle(
        "SMPL-X 127 Normalization Validation"
    )

    fig.tight_layout()

    fig.savefig(
        output_dir / f"frame_{frame_index:04d}_comparison.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)


# ============================================================================
# OVERLAY VISUALIZATION
# ============================================================================

def save_overlay(
    original: np.ndarray,
    normalized: np.ndarray,
    frame_index: int,
    output_dir: Path,
    *,
    draw_hands: bool,
    draw_face: bool,
) -> None:

    orig = original[frame_index]
    norm = normalized[frame_index]

    points = np.concatenate(
        [orig, norm],
        axis=0,
    )

    limits = calculate_equal_limits(points)

    fig = plt.figure(figsize=(9, 9))

    ax = fig.add_subplot(
        111,
        projection="3d",
    )

    # Original skeleton.
    for a, b in ALL_EDGES:

        if not draw_hands and (a, b) in HAND_EDGES:
            continue

        if not draw_face and (a, b) in FACE_EDGES:
            continue

        ax.plot(
            [orig[a, 0], orig[b, 0]],
            [orig[a, 1], orig[b, 1]],
            [orig[a, 2], orig[b, 2]],
            linewidth=1.3,
        )

    # Normalized skeleton.
    for a, b in ALL_EDGES:

        if not draw_hands and (a, b) in HAND_EDGES:
            continue

        if not draw_face and (a, b) in FACE_EDGES:
            continue

        ax.plot(
            [norm[a, 0], norm[b, 0]],
            [norm[a, 1], norm[b, 1]],
            [norm[a, 2], norm[b, 2]],
            linestyle="--",
            linewidth=1.0,
        )

    # Show root positions.
    ax.scatter(
        [orig[0, 0]],
        [orig[0, 1]],
        [orig[0, 2]],
        s=40,
    )

    ax.scatter(
        [norm[0, 0]],
        [norm[0, 1]],
        [norm[0, 2]],
        s=40,
    )

    ax.set_title(
        f"Original vs Normalized Overlay | Frame {frame_index}"
    )

    ax.set_xlim(*limits[0])
    ax.set_ylim(*limits[1])
    ax.set_zlim(*limits[2])

    fig.tight_layout()

    fig.savefig(
        output_dir / f"frame_{frame_index:04d}_overlay.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)


# ============================================================================
# ANIMATION
# ============================================================================

def create_animation(
    joints: np.ndarray,
    output_path: Path,
    title: str,
    *,
    max_frames: int,
    fps: int,
    draw_hands: bool,
    draw_face: bool,
) -> None:

    total_frames = joints.shape[0]

    if total_frames <= max_frames:
        indices = np.arange(total_frames)
    else:
        indices = np.linspace(
            0,
            total_frames - 1,
            max_frames,
        ).round().astype(int)

    # Determine stable axis limits from the full sampled sequence.
    sampled = joints[indices]

    flat = sampled.reshape(-1, 3)

    limits = calculate_equal_limits(flat)

    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_subplot(
        111,
        projection="3d",
    )

    def update(frame_number: int):

        ax.cla()

        frame_index = int(indices[frame_number])

        draw_skeleton(
            ax,
            joints[frame_index],
            draw_hands=draw_hands,
            draw_face=draw_face,
        )

        ax.set_title(
            f"{title}\nFrame {frame_index}/{total_frames - 1}"
        )

        ax.set_xlim(*limits[0])
        ax.set_ylim(*limits[1])
        ax.set_zlim(*limits[2])

        return []

    animation = FuncAnimation(
        fig,
        update,
        frames=len(indices),
        interval=1000 / max(fps, 1),
        blit=False,
    )

    writer = PillowWriter(
        fps=max(fps, 1)
    )

    animation.save(
        output_path,
        writer=writer,
    )

    plt.close(fig)


# ============================================================================
# BONE LENGTH VALIDATION
# ============================================================================

def save_bone_length_comparison(
    original: np.ndarray,
    normalized: np.ndarray,
    output_dir: Path,
) -> Dict:

    original_lengths = compute_bone_lengths(
        original,
        BODY_EDGES,
    )

    normalized_lengths = compute_bone_lengths(
        normalized,
        BODY_EDGES,
    )

    # Mean bone length over time.
    orig_mean = np.mean(
        original_lengths,
        axis=0,
    )

    norm_mean = np.mean(
        normalized_lengths,
        axis=0,
    )

    ratio = np.divide(
        norm_mean,
        orig_mean,
        out=np.full_like(norm_mean, np.nan),
        where=orig_mean > 1e-12,
    )

    # Plot.
    x = np.arange(len(BODY_EDGES))

    fig = plt.figure(figsize=(14, 6))

    ax = fig.add_subplot(111)

    ax.plot(
        x,
        orig_mean,
        marker="o",
        label="Original",
    )

    ax.plot(
        x,
        norm_mean,
        marker="x",
        label="Normalized",
    )

    ax.set_xlabel("Body bone edge index")
    ax.set_ylabel("Mean bone length")
    ax.set_title(
        "Mean Body Bone Length: Original vs Normalized"
    )

    ax.legend()

    fig.tight_layout()

    fig.savefig(
        output_dir / "bone_length_comparison.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    # Summary.
    valid = np.isfinite(ratio)

    if np.any(valid):

        ratio_valid = ratio[valid]

        summary = {
            "mean_scale_ratio": float(
                np.mean(ratio_valid)
            ),
            "median_scale_ratio": float(
                np.median(ratio_valid)
            ),
            "min_scale_ratio": float(
                np.min(ratio_valid)
            ),
            "max_scale_ratio": float(
                np.max(ratio_valid)
            ),
            "std_scale_ratio": float(
                np.std(ratio_valid)
            ),
        }

    else:

        summary = {
            "mean_scale_ratio": None,
            "median_scale_ratio": None,
            "min_scale_ratio": None,
            "max_scale_ratio": None,
            "std_scale_ratio": None,
        }

    return summary


# ============================================================================
# NUMERICAL VALIDATION
# ============================================================================

def numerical_validation(
    original: np.ndarray,
    normalized: np.ndarray,
) -> Dict:

    result = {
        "original_shape": list(original.shape),
        "normalized_shape": list(normalized.shape),
        "joint_count_preserved": (
            original.shape[1] == NUM_JOINTS
            and normalized.shape[1] == NUM_JOINTS
        ),
        "frame_count_preserved": (
            original.shape[0] == normalized.shape[0]
        ),
        "xyz_dimension_preserved": (
            original.shape[2] == 3
            and normalized.shape[2] == 3
        ),
        "original_finite": bool(
            np.isfinite(original).all()
        ),
        "normalized_finite": bool(
            np.isfinite(normalized).all()
        ),
    }

    # ------------------------------------------------------------------------
    # Root positions.
    # ------------------------------------------------------------------------

    original_root = original[:, 0, :]
    normalized_root = normalized[:, 0, :]

    result["original_root_mean"] = (
        np.mean(original_root, axis=0).tolist()
    )

    result["normalized_root_mean"] = (
        np.mean(normalized_root, axis=0).tolist()
    )

    result["normalized_root_abs_max"] = float(
        np.max(np.abs(normalized_root))
    )

    result["normalized_root_mean_abs"] = float(
        np.mean(np.abs(normalized_root))
    )

    # ------------------------------------------------------------------------
    # Body bone scale.
    # ------------------------------------------------------------------------

    ratios = compute_scale_ratio(
        original,
        normalized,
    )

    valid = np.isfinite(ratios)

    if np.any(valid):

        valid_ratios = ratios[valid]

        result["bone_scale_ratio_mean"] = float(
            np.mean(valid_ratios)
        )

        result["bone_scale_ratio_median"] = float(
            np.median(valid_ratios)
        )

        result["bone_scale_ratio_std"] = float(
            np.std(valid_ratios)
        )

        result["bone_scale_ratio_min"] = float(
            np.min(valid_ratios)
        )

        result["bone_scale_ratio_max"] = float(
            np.max(valid_ratios)
        )

    # ------------------------------------------------------------------------
    # Pairwise body shape preservation.
    #
    # Compare distances between selected core body joints.
    # The ratio should be approximately consistent with the applied
    # sequence-level scale.
    # ------------------------------------------------------------------------

    core = np.asarray(
        BODY_CORE,
        dtype=np.int64,
    )

    orig_core = original[:, core, :]
    norm_core = normalized[:, core, :]

    pair_errors = []

    for i in range(len(core)):

        for j in range(i + 1, len(core)):

            d_orig = np.linalg.norm(
                orig_core[:, i, :]
                - orig_core[:, j, :],
                axis=-1,
            )

            d_norm = np.linalg.norm(
                norm_core[:, i, :]
                - norm_core[:, j, :],
                axis=-1,
            )

            valid_pair = d_orig > 1e-8

            if np.any(valid_pair):

                ratio = (
                    d_norm[valid_pair]
                    / d_orig[valid_pair]
                )

                pair_errors.extend(
                    ratio.tolist()
                )

    if pair_errors:

        pair_errors = np.asarray(
            pair_errors,
            dtype=np.float64,
        )

        result["core_pair_distance_ratio_mean"] = float(
            np.mean(pair_errors)
        )

        result["core_pair_distance_ratio_std"] = float(
            np.std(pair_errors)
        )

        result["core_pair_distance_ratio_min"] = float(
            np.min(pair_errors)
        )

        result["core_pair_distance_ratio_max"] = float(
            np.max(pair_errors)
        )

    return result


# ============================================================================
# VALIDATION DECISION
# ============================================================================

def determine_status(
    report: Dict,
) -> str:

    checks = []

    checks.append(
        report["joint_count_preserved"]
    )

    checks.append(
        report["frame_count_preserved"]
    )

    checks.append(
        report["xyz_dimension_preserved"]
    )

    checks.append(
        report["original_finite"]
    )

    checks.append(
        report["normalized_finite"]
    )

    # Root should be close to zero after root-centering.
    root_max = report.get(
        "normalized_root_abs_max",
        math.inf,
    )

    checks.append(
        root_max < 1e-4
    )

    return "PASS" if all(checks) else "REVIEW"


# ============================================================================
# PROCESS ONE SEQUENCE
# ============================================================================

def process_sequence(
    input_path: Path,
    args: argparse.Namespace,
) -> Dict:

    normalized_path = normalized_path_for(
        input_path
    )

    output_dir = output_dir_for(
        input_path
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    log("=" * 70)

    log(f"Input      : {input_path}")

    log(f"Normalized : {normalized_path}")

    log(f"Output     : {output_dir}")

    # ------------------------------------------------------------------------
    # Check normalized file.
    # ------------------------------------------------------------------------

    if not normalized_path.exists():

        raise FileNotFoundError(
            f"Normalized file not found: "
            f"{normalized_path}"
        )

    # ------------------------------------------------------------------------
    # Load.
    # ------------------------------------------------------------------------

    original = load_full_tensor(
        input_path
    )

    normalized = load_full_tensor(
        normalized_path
    )

    log(
        f"Original shape   : {original.shape}"
    )

    log(
        f"Normalized shape : {normalized.shape}"
    )

    # ------------------------------------------------------------------------
    # Numerical validation.
    # ------------------------------------------------------------------------

    report = numerical_validation(
        original,
        normalized,
    )

    # ------------------------------------------------------------------------
    # Representative frames.
    # ------------------------------------------------------------------------

    frames = representative_frames(
        original.shape[0],
        args.frames,
    )

    log(
        f"Representative frames: {frames}"
    )

    # ------------------------------------------------------------------------
    # Static images.
    # ------------------------------------------------------------------------

    for frame_index in frames:

        save_frame_comparison(
            original,
            normalized,
            frame_index,
            output_dir,
            draw_hands=not args.no_hands,
            draw_face=not args.no_face,
            draw_all_joints=args.show_all_joints,
        )

        save_overlay(
            original,
            normalized,
            frame_index,
            output_dir,
            draw_hands=not args.no_hands,
            draw_face=not args.no_face,
        )

    # ------------------------------------------------------------------------
    # Bone length validation.
    # ------------------------------------------------------------------------

    bone_summary = save_bone_length_comparison(
        original,
        normalized,
        output_dir,
    )

    report["bone_length_summary"] = bone_summary

    # ------------------------------------------------------------------------
    # GIFs.
    # ------------------------------------------------------------------------

    if not args.no_gif:

        create_animation(
            original,
            output_dir / "animation_original.gif",
            "Original SMPL-X 127",
            max_frames=args.animation_frames,
            fps=args.fps,
            draw_hands=not args.no_hands,
            draw_face=not args.no_face,
        )

        create_animation(
            normalized,
            output_dir / "animation_normalized.gif",
            "Normalized SMPL-X 127",
            max_frames=args.animation_frames,
            fps=args.fps,
            draw_hands=not args.no_hands,
            draw_face=not args.no_face,
        )

    # ------------------------------------------------------------------------
    # Final status.
    # ------------------------------------------------------------------------

    status = determine_status(
        report
    )

    report["status"] = status

    report["input_file"] = str(
        input_path
    )

    report["normalized_file"] = str(
        normalized_path
    )

    report["representative_frames"] = frames

    report["canonical_representation"] = (
        "SMPL-X 127"
    )

    report["canonical_key"] = "full"

    report["body_core_joint_count"] = len(
        BODY_CORE
    )

    report["body_contact_joint_count"] = len(
        BODY_CONTACT
    )

    report["hand_joint_count"] = len(
        HAND_INDICES
    )

    report["face_joint_count"] = len(
        FACE_INDICES
    )

    report_path = (
        output_dir
        / "validation_report.json"
    )

    with report_path.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            report,
            f,
            indent=2,
            ensure_ascii=False,
        )

    log(
        f"Validation status: {status}"
    )

    log(
        f"Report saved: {report_path}"
    )

    return report


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:

    args = parse_args()

    print()
    log("=" * 78)
    log("04_visualize_normalization")
    log("=" * 78)

    log(
        f"Project root : {PROJECT_ROOT}"
    )

    log(
        f"Input root   : {JOINTS_ROOT}"
    )

    log(
        f"Normalized   : {NORMALIZED_ROOT}"
    )

    log(
        f"Output root  : {OUTPUT_ROOT}"
    )

    log(
        "Canonical representation: SMPL-X 127"
    )

    log(
        "Canonical tensor key: 'full'"
    )

    log(
        "Visualization: Original vs Normalized"
    )

    print()

    # ------------------------------------------------------------------------
    # Validate parent array.
    # ------------------------------------------------------------------------

    if len(PARENTS) != 55:

        raise RuntimeError(
            f"Expected 55 parents, got {len(PARENTS)}"
        )

    # ------------------------------------------------------------------------
    # Find files.
    # ------------------------------------------------------------------------

    files = find_input_files(
        args.limit
    )

    log(
        f"Found {len(files)} input NPZ files."
    )

    if not files:

        warn(
            "No NPZ files found."
        )

        return

    OUTPUT_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    processed = 0
    failed = 0

    results = []

    # ------------------------------------------------------------------------
    # Process.
    # ------------------------------------------------------------------------

    for index, input_path in enumerate(
        files,
        start=1,
    ):

        log(
            f"[{index}/{len(files)}]"
        )

        try:

            report = process_sequence(
                input_path,
                args,
            )

            processed += 1

            results.append(
                report
            )

        except Exception as exc:

            failed += 1

            error(
                f"FAILED: {input_path}"
            )

            error(
                f"Reason: {exc}"
            )

    # ------------------------------------------------------------------------
    # Global summary.
    # ------------------------------------------------------------------------

    summary = {
        "script": SCRIPT_NAME,
        "canonical_representation": "SMPL-X 127",
        "canonical_key": "full",
        "num_joints": NUM_JOINTS,
        "files_found": len(files),
        "processed": processed,
        "failed": failed,
        "results": results,
    }

    summary_path = (
        OUTPUT_ROOT
        / "_visualization_summary.json"
    )

    with summary_path.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            summary,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print()

    log("=" * 78)
    log("DONE")
    log("=" * 78)

    log(
        f"Processed : {processed}"
    )

    log(
        f"Failed    : {failed}"
    )

    log(
        f"Summary   : {summary_path}"
    )

    log("=" * 78)


if __name__ == "__main__":
    main()