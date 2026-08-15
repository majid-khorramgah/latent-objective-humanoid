"""
02_smplx_reconstruction.py

Stage 03 - Human Motion Processing
Project: latent-objective-humanoid

Purpose
-------
Reconstruct valid AMASS motion sequences using the SMPL-X body model
available in this project.

IMPORTANT REPRESENTATION NOTE
-----------------------------
AMASS uses an SMPL+H-style 156-D pose representation:

    3   global orientation
    63  body pose
    45  left hand
    45  right hand
    ----------------
    156 total

The available model files in this project are SMPL-X files:

    SMPLX_FEMALE.npz
    SMPLX_MALE.npz
    SMPLX_NEUTRAL.npz

Therefore this script performs an explicit:

    AMASS SMPL+H 156-D
            |
            v
    explicit pose mapping
            |
            v
    SMPL-X
            |
            v
    3D joints

SMPL-X facial parameters are zero-initialized because the AMASS
156-D pose vector does not contain jaw/eye/expression parameters.

The script:
    - reads the inventory created by 01_load_amass.py
    - processes only valid files
    - resolves paths relative to the project
    - never modifies raw AMASS files
    - supports CPU and CUDA
    - supports deterministic --sample N
    - supports --dataset
    - supports configurable batch size
    - safely handles the final partial batch
    - saves joints by default
    - optionally saves vertices
    - writes reconstruction summary
    - writes per-sequence failures
    - validates finite output values
"""


from __future__ import annotations

import argparse
import csv
import json
import math
import time
import traceback
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import torch
import smplx


# ============================================================================
# PROJECT PATHS
# ============================================================================

# File:
# E:/latent-objective-humanoid/03_human_motion/scripts/
#                         02_smplx_reconstruction.py
#
# parents[0] = scripts
# parents[1] = 03_human_motion
# parents[2] = project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

HUMAN_MOTION_DIR = PROJECT_ROOT / "03_human_motion"

AMASS_DIR = (
    HUMAN_MOTION_DIR
    / "data"
    / "AMASS"
    / "raw"
)

PROCESSED_DIR = (
    HUMAN_MOTION_DIR
    / "data"
    / "processed"
)

STATISTICS_DIR = (
    HUMAN_MOTION_DIR
    / "results"
    / "statistics"
)

INVENTORY_CSV = (
    STATISTICS_DIR
    / "amass_motion_files.csv"
)

OUTPUT_DIR = (
    PROCESSED_DIR
    / "smplx"
)

SUMMARY_JSON = (
    STATISTICS_DIR
    / "reconstruction_summary.json"
)

FAILURES_CSV = (
    STATISTICS_DIR
    / "reconstruction_failures.csv"
)

# IMPORTANT:
# The directory name is "smplx" in the current project, but we do NOT infer
# the model family from the directory name.
#
# Actual files are:
#   SMPLX_FEMALE.npz
#   SMPLX_MALE.npz
#   SMPLX_NEUTRAL.npz
#
# Therefore the actual model family is determined from those files.
MODEL_DIR = (
    HUMAN_MOTION_DIR
    / "external"
    / "smplx"
    / "models"
    / "smplx"
)


# ============================================================================
# REPRESENTATION CONSTANTS
# ============================================================================

AMASS_POSE_DIM = 156

GLOBAL_ORIENT_DIM = 3
BODY_JOINTS = 21
BODY_POSE_DIM = BODY_JOINTS * 3

HAND_JOINTS = 15
HAND_POSE_DIM = HAND_JOINTS * 3

EXPECTED_BETAS = 16

DEFAULT_BATCH_SIZE = 32

SUPPORTED_GENDERS = {
    "male",
    "female",
    "neutral",
}


# ============================================================================
# LOGGING
# ============================================================================

def log(message: str) -> None:
    """Print a flushed terminal message."""
    print(message, flush=True)


# ============================================================================
# JSON / PATH UTILITIES
# ============================================================================

def json_safe(value: Any) -> Any:
    """
    Convert common numpy / torch / Path values to JSON-safe objects.
    """

    if isinstance(value, Path):
        return value.as_posix()

    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, torch.Tensor):
        return value.detach().cpu().tolist()

    if isinstance(value, dict):
        return {
            str(key): json_safe(val)
            for key, val in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            json_safe(item)
            for item in value
        ]

    return value


def relative_to_project(path: Path) -> str:
    """
    Convert an absolute path to a project-relative path whenever possible.
    """

    try:
        return path.resolve().relative_to(
            PROJECT_ROOT.resolve()
        ).as_posix()

    except ValueError:
        return path.as_posix()


# ============================================================================
# DEVICE
# ============================================================================

def resolve_device(
    requested: str,
) -> torch.device:
    """
    Resolve requested torch device.
    """

    requested = requested.lower().strip()

    if requested == "cpu":
        return torch.device("cpu")

    if requested == "cuda":

        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA was requested, but "
                "torch.cuda.is_available() is False."
            )

        return torch.device("cuda")

    raise ValueError(
        f"Unsupported device: {requested}"
    )


# ============================================================================
# GENDER
# ============================================================================

def normalize_gender(
    value: Any,
) -> str:
    """
    Normalize AMASS gender values.
    """

    if isinstance(value, np.ndarray):

        if value.ndim == 0:
            value = value.item()

        elif value.size == 1:
            value = value.reshape(-1)[0].item()

    gender = str(value).strip().lower()

    if gender in {
        "m",
        "male",
    }:
        return "male"

    if gender in {
        "f",
        "female",
    }:
        return "female"

    if gender in {
        "n",
        "neutral",
        "none",
    }:
        return "neutral"

    raise ValueError(
        f"Unsupported gender value: {value!r}"
    )


# ============================================================================
# INVENTORY
# ============================================================================

def find_column(
    fieldnames: List[str],
    candidates: Iterable[str],
) -> Optional[str]:
    """
    Find a column name case-insensitively.
    """

    normalized = {
        field.strip().lower(): field
        for field in fieldnames
        if field is not None
    }

    for candidate in candidates:

        key = candidate.lower()

        if key in normalized:
            return normalized[key]

    return None


def load_inventory(
    inventory_path: Path,
    dataset_filter: Optional[str] = None,
    sample: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Read AMASS inventory and return only valid sequences.

    Selection is deterministic:
        dataset name
        source path
    """

    if not inventory_path.exists():

        raise FileNotFoundError(
            "Inventory not found:\n"
            f"{inventory_path}"
        )

    with inventory_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as f:

        reader = csv.DictReader(f)

        if reader.fieldnames is None:

            raise RuntimeError(
                "Inventory CSV has no header."
            )

        fieldnames = list(
            reader.fieldnames
        )

        dataset_col = find_column(
            fieldnames,
            [
                "dataset",
                "dataset_name",
                "source_dataset",
            ],
        )

        valid_col = find_column(
            fieldnames,
            [
                "valid",
                "is_valid",
                "validation",
                "status",
            ],
        )

        path_col = find_column(
            fieldnames,
            [
                "relative_path",
                "source_path",
                "file_path",
                "path",
                "filepath",
                "file",
            ],
        )

        if path_col is None:

            raise RuntimeError(
                "Could not identify source path "
                "column in inventory.\n"
                f"Available columns: {fieldnames}"
            )

        if valid_col is None:

            raise RuntimeError(
                "Could not identify validity column "
                "in inventory.\n"
                f"Available columns: {fieldnames}"
            )

        rows: List[Dict[str, Any]] = []

        for row in reader:

            raw_valid = str(
                row.get(valid_col, "")
            ).strip().lower()

            is_valid = raw_valid in {
                "true",
                "1",
                "yes",
                "valid",
            }

            if not is_valid:
                continue

            dataset = ""

            if dataset_col is not None:

                dataset = str(
                    row.get(dataset_col, "")
                ).strip()

            if (
                dataset_filter is not None
                and dataset.lower()
                != dataset_filter.lower()
            ):
                continue

            source_value = str(
                row.get(path_col, "")
            ).strip()

            if not source_value:
                continue

            row["_source_value"] = source_value
            row["_dataset"] = dataset

            rows.append(row)

    # Deterministic ordering.
    rows.sort(
        key=lambda row: (
            row.get("_dataset", "").lower(),
            row.get(
                "_source_value",
                "",
            ).lower(),
        )
    )

    if sample is not None:
        rows = rows[:sample]

    return rows


# ============================================================================
# AMASS PATH RESOLUTION
# ============================================================================

def resolve_amass_path(
    source_value: str,
) -> Path:
    """
    Resolve an inventory path.

    Supported forms:

        ACCAD/foo/file.npz

        03_human_motion/data/AMASS/raw/ACCAD/foo/file.npz

        absolute path

    No absolute path is hard-coded.
    """

    candidate = Path(source_value)

    # ------------------------------------------------------------
    # Case 1: inventory already contains an absolute path
    # ------------------------------------------------------------

    if candidate.is_absolute():

        if candidate.exists():
            return candidate.resolve()

        raise FileNotFoundError(
            "Inventory contains an absolute path "
            "that does not exist:\n"
            f"{candidate}"
        )

    # ------------------------------------------------------------
    # Case 2: relative to AMASS/raw
    # ------------------------------------------------------------

    candidate_raw = (
        AMASS_DIR
        / candidate
    )

    if candidate_raw.exists():
        return candidate_raw.resolve()

    # ------------------------------------------------------------
    # Case 3: relative to project root
    # ------------------------------------------------------------

    candidate_project = (
        PROJECT_ROOT
        / candidate
    )

    if candidate_project.exists():
        return candidate_project.resolve()

    # ------------------------------------------------------------
    # Case 4: relative to 03_human_motion
    # ------------------------------------------------------------

    candidate_motion = (
        HUMAN_MOTION_DIR
        / candidate
    )

    if candidate_motion.exists():
        return candidate_motion.resolve()

    raise FileNotFoundError(
        "Could not resolve AMASS source file.\n"
        f"Inventory value: {source_value}\n\n"
        "Checked:\n"
        f"  {candidate_raw}\n"
        f"  {candidate_project}\n"
        f"  {candidate_motion}"
    )


# ============================================================================
# MODEL AUDIT
# ============================================================================

def inspect_model_files(
    model_dir: Path,
) -> Dict[str, Path]:
    """
    Verify that actual available files are SMPL-X files.

    We intentionally do NOT infer model family from directory name.
    """

    if not model_dir.exists():

        raise FileNotFoundError(
            "Model directory does not exist:\n"
            f"{model_dir}"
        )

    expected = {
        "female": (
            model_dir
            / "SMPLX_FEMALE.npz"
        ),
        "male": (
            model_dir
            / "SMPLX_MALE.npz"
        ),
        "neutral": (
            model_dir
            / "SMPLX_NEUTRAL.npz"
        ),
    }

    missing = [
        str(path)
        for path in expected.values()
        if not path.exists()
    ]

    if missing:

        raise RuntimeError(
            "The expected SMPL-X model files are incomplete.\n"
            "Missing:\n"
            + "\n".join(missing)
        )

    # Verify actual NPZ contents.
    required_keys = {
        "v_template",
        "shapedirs",
        "posedirs",
        "J_regressor",
        "weights",
    }

    for gender, path in expected.items():

        with np.load(
            path,
            allow_pickle=True,
        ) as data:

            keys = set(data.files)

        missing_keys = (
            required_keys - keys
        )

        if missing_keys:

            raise RuntimeError(
                f"{path.name} does not appear to be "
                "a valid SMPL-X model file.\n"
                f"Missing keys: "
                f"{sorted(missing_keys)}"
            )

    return expected


# ============================================================================
# SMPL-X MODEL CREATION
# ============================================================================

def create_smplx_model(
    model_dir: Path,
    gender: str,
    device: torch.device,
    batch_size: int,
) -> torch.nn.Module:
    """
    Create one gender-specific SMPL-X model.

    IMPORTANT:
        use_pca=False

    because AMASS provides full 15x3 hand axis-angle poses.
    """

    gender = normalize_gender(gender)

    model_file = (
        model_dir
        / f"SMPLX_{gender.upper()}.npz"
    )

    if not model_file.exists():

        raise FileNotFoundError(
            "SMPL-X model file not found:\n"
            f"{model_file}"
        )

    model = smplx.create(
        str(model_file),
        model_type="smplx",
        gender=gender,
        num_betas=EXPECTED_BETAS,
        num_expression_coeffs=10,
        use_pca=False,
        ext="npz",
        batch_size=batch_size,
        create_expression=True,
        create_jaw_pose=True,
        create_leye_pose=True,
        create_reye_pose=True,
    )

    model = model.to(device)

    model.eval()

    return model


# ============================================================================
# AMASS POSE MAPPING
# ============================================================================

def map_amass_pose_to_smplx(
    poses: np.ndarray,
    device: torch.device,
) -> Dict[str, torch.Tensor]:
    """
    Map AMASS 156-D SMPL+H-style pose to SMPL-X inputs.

    Layout:

        [0:3]       global orientation
        [3:66]      body pose
        [66:111]    hand block A
        [111:156]   hand block B

    Facial parameters are zero-initialized.
    """

    if poses.ndim != 2:

        raise ValueError(
            "Expected poses with shape (N,156), "
            f"got {poses.shape}"
        )

    if poses.shape[1] != AMASS_POSE_DIM:

        raise ValueError(
            "AMASS pose dimension mismatch.\n"
            f"Expected: {AMASS_POSE_DIM}\n"
            f"Got:      {poses.shape[1]}"
        )

    poses = np.asarray(
        poses,
        dtype=np.float32,
    )

    num_frames = poses.shape[0]

    # ------------------------------------------------------------
    # AMASS SMPL+H blocks
    # ------------------------------------------------------------

    global_orient = (
        poses[:, 0:3]
    )

    body_pose = (
        poses[:, 3:66]
    )

    hand_a = (
        poses[:, 66:111]
    )

    hand_b = (
        poses[:, 111:156]
    )

    # Current AMASS convention:
    # first hand block = left hand
    # second hand block = right hand.
    #
    # Semantic left/right will be validated separately through
    # joint-level visualization / motion inspection.

    left_hand_pose = hand_a
    right_hand_pose = hand_b

    # ------------------------------------------------------------
    # Facial parameters absent from AMASS 156-D
    # ------------------------------------------------------------

    zeros3 = np.zeros(
        (num_frames, 3),
        dtype=np.float32,
    )

    zeros_expression = np.zeros(
        (num_frames, 10),
        dtype=np.float32,
    )

    tensors = {

        "global_orient":
            torch.from_numpy(
                global_orient
            ).to(device),

        "body_pose":
            torch.from_numpy(
                body_pose
            ).to(device),

        "left_hand_pose":
            torch.from_numpy(
                left_hand_pose
            ).to(device),

        "right_hand_pose":
            torch.from_numpy(
                right_hand_pose
            ).to(device),

        "jaw_pose":
            torch.from_numpy(
                zeros3
            ).to(device),

        "leye_pose":
            torch.from_numpy(
                zeros3
            ).to(device),

        "reye_pose":
            torch.from_numpy(
                zeros3
            ).to(device),

        "expression":
            torch.from_numpy(
                zeros_expression
            ).to(device),
    }

    # ------------------------------------------------------------
    # Explicit pre-forward shape validation
    # ------------------------------------------------------------

    expected_shapes = {

        "global_orient":
            (num_frames, 3),

        "body_pose":
            (num_frames, 63),

        "left_hand_pose":
            (num_frames, 45),

        "right_hand_pose":
            (num_frames, 45),

        "jaw_pose":
            (num_frames, 3),

        "leye_pose":
            (num_frames, 3),

        "reye_pose":
            (num_frames, 3),

        "expression":
            (num_frames, 10),
    }

    for name, expected_shape in expected_shapes.items():

        actual_shape = tuple(
            tensors[name].shape
        )

        if actual_shape != expected_shape:

            raise RuntimeError(
                f"Pose mapping error for "
                f"{name}:\n"
                f"Expected: {expected_shape}\n"
                f"Got:      {actual_shape}"
            )

    return tensors


# ============================================================================
# BETAS
# ============================================================================

def prepare_betas(
    betas: np.ndarray,
    num_frames: int,
    device: torch.device,
) -> torch.Tensor:
    """
    Convert shape coefficients:

        (16,)
            ->
        (N,16)

    The same body shape is used for every frame.
    """

    betas = np.asarray(
        betas,
        dtype=np.float32,
    ).reshape(-1)

    # ------------------------------------------------------------
    # Normalize beta dimensionality
    # ------------------------------------------------------------

    if betas.size < EXPECTED_BETAS:

        padded = np.zeros(
            EXPECTED_BETAS,
            dtype=np.float32,
        )

        padded[
            :betas.size
        ] = betas

        betas = padded

    elif betas.size > EXPECTED_BETAS:

        betas = betas[
            :EXPECTED_BETAS
        ]

    # ------------------------------------------------------------
    # Expand across frames
    # ------------------------------------------------------------

    beta_tensor = torch.from_numpy(
        betas
    ).to(device)

    beta_tensor = (
        beta_tensor
        .unsqueeze(0)
        .expand(
            num_frames,
            -1,
        )
        .contiguous()
    )

    expected_shape = (
        num_frames,
        EXPECTED_BETAS,
    )

    if tuple(beta_tensor.shape) != expected_shape:

        raise RuntimeError(
            "Beta expansion failed.\n"
            f"Expected: {expected_shape}\n"
            f"Got:      {tuple(beta_tensor.shape)}"
        )

    return beta_tensor


# ============================================================================
# SAFE BATCH PREPARATION
# ============================================================================

def pad_batch_to_model_size(
    poses_batch: np.ndarray,
    trans_batch: np.ndarray,
    model_batch_size: int,
) -> Tuple[
    np.ndarray,
    np.ndarray,
    int,
]:
    """
    Pad a final partial batch to model.batch_size.

    Example:

        actual = 8
        model  = 32

        8 real frames
        +24 repeated padding frames
        --------------------------
        32 model frames

    The caller MUST discard the padded output afterward.

    We repeat the final real frame rather than introducing zeros.
    This keeps the artificial input physically valid and avoids
    creating an artificial discontinuity.
    """

    actual_batch_size = (
        poses_batch.shape[0]
    )

    if actual_batch_size > model_batch_size:

        raise ValueError(
            "Actual batch is larger than model batch size.\n"
            f"Actual: {actual_batch_size}\n"
            f"Model:  {model_batch_size}"
        )

    if actual_batch_size == model_batch_size:

        return (
            poses_batch,
            trans_batch,
            actual_batch_size,
        )

    if actual_batch_size <= 0:

        raise ValueError(
            "Cannot pad an empty batch."
        )

    pad_count = (
        model_batch_size
        - actual_batch_size
    )

    poses_padding = np.repeat(
        poses_batch[-1:],
        pad_count,
        axis=0,
    )

    trans_padding = np.repeat(
        trans_batch[-1:],
        pad_count,
        axis=0,
    )

    padded_poses = np.concatenate(
        [
            poses_batch,
            poses_padding,
        ],
        axis=0,
    )

    padded_trans = np.concatenate(
        [
            trans_batch,
            trans_padding,
        ],
        axis=0,
    )

    return (
        padded_poses,
        padded_trans,
        actual_batch_size,
    )


# ============================================================================
# RECONSTRUCTION
# ============================================================================

@torch.no_grad()
def reconstruct_sequence(
    model: torch.nn.Module,
    poses: np.ndarray,
    trans: np.ndarray,
    betas: np.ndarray,
    batch_size: int,
    device: torch.device,
    debug: bool = False,
    save_vertices: bool = False,
) -> Dict[str, np.ndarray]:
    """
    Reconstruct one AMASS sequence.

    IMPORTANT:
    The final partial batch is padded to model.batch_size.

    This avoids the SMPL-X landmark bug:

        model.batch_size = 32
        actual final batch = 8

    which otherwise causes:

        einsum(): subscript b has size 32
        for operand 1 which does not broadcast
        with previously seen size 8
    """

    if poses.ndim != 2:

        raise ValueError(
            f"Invalid poses shape: {poses.shape}"
        )

    if poses.shape[1] != AMASS_POSE_DIM:

        raise ValueError(
            f"Expected poses (N,156), "
            f"got {poses.shape}"
        )

    num_frames = poses.shape[0]

    if num_frames == 0:

        raise ValueError(
            "Sequence contains zero frames."
        )

    if trans.shape != (
        num_frames,
        3,
    ):

        raise ValueError(
            "Translation shape mismatch.\n"
            f"Expected: {(num_frames, 3)}\n"
            f"Got:      {trans.shape}"
        )

    # ------------------------------------------------------------
    # IMPORTANT:
    # Use the model's actual internal batch size.
    # ------------------------------------------------------------

    model_batch_size = int(
        getattr(
            model,
            "batch_size",
            batch_size,
        )
    )

    if model_batch_size <= 0:

        raise RuntimeError(
            f"Invalid model.batch_size: "
            f"{model_batch_size}"
        )

    if batch_size != model_batch_size:

        raise RuntimeError(
            "Requested batch size does not match "
            "the instantiated SMPL-X model.\n"
            f"Requested: {batch_size}\n"
            f"Model:     {model_batch_size}"
        )

    outputs_joints: List[np.ndarray] = []

    outputs_vertices: List[np.ndarray] = []

    # ------------------------------------------------------------
    # Frame batches
    # ------------------------------------------------------------

    for start in range(
        0,
        num_frames,
        model_batch_size,
    ):

        end = min(
            start + model_batch_size,
            num_frames,
        )

        poses_batch = poses[
            start:end
        ]

        trans_batch = trans[
            start:end
        ]

        # --------------------------------------------------------
        # Pad final partial batch
        # --------------------------------------------------------

        (
            poses_model,
            trans_model,
            actual_batch_size,
        ) = pad_batch_to_model_size(
            poses_batch=poses_batch,
            trans_batch=trans_batch,
            model_batch_size=model_batch_size,
        )

        model_num_frames = (
            poses_model.shape[0]
        )

        if model_num_frames != model_batch_size:

            raise RuntimeError(
                "Internal padding failed.\n"
                f"Expected model batch: "
                f"{model_batch_size}\n"
                f"Got: {model_num_frames}"
            )

        # --------------------------------------------------------
        # Map AMASS pose
        # --------------------------------------------------------

        mapped = map_amass_pose_to_smplx(
            poses_model,
            device=device,
        )

        # --------------------------------------------------------
        # Expand betas
        # --------------------------------------------------------

        beta_batch = prepare_betas(
            betas=betas,
            num_frames=model_num_frames,
            device=device,
        )

        # --------------------------------------------------------
        # Translation
        # --------------------------------------------------------

        transl_tensor = torch.from_numpy(
            np.asarray(
                trans_model,
                dtype=np.float32,
            )
        ).to(device)

        if tuple(
            transl_tensor.shape
        ) != (
            model_num_frames,
            3,
        ):

            raise RuntimeError(
                "Translation batch shape mismatch.\n"
                f"Expected: "
                f"{(model_num_frames, 3)}\n"
                f"Got: "
                f"{tuple(transl_tensor.shape)}"
            )

        # --------------------------------------------------------
        # Debug output
        # --------------------------------------------------------

        if debug:

            log(
                f"  model batch "
                f"{start}:{end} | "
                f"actual={actual_batch_size} | "
                f"padded={model_num_frames} | "
                f"global="
                f"{tuple(mapped['global_orient'].shape)} | "
                f"body="
                f"{tuple(mapped['body_pose'].shape)} | "
                f"left_hand="
                f"{tuple(mapped['left_hand_pose'].shape)} | "
                f"right_hand="
                f"{tuple(mapped['right_hand_pose'].shape)} | "
                f"betas="
                f"{tuple(beta_batch.shape)}"
            )

        # --------------------------------------------------------
        # Forward
        # --------------------------------------------------------

        output = model(
            betas=beta_batch,
            global_orient=mapped[
                "global_orient"
            ],
            body_pose=mapped[
                "body_pose"
            ],
            left_hand_pose=mapped[
                "left_hand_pose"
            ],
            right_hand_pose=mapped[
                "right_hand_pose"
            ],
            jaw_pose=mapped[
                "jaw_pose"
            ],
            leye_pose=mapped[
                "leye_pose"
            ],
            reye_pose=mapped[
                "reye_pose"
            ],
            expression=mapped[
                "expression"
            ],
            transl=transl_tensor,
            return_verts=save_vertices,
            return_full_pose=False,
            pose2rot=True,
        )

        # --------------------------------------------------------
        # Remove artificial padding
        # --------------------------------------------------------

        joints = (
            output
            .joints[
                :actual_batch_size
            ]
        )

        vertices = None

        if save_vertices:

            if output.vertices is None:

                raise RuntimeError(
                    "save_vertices=True but "
                    "SMPL-X returned no vertices."
                )

            vertices = (
                output
                .vertices[
                    :actual_batch_size
                ]
            )

        # --------------------------------------------------------
        # Output shape validation
        # --------------------------------------------------------

        if joints.ndim != 3:

            raise RuntimeError(
                "Unexpected joints dimensions.\n"
                f"Got: {tuple(joints.shape)}"
            )

        if joints.shape[0] != actual_batch_size:

            raise RuntimeError(
                "Output frame count mismatch after "
                "padding removal.\n"
                f"Expected: {actual_batch_size}\n"
                f"Got:      {joints.shape[0]}"
            )

        if joints.shape[2] != 3:

            raise RuntimeError(
                "Joint coordinate dimension must be 3.\n"
                f"Got: {tuple(joints.shape)}"
            )

        # --------------------------------------------------------
        # Finite validation
        # --------------------------------------------------------

        if not torch.isfinite(
            joints
        ).all():

            raise FloatingPointError(
                "Non-finite joint values detected "
                f"in batch {start}:{end}."
            )

        outputs_joints.append(
            joints
            .detach()
            .cpu()
            .numpy()
            .astype(np.float32)
        )

        # --------------------------------------------------------
        # Vertices
        # --------------------------------------------------------

        if save_vertices:

            assert vertices is not None

            if not torch.isfinite(
                vertices
            ).all():

                raise FloatingPointError(
                    "Non-finite vertex values detected "
                    f"in batch {start}:{end}."
                )

            outputs_vertices.append(
                vertices
                .detach()
                .cpu()
                .numpy()
                .astype(np.float32)
            )

    # ------------------------------------------------------------
    # Concatenate all real frames
    # ------------------------------------------------------------

    result: Dict[str, np.ndarray] = {

        "joints":
            np.concatenate(
                outputs_joints,
                axis=0,
            )
    }

    if save_vertices:

        result["vertices"] = (
            np.concatenate(
                outputs_vertices,
                axis=0,
            )
        )

    return result


# ============================================================================
# VALIDATION
# ============================================================================

def validate_reconstruction(
    result: Dict[str, np.ndarray],
    num_frames: int,
    fps: float,
) -> Dict[str, Any]:
    """
    Validate reconstructed 3D data.
    """

    joints = result["joints"]

    if joints.ndim != 3:

        raise ValueError(
            "joints must have shape "
            "(N,J,3).\n"
            f"Got: {joints.shape}"
        )

    if joints.shape[0] != num_frames:

        raise ValueError(
            "Frame count mismatch.\n"
            f"Expected: {num_frames}\n"
            f"Got:      {joints.shape[0]}"
        )

    if joints.shape[2] != 3:

        raise ValueError(
            "Last joint dimension must be 3.\n"
            f"Got: {joints.shape}"
        )

    nan_count = int(
        np.isnan(joints).sum()
    )

    inf_count = int(
        np.isinf(joints).sum()
    )

    if nan_count != 0:

        raise FloatingPointError(
            f"NaN detected in reconstructed "
            f"joints: {nan_count}"
        )

    if inf_count != 0:

        raise FloatingPointError(
            f"Inf detected in reconstructed "
            f"joints: {inf_count}"
        )

    if (
        not math.isfinite(
            float(fps)
        )
        or fps <= 0
    ):

        raise ValueError(
            f"Invalid FPS: {fps}"
        )

    validation: Dict[str, Any] = {

        "num_frames":
            int(num_frames),

        "joint_shape":
            list(joints.shape),

        "num_joints":
            int(joints.shape[1]),

        "nan_count":
            nan_count,

        "inf_count":
            inf_count,

        "finite":
            True,

        "fps":
            float(fps),
    }

    if "vertices" in result:

        vertices = result[
            "vertices"
        ]

        validation[
            "vertices_shape"
        ] = list(
            vertices.shape
        )

        validation[
            "vertices_nan_count"
        ] = int(
            np.isnan(vertices).sum()
        )

        validation[
            "vertices_inf_count"
        ] = int(
            np.isinf(vertices).sum()
        )

    return validation


# ============================================================================
# AMASS LOADING
# ============================================================================

def load_amass_file(
    source_path: Path,
) -> Dict[str, Any]:
    """
    Load required AMASS fields.

    Raw file is opened read-only and never modified.
    """

    with np.load(
        source_path,
        allow_pickle=True,
    ) as data:

        required_fields = {
            "poses",
            "trans",
            "betas",
            "gender",
            "mocap_framerate",
        }

        missing = (
            required_fields
            - set(data.files)
        )

        if missing:

            raise KeyError(
                "Missing required AMASS fields:\n"
                f"{sorted(missing)}"
            )

        return {

            "poses":
                np.asarray(
                    data["poses"]
                ),

            "trans":
                np.asarray(
                    data["trans"]
                ),

            "betas":
                np.asarray(
                    data["betas"]
                ),

            "gender":
                data["gender"],

            "mocap_framerate":
                float(
                    np.asarray(
                        data[
                            "mocap_framerate"
                        ]
                    )
                    .reshape(-1)[0]
                ),
        }


# ============================================================================
# OUTPUT PATH
# ============================================================================

def output_path_for(
    source_path: Path,
) -> Path:
    """
    Preserve AMASS relative hierarchy in processed/smplx.
    """

    relative = (
        source_path
        .resolve()
        .relative_to(
            AMASS_DIR.resolve()
        )
    )

    return (
        OUTPUT_DIR
        / relative
    )


# ============================================================================
# SAVE OUTPUT
# ============================================================================

def save_reconstruction(
    output_path: Path,
    result: Dict[str, np.ndarray],
    metadata: Dict[str, Any],
    overwrite: bool,
) -> None:
    """
    Save reconstructed sequence.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if (
        output_path.exists()
        and not overwrite
    ):

        raise FileExistsError(
            "Output already exists and "
            "--overwrite was not supplied:\n"
            f"{output_path}"
        )

    metadata_json = json.dumps(
        json_safe(metadata),
        ensure_ascii=False,
    )

    payload: Dict[str, Any] = {

        "joints":
            result["joints"],

        "metadata_json":
            np.array(
                metadata_json
            ),
    }

    if "vertices" in result:

        payload[
            "vertices"
        ] = result[
            "vertices"
        ]

    np.savez_compressed(
        output_path,
        **payload,
    )


# ============================================================================
# FAILURE REPORT
# ============================================================================

def write_failures(
    failures: List[Dict[str, Any]],
    path: Path,
) -> None:
    """
    Save per-sequence reconstruction failures.
    """

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "dataset",
        "source_file",
        "error_type",
        "error_message",
    ]

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for failure in failures:

            writer.writerow(
                {
                    field:
                        failure.get(
                            field,
                            "",
                        )
                    for field in fieldnames
                }
            )


# ============================================================================
# PROCESS ONE SEQUENCE
# ============================================================================

def process_one(
    row: Dict[str, Any],
    model_cache: Dict[
        str,
        torch.nn.Module,
    ],
    device: torch.device,
    batch_size: int,
    save_vertices: bool,
    overwrite: bool,
    debug: bool,
) -> Tuple[
    bool,
    Dict[str, Any],
]:
    """
    Process exactly one AMASS sequence.
    """

    source_value = (
        row["_source_value"]
    )

    dataset = (
        row.get(
            "_dataset",
            "",
        )
    )

    # ------------------------------------------------------------
    # Resolve source
    # ------------------------------------------------------------

    source_path = (
        resolve_amass_path(
            source_value
        )
    )

    # ------------------------------------------------------------
    # Load AMASS
    # ------------------------------------------------------------

    data = load_amass_file(
        source_path
    )

    poses = data[
        "poses"
    ]

    trans = data[
        "trans"
    ]

    betas = data[
        "betas"
    ]

    gender = normalize_gender(
        data["gender"]
    )

    fps = data[
        "mocap_framerate"
    ]

    # ------------------------------------------------------------
    # Validate source shapes
    # ------------------------------------------------------------

    if poses.ndim != 2:

        raise ValueError(
            "Invalid AMASS poses shape:\n"
            f"{poses.shape}"
        )

    if poses.shape[1] != (
        AMASS_POSE_DIM
    ):

        raise ValueError(
            "This reconstruction script expects "
            "AMASS 156-D pose representation.\n"
            f"Got: {poses.shape}"
        )

    if trans.shape != (
        poses.shape[0],
        3,
    ):

        raise ValueError(
            "Invalid AMASS translation shape.\n"
            f"Expected: "
            f"{(poses.shape[0], 3)}\n"
            f"Got: {trans.shape}"
        )

    # ------------------------------------------------------------
    # Gender-specific model
    # ------------------------------------------------------------

    if gender not in model_cache:

        model_cache[
            gender
        ] = create_smplx_model(
            model_dir=MODEL_DIR,
            gender=gender,
            device=device,
            batch_size=batch_size,
        )

    model = model_cache[
        gender
    ]

    # ------------------------------------------------------------
    # Reconstruction
    # ------------------------------------------------------------

    start_time = (
        time.perf_counter()
    )

    result = reconstruct_sequence(
        model=model,
        poses=poses,
        trans=trans,
        betas=betas,
        batch_size=batch_size,
        device=device,
        debug=debug,
        save_vertices=save_vertices,
    )

    # ------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------

    validation = (
        validate_reconstruction(
            result=result,
            num_frames=poses.shape[0],
            fps=fps,
        )
    )

    elapsed = (
        time.perf_counter()
        - start_time
    )

    # ------------------------------------------------------------
    # Output path
    # ------------------------------------------------------------

    output_path = (
        output_path_for(
            source_path
        )
    )

    # ------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------

    metadata: Dict[str, Any] = {

        "schema_version":
            "stage03-reconstruction-v1",

        "model_type":
            "smplx",

        "source_pose_representation":
            "AMASS_SMPL+H_156",

        "target_body_model":
            "SMPL-X",

        "pose_mapping": {

            "global_orient":
                "poses[:, 0:3]",

            "body_pose":
                "poses[:, 3:66]",

            "left_hand_pose":
                "poses[:, 66:111]",

            "right_hand_pose":
                "poses[:, 111:156]",

            "jaw_pose":
                "zeros",

            "leye_pose":
                "zeros",

            "reye_pose":
                "zeros",

            "expression":
                "zeros",
        },

        "hand_semantics":
            "pending_visual_validation",

        "num_betas_used":
            EXPECTED_BETAS,

        "gender":
            gender,

        "fps":
            float(fps),

        "source_dataset":
            dataset,

        "source_file":
            relative_to_project(
                source_path
            ),

        "num_frames":
            int(
                poses.shape[0]
            ),

        "device":
            str(device),

        "batch_size":
            int(batch_size),

        "save_vertices":
            bool(save_vertices),

        "runtime_seconds":
            float(elapsed),

        "validation":
            validation,
    }

    # ------------------------------------------------------------
    # Save
    # ------------------------------------------------------------

    save_reconstruction(
        output_path=output_path,
        result=result,
        metadata=metadata,
        overwrite=overwrite,
    )

    return (
        True,
        {
            "dataset":
                dataset,

            "source_file":
                relative_to_project(
                    source_path
                ),

            "output_file":
                relative_to_project(
                    output_path
                ),

            "gender":
                gender,

            "num_frames":
                int(
                    poses.shape[0]
                ),

            "fps":
                float(fps),

            "joint_shape":
                list(
                    result[
                        "joints"
                    ].shape
                ),

            "runtime_seconds":
                float(elapsed),
        },
    )


# ============================================================================
# ARGUMENTS
# ============================================================================

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.
    """

    parser = argparse.ArgumentParser(
        description=(
            "Reconstruct valid AMASS SMPL+H 156-D "
            "sequences using the available SMPL-X models."
        )
    )

    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help=(
            "Process only the first N valid "
            "inventory entries."
        ),
    )

    parser.add_argument(
        "--dataset",
        type=str,
        default=None,
        help=(
            "Process only one AMASS dataset, "
            "for example ACCAD."
        ),
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=(
            "SMPL-X model batch size. "
            "Default: 32."
        ),
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        choices=[
            "cpu",
            "cuda",
        ],
        help=(
            "Torch device. "
            "Default: cpu."
        ),
    )

    parser.add_argument(
        "--save-vertices",
        action="store_true",
        help=(
            "Store SMPL-X vertices in addition "
            "to joints."
        ),
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Overwrite existing processed files."
        ),
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help=(
            "Print detailed tensor/batch "
            "information."
        ),
    )

    return parser.parse_args()


# ============================================================================
# MAIN
# ============================================================================

def main() -> int:
    """
    Main reconstruction entry point.
    """

    args = parse_args()

    # ------------------------------------------------------------
    # Argument validation
    # ------------------------------------------------------------

    if (
        args.sample is not None
        and args.sample <= 0
    ):

        raise ValueError(
            "--sample must be greater than zero."
        )

    if args.batch_size <= 0:

        raise ValueError(
            "--batch-size must be greater than zero."
        )

    # ------------------------------------------------------------
    # Directories
    # ------------------------------------------------------------

    STATISTICS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ------------------------------------------------------------
    # Device
    # ------------------------------------------------------------

    device = resolve_device(
        args.device
    )

    # ------------------------------------------------------------
    # Header
    # ------------------------------------------------------------

    log("=" * 70)
    log("AMASS -> SMPL-X RECONSTRUCTION")
    log("=" * 70)

    log(
        f"Project root : "
        f"{PROJECT_ROOT}"
    )

    log(
        f"AMASS root   : "
        f"{AMASS_DIR}"
    )

    log(
        f"Inventory    : "
        f"{INVENTORY_CSV}"
    )

    log(
        f"Model dir    : "
        f"{MODEL_DIR}"
    )

    log(
        f"Output dir   : "
        f"{OUTPUT_DIR}"
    )

    log(
        f"Device       : "
        f"{device}"
    )

    log(
        f"Batch size   : "
        f"{args.batch_size}"
    )

    log(
        f"Save verts   : "
        f"{args.save_vertices}"
    )

    # ------------------------------------------------------------
    # Model audit
    # ------------------------------------------------------------

    log("")
    log(
        "Checking actual model files..."
    )

    model_files = (
        inspect_model_files(
            MODEL_DIR
        )
    )

    for gender, path in (
        model_files.items()
    ):

        log(
            f"  {gender:7s}: "
            f"{path.name}"
        )

    log(
        "Model family detected: SMPL-X"
    )

    log(
        "Source representation: "
        "AMASS SMPL+H 156-D"
    )

    # ------------------------------------------------------------
    # Inventory
    # ------------------------------------------------------------

    rows = load_inventory(
        inventory_path=INVENTORY_CSV,
        dataset_filter=args.dataset,
        sample=args.sample,
    )

    log("")
    log(
        f"Valid sequences selected: "
        f"{len(rows)}"
    )

    if not rows:

        log(
            "No valid sequences selected."
        )

        return 0

    # ------------------------------------------------------------
    # Model cache
    # ------------------------------------------------------------

    model_cache: Dict[
        str,
        torch.nn.Module,
    ] = {}

    # ------------------------------------------------------------
    # Result containers
    # ------------------------------------------------------------

    successes: List[
        Dict[str, Any]
    ] = []

    failures: List[
        Dict[str, Any]
    ] = []

    total_frames = 0

    start_all = (
        time.perf_counter()
    )

    # ------------------------------------------------------------
    # Process sequences
    # ------------------------------------------------------------

    for index, row in enumerate(
        rows,
        start=1,
    ):

        source_value = (
            row["_source_value"]
        )

        dataset = (
            row.get(
                "_dataset",
                "",
            )
        )

        log("")
        log(
            f"[{index}/{len(rows)}] "
            f"{dataset} | "
            f"{source_value}"
        )

        try:

            ok, info = process_one(
                row=row,
                model_cache=model_cache,
                device=device,
                batch_size=args.batch_size,
                save_vertices=args.save_vertices,
                overwrite=args.overwrite,
                debug=args.debug,
            )

            successes.append(
                info
            )

            total_frames += (
                info["num_frames"]
            )

            log(
                f"  SUCCESS | "
                f"frames="
                f"{info['num_frames']} | "
                f"joints="
                f"{info['joint_shape']} | "
                f"time="
                f"{info['runtime_seconds']:.3f}s"
            )

        except Exception as exc:

            source_for_failure = (
                source_value
            )

            try:

                resolved = (
                    resolve_amass_path(
                        source_value
                    )
                )

                source_for_failure = (
                    relative_to_project(
                        resolved
                    )
                )

            except Exception:
                pass

            failure = {

                "dataset":
                    dataset,

                "source_file":
                    source_for_failure,

                "error_type":
                    type(exc).__name__,

                "error_message":
                    str(exc),
            }

            failures.append(
                failure
            )

            log(
                f"  FAILED | "
                f"{failure['error_type']}: "
                f"{failure['error_message']}"
            )

            if args.debug:

                traceback.print_exc()

            continue

    # ------------------------------------------------------------
    # Runtime
    # ------------------------------------------------------------

    total_runtime = (
        time.perf_counter()
        - start_all
    )

    # ------------------------------------------------------------
    # Dataset names
    # ------------------------------------------------------------

    datasets = sorted(
        {
            info["dataset"]
            for info in successes
            if info.get("dataset")
        }
    )

    # ------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------

    summary: Dict[str, Any] = {

        "schema_version":
            "stage03-reconstruction-v1",

        "total_selected":
            len(rows),

        "successful":
            len(successes),

        "failed":
            len(failures),

        "total_frames_successful":
            total_frames,

        "datasets":
            datasets,

        "model_type":
            "smplx",

        "source_pose_representation":
            "AMASS_SMPL+H_156",

        "target_body_model":
            "SMPL-X",

        "device":
            str(device),

        "batch_size":
            int(args.batch_size),

        "save_vertices":
            bool(args.save_vertices),

        "runtime_seconds":
            float(total_runtime),

        "inventory":
            relative_to_project(
                INVENTORY_CSV
            ),

        "model_directory":
            relative_to_project(
                MODEL_DIR
            ),

        "output_directory":
            relative_to_project(
                OUTPUT_DIR
            ),

        "successes":
            successes,
    }

    with SUMMARY_JSON.open(
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            json_safe(summary),
            f,
            indent=2,
            ensure_ascii=False,
        )

    # ------------------------------------------------------------
    # Failure CSV
    # ------------------------------------------------------------

    write_failures(
        failures=failures,
        path=FAILURES_CSV,
    )

    # ------------------------------------------------------------
    # Final report
    # ------------------------------------------------------------

    log("")
    log("=" * 70)
    log("RECONSTRUCTION COMPLETE")
    log("=" * 70)

    log(
        f"Selected  : "
        f"{len(rows)}"
    )

    log(
        f"Successful: "
        f"{len(successes)}"
    )

    log(
        f"Failed    : "
        f"{len(failures)}"
    )

    log(
        f"Frames    : "
        f"{total_frames}"
    )

    log(
        f"Runtime   : "
        f"{total_runtime:.3f} sec"
    )

    log("")
    log(
        "Summary   : "
        f"{relative_to_project(SUMMARY_JSON)}"
    )

    log(
        "Failures  : "
        f"{relative_to_project(FAILURES_CSV)}"
    )

    # ------------------------------------------------------------
    # Exit code
    # ------------------------------------------------------------

    # 0 = every selected sequence succeeded
    # 2 = one or more selected sequences failed
    return (
        0
        if not failures
        else 2
    )


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    raise SystemExit(
        main()
    )