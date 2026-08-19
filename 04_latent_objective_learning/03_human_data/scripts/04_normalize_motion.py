from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np


SCRIPT_NAME = "04_normalize_motion"

CANONICAL_KEY = "full"
CANONICAL_JOINT_COUNT = 127
COORD_DIM = 3

ROOT_JOINT_INDEX = 0

DERIVED_KEYS = (
    "body_core",
    "body_contact",
    "hands",
    "face",
)


def log(message: str) -> None:
    print(f"[{SCRIPT_NAME}] {message}")


def warn(message: str) -> None:
    print(f"[WARNING] {message}")


def error(message: str) -> None:
    print(f"[ERROR] {message}")


# ---------------------------------------------------------------------
# Arguments
# ---------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Normalize canonical SMPL-X 127-joint motion data "
            "while preserving both local/root-centered pose and "
            "global root motion."
        )
    )

    parser.add_argument(
        "--input-root",
        type=Path,
        default=None,
        help="Input root containing processed joint NPZ files.",
    )

    parser.add_argument(
        "--output-root",
        type=Path,
        default=None,
        help="Output root for normalized NPZ files.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most N NPZ files.",
    )

    return parser.parse_args()


# ---------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------

def get_project_root(script_path: Path) -> Path:
    """
    scripts/
        04_normalize_motion.py

    project root:
        ../../
    """

    return script_path.resolve().parents[2]


def resolve_roots(
    args: argparse.Namespace,
) -> tuple[Path, Path, Path, Path]:

    script_path = Path(__file__).resolve()

    project_root = get_project_root(
        script_path
    )

    input_root = (
        args.input_root.resolve()
        if args.input_root is not None
        else (
            project_root
            / "data"
            / "processed"
            / "joints"
        )
    )

    output_root = (
        args.output_root.resolve()
        if args.output_root is not None
        else (
            project_root
            / "data"
            / "processed"
            / "normalized"
        )
    )

    return (
        script_path,
        project_root,
        input_root,
        output_root,
    )


# ---------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------

def validate_canonical_tensor(
    joints: np.ndarray,
    source_path: Path,
) -> None:

    if not isinstance(
        joints,
        np.ndarray,
    ):
        raise TypeError(
            "Canonical tensor is not a NumPy array: "
            f"{type(joints)}"
        )

    if joints.ndim != 3:
        raise ValueError(
            "Expected canonical tensor with shape "
            "[T,127,3], "
            f"got {joints.shape}"
        )

    if joints.shape[1] != CANONICAL_JOINT_COUNT:
        raise ValueError(
            f"Expected {CANONICAL_JOINT_COUNT} joints, "
            f"got shape={joints.shape}"
        )

    if joints.shape[2] != COORD_DIM:
        raise ValueError(
            f"Expected XYZ dimension {COORD_DIM}, "
            f"got shape={joints.shape}"
        )

    if joints.shape[0] <= 0:
        raise ValueError(
            f"Sequence contains zero frames: "
            f"{source_path}"
        )

    if not np.isfinite(joints).all():
        raise ValueError(
            "Canonical tensor contains NaN or Inf values: "
            f"{source_path}"
        )


# ---------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------

def load_canonical_and_derived(
    source_path: Path,
) -> tuple[
    np.ndarray,
    dict[str, np.ndarray],
]:

    with np.load(
        source_path,
        allow_pickle=False,
    ) as data:

        available_keys = list(
            data.files
        )

        if CANONICAL_KEY not in available_keys:
            raise KeyError(
                "Canonical SMPL-X tensor 'full' "
                "was not found. "
                f"Available keys: {available_keys}"
            )

        joints = np.asarray(
            data[CANONICAL_KEY]
        )

        validate_canonical_tensor(
            joints,
            source_path,
        )

        derived: dict[str, np.ndarray] = {}

        for key in DERIVED_KEYS:

            if key in available_keys:

                value = np.asarray(
                    data[key]
                )

                if not np.isfinite(
                    value
                ).all():

                    raise ValueError(
                        f"Derived tensor '{key}' "
                        "contains NaN or Inf values."
                    )

                derived[key] = value

    return (
        joints,
        derived,
    )


# ---------------------------------------------------------------------
# Root motion
# ---------------------------------------------------------------------

def compute_root_positions(
    joints: np.ndarray,
) -> np.ndarray:
    """
    Extract original global root/pelvis position.

    Shape:
        [T,3]

    IMPORTANT:
        These values are NOT modified.
        They preserve the original global motion.
    """

    root_positions = joints[
        :,
        ROOT_JOINT_INDEX,
        :
    ]

    return root_positions.astype(
        np.float32,
        copy=True,
    )


def compute_root_displacement(
    root_positions: np.ndarray,
) -> np.ndarray:
    """
    Global root displacement relative to
    the first frame.

    Shape:
        [T,3]

    Frame 0:
        [0,0,0]

    This removes only the arbitrary initial
    world translation while preserving motion.
    """

    displacement = (
        root_positions
        - root_positions[0:1]
    )

    return displacement.astype(
        np.float32,
        copy=False,
    )


def compute_root_velocity(
    root_positions: np.ndarray,
) -> np.ndarray:
    """
    Root displacement per frame.

    Since FPS is not assumed here, this is
    NOT physical meters/second.

    Units:
        dataset coordinate units / frame

    Shape:
        [T,3]

    Frame 0:
        [0,0,0]
    """

    velocity = np.zeros_like(
        root_positions,
        dtype=np.float32,
    )

    if root_positions.shape[0] > 1:

        velocity[1:] = (
            root_positions[1:]
            - root_positions[:-1]
        )

    return velocity


# ---------------------------------------------------------------------
# Body scale
# ---------------------------------------------------------------------

def compute_root_centered(
    joints: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:

    root_positions = compute_root_positions(
        joints
    )

    centered = (
        joints
        - root_positions[:, None, :]
    )

    return (
        centered,
        root_positions,
    )


def compute_sequence_body_scale(
    centered_joints: np.ndarray,
) -> float:
    """
    Compute one scalar body scale for the
    complete sequence.

    This is deliberately sequence-level.

    It does NOT independently scale each frame.
    """

    distances = np.linalg.norm(
        centered_joints,
        axis=-1,
    )

    scale = float(
        np.max(distances)
    )

    if not np.isfinite(scale):
        raise ValueError(
            "Computed body scale is not finite."
        )

    if scale <= 0.0:
        raise ValueError(
            "Computed body scale is zero or negative."
        )

    return scale


# ---------------------------------------------------------------------
# Local normalization
# ---------------------------------------------------------------------

def normalize_local_motion(
    joints: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
    float,
]:

    centered, root_positions = (
        compute_root_centered(
            joints
        )
    )

    scale = compute_sequence_body_scale(
        centered
    )

    normalized = (
        centered / scale
    )

    return (
        normalized.astype(
            np.float32,
            copy=False,
        ),
        root_positions.astype(
            np.float32,
            copy=False,
        ),
        scale,
    )


# ---------------------------------------------------------------------
# Global normalization
# ---------------------------------------------------------------------

def compute_global_motion_features(
    root_positions: np.ndarray,
    body_scale: float,
) -> dict[str, np.ndarray]:

    # -------------------------------------------------------------
    # Original global root trajectory
    # -------------------------------------------------------------

    root_positions_original = (
        root_positions.astype(
            np.float32,
            copy=True,
        )
    )

    # -------------------------------------------------------------
    # Global displacement relative to first frame
    #
    # This preserves:
    #   forward motion
    #   backward motion
    #   left/right motion
    #   jumping
    #   rising/falling
    #
    # But removes arbitrary initial world offset.
    # -------------------------------------------------------------

    root_displacement = (
        compute_root_displacement(
            root_positions_original
        )
    )

    # -------------------------------------------------------------
    # Scale-normalized global trajectory
    # -------------------------------------------------------------

    root_positions_normalized = (
        root_displacement
        / body_scale
    ).astype(
        np.float32,
        copy=False,
    )

    # -------------------------------------------------------------
    # Root velocity / frame displacement
    # -------------------------------------------------------------

    root_velocity = (
        compute_root_velocity(
            root_positions_original
        )
    )

    # -------------------------------------------------------------
    # Scale-normalized root velocity
    # -------------------------------------------------------------

    root_velocity_normalized = (
        root_velocity
        / body_scale
    ).astype(
        np.float32,
        copy=False,
    )

    # -------------------------------------------------------------
    # Normalized displacement
    # -------------------------------------------------------------

    root_displacement_normalized = (
        root_displacement
        / body_scale
    ).astype(
        np.float32,
        copy=False,
    )

    return {
        "root_positions": root_positions_original,

        "root_positions_normalized":
            root_positions_normalized,

        "root_displacement":
            root_displacement,

        "root_displacement_normalized":
            root_displacement_normalized,

        "root_velocity":
            root_velocity,

        "root_velocity_normalized":
            root_velocity_normalized,
    }


# ---------------------------------------------------------------------
# Reconstruction
# ---------------------------------------------------------------------

def reconstruct_original_motion(
    normalized: np.ndarray,
    root_positions: np.ndarray,
    body_scale: float,
) -> np.ndarray:
    """
    Reconstruct original canonical motion.

        original =
            normalized * body_scale
            + root_position
    """

    reconstructed = (
        normalized * body_scale
        + root_positions[:, None, :]
    )

    return reconstructed.astype(
        np.float32,
        copy=False,
    )


def compute_reconstruction_error(
    original: np.ndarray,
    reconstructed: np.ndarray,
) -> dict[str, float]:

    difference = (
        reconstructed.astype(np.float64)
        - original.astype(np.float64)
    )

    abs_difference = np.abs(
        difference
    )

    max_error = float(
        np.max(abs_difference)
    )

    mean_error = float(
        np.mean(abs_difference)
    )

    rmse = float(
        np.sqrt(
            np.mean(
                difference ** 2
            )
        )
    )

    return {
        "max_abs_error": max_error,
        "mean_abs_error": mean_error,
        "rmse": rmse,
    }


# ---------------------------------------------------------------------
# Output path
# ---------------------------------------------------------------------

def make_output_path(
    input_path: Path,
    input_root: Path,
    output_root: Path,
) -> Path:

    relative = (
        input_path.relative_to(
            input_root
        )
    )

    output_path = (
        output_root
        / relative
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    return output_path


# ---------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------

def save_normalized(
    output_path: Path,
    normalized: np.ndarray,
    global_features: dict[str, np.ndarray],
    body_scale: float,
    source_path: Path,
    derived: dict[str, np.ndarray],
    reconstruction_error: dict[str, float],
) -> None:

    payload: dict[str, Any] = {}

    # ==============================================================
    # MAIN LOCAL REPRESENTATION
    # ==============================================================

    payload["full"] = normalized

    # ==============================================================
    # GLOBAL ROOT MOTION
    # ==============================================================

    payload[
        "root_positions"
    ] = global_features[
        "root_positions"
    ]

    payload[
        "root_positions_normalized"
    ] = global_features[
        "root_positions_normalized"
    ]

    payload[
        "root_displacement"
    ] = global_features[
        "root_displacement"
    ]

    payload[
        "root_displacement_normalized"
    ] = global_features[
        "root_displacement_normalized"
    ]

    payload[
        "root_velocity"
    ] = global_features[
        "root_velocity"
    ]

    payload[
        "root_velocity_normalized"
    ] = global_features[
        "root_velocity_normalized"
    ]

    # ==============================================================
    # SCALE
    # ==============================================================

    payload[
        "body_scale"
    ] = np.float32(
        body_scale
    )

    # ==============================================================
    # METADATA
    # ==============================================================

    payload[
        "source"
    ] = np.array(
        str(source_path),
        dtype=np.str_,
    )

    payload[
        "representation"
    ] = np.array(
        "smplx_127",
        dtype=np.str_,
    )

    payload[
        "normalization"
    ] = np.array(
        "local_root_centered_sequence_body_scale",
        dtype=np.str_,
    )

    payload[
        "root_joint_index"
    ] = np.int32(
        ROOT_JOINT_INDEX
    )

    payload[
        "global_motion"
    ] = np.array(
        "preserved",
        dtype=np.str_,
    )

    payload[
        "root_velocity_unit"
    ] = np.array(
        "dataset_units_per_frame",
        dtype=np.str_,
    )

    # ==============================================================
    # RECONSTRUCTION CHECK
    # ==============================================================

    payload[
        "reconstruction_max_abs_error"
    ] = np.float64(
        reconstruction_error[
            "max_abs_error"
        ]
    )

    payload[
        "reconstruction_mean_abs_error"
    ] = np.float64(
        reconstruction_error[
            "mean_abs_error"
        ]
    )

    payload[
        "reconstruction_rmse"
    ] = np.float64(
        reconstruction_error[
            "rmse"
        ]
    )

    # ==============================================================
    # DERIVED REPRESENTATIONS
    #
    # These are preserved exactly as they were in Stage 03.
    # ==============================================================
    
    for key, value in derived.items():

        payload[key] = value

    # ==============================================================
    # SAVE
    # ==============================================================

    np.savez_compressed(
        output_path,
        **payload,
    )


# ---------------------------------------------------------------------
# Process one file
# ---------------------------------------------------------------------

def process_one(
    input_path: Path,
    input_root: Path,
    output_root: Path,
) -> dict[str, Any]:

    log(
        f"Loading: {input_path}"
    )

    joints, derived = (
        load_canonical_and_derived(
            input_path
        )
    )

    log(
        f"Canonical shape: {joints.shape}"
    )

    # ==============================================================
    # LOCAL NORMALIZATION
    # ==============================================================

    normalized, root_positions, body_scale = (
        normalize_local_motion(
            joints
        )
    )

    # ==============================================================
    # GLOBAL MOTION
    # ==============================================================

    global_features = (
        compute_global_motion_features(
            root_positions=root_positions,
            body_scale=body_scale,
        )
    )

    # ==============================================================
    # RECONSTRUCTION
    # ==============================================================

    reconstructed = (
        reconstruct_original_motion(
            normalized=normalized,
            root_positions=root_positions,
            body_scale=body_scale,
        )
    )

    reconstruction_error = (
        compute_reconstruction_error(
            original=joints,
            reconstructed=reconstructed,
        )
    )

    # ==============================================================
    # SAFETY CHECK
    # ==============================================================

    if (
        reconstruction_error[
            "max_abs_error"
        ]
        > 1e-4
    ):
        raise ValueError(
            "Reconstruction error is too large: "
            f"{reconstruction_error}"
        )

    # ==============================================================
    # OUTPUT PATH
    # ==============================================================

    output_path = make_output_path(
        input_path=input_path,
        input_root=input_root,
        output_root=output_root,
    )

    # ==============================================================
    # SAVE
    # ==============================================================

    save_normalized(
        output_path=output_path,
        normalized=normalized,
        global_features=global_features,
        body_scale=body_scale,
        source_path=input_path,
        derived=derived,
        reconstruction_error=reconstruction_error,
    )

    # ==============================================================
    # LOG
    # ==============================================================

    log(
        f"Saved: {output_path}"
    )

    log(
        f"  full: "
        f"{joints.shape} -> "
        f"{normalized.shape}"
    )

    log(
        f"  body scale: "
        f"{body_scale:.8f}"
    )

    log(
        "  root_positions: "
        f"{global_features['root_positions'].shape}"
    )

    log(
        "  root_positions_normalized: "
        f"{global_features['root_positions_normalized'].shape}"
    )

    log(
        "  root_displacement: "
        f"{global_features['root_displacement'].shape}"
    )

    log(
        "  root_velocity: "
        f"{global_features['root_velocity'].shape}"
    )

    log(
        "  reconstruction max error: "
        f"{reconstruction_error['max_abs_error']:.10e}"
    )

    return {
        "input": str(input_path),
        "output": str(output_path),

        "frames": int(
            joints.shape[0]
        ),

        "input_shape": list(
            joints.shape
        ),

        "output_shape": list(
            normalized.shape
        ),

        "body_scale": float(
            body_scale
        ),

        "global_features": {
            key: list(value.shape)
            for key, value
            in global_features.items()
        },

        "derived_shapes": {
            key: list(value.shape)
            for key, value
            in derived.items()
        },

        "reconstruction": (
            reconstruction_error
        ),

        "status": "success",
    }


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:

    args = parse_args()

    (
        script_path,
        project_root,
        input_root,
        output_root,
    ) = resolve_roots(args)

    print(
        "[04_normalize_motion] "
        + "=" * 70
    )

    log(
        "04_normalize_motion"
    )

    print(
        "[04_normalize_motion] "
        + "=" * 70
    )

    log(
        f"Project root : {project_root}"
    )

    log(
        f"Input root   : {input_root}"
    )

    log(
        f"Output root  : {output_root}"
    )

    log(
        "Canonical representation: SMPL-X 127"
    )

    log(
        "Local normalization: "
        "root-centered + sequence-level body scale"
    )

    log(
        "Global root motion: PRESERVED"
    )

    log(
        "Global trajectory: "
        "initial-offset removed + body-scale normalized"
    )

    log(
        "Root velocity: "
        "dataset units per frame"
    )

    log(
        "Reconstruction check: ENABLED"
    )

    log(
        "Canonical joint information will NOT be reduced."
    )

    log(
        "Canonical tensor key: 'full'"
    )

    # --------------------------------------------------------------
    # Validate input
    # --------------------------------------------------------------

    if not input_root.exists():

        raise FileNotFoundError(
            f"Input root does not exist: "
            f"{input_root}"
        )

    output_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------------
    # Find files
    # --------------------------------------------------------------

    files = sorted(
        input_root.rglob("*.npz")
    )

    if args.limit is not None:

        if args.limit <= 0:

            raise ValueError(
                "--limit must be greater than zero."
            )

        files = files[
            : args.limit
        ]

    log(
        f"Found {len(files)} NPZ files."
    )

    # --------------------------------------------------------------
    # Process
    # --------------------------------------------------------------

    processed = 0
    failed = 0

    results: list[
        dict[str, Any]
    ] = []

    failed_files: list[str] = []

    for index, input_path in enumerate(
        files,
        start=1,
    ):

        log(
            f"[{index}/{len(files)}]"
        )

        try:

            result = process_one(
                input_path=input_path,
                input_root=input_root,
                output_root=output_root,
            )

            results.append(
                result
            )

            processed += 1

        except Exception as exc:

            failed += 1

            error(
                str(exc)
            )

            warn(
                f"FAILED: {input_path}"
            )

            warn(
                f"Reason: {exc}"
            )

            failed_files.append(
                str(input_path)
            )

            results.append(
                {
                    "input": str(
                        input_path
                    ),
                    "status": "failed",
                    "error": str(exc),
                }
            )

    # --------------------------------------------------------------
    # Summary
    # --------------------------------------------------------------

    summary = {

        "script": SCRIPT_NAME,

        "project_root": str(
            project_root
        ),

        "input_root": str(
            input_root
        ),

        "output_root": str(
            output_root
        ),

        "canonical_key": (
            CANONICAL_KEY
        ),

        "canonical_representation": (
            "SMPL-X 127"
        ),

        "canonical_shape": (
            "[T,127,3]"
        ),

        "root_joint_index": (
            ROOT_JOINT_INDEX
        ),

        "local_normalization": (
            "root-centered + "
            "sequence-level body scale"
        ),

        "global_motion": (
            "preserved"
        ),

        "global_normalization": (
            "root displacement from first frame "
            "+ sequence body scale"
        ),

        "root_velocity": (
            "frame-to-frame displacement"
        ),

        "canonical_information_reduced": (
            False
        ),

        "reconstruction_check": (
            True
        ),

        "processed": processed,

        "failed": failed,

        "files_found": len(files),

        "failed_files": failed_files,

        "results": results,
    }

    summary_path = (
        output_root
        / "_normalization_summary.json"
    )

    with open(
        summary_path,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            summary,
            f,
            indent=2,
            ensure_ascii=False,
        )

    log(
        f"Summary saved: "
        f"{summary_path}"
    )

    # --------------------------------------------------------------
    # Final output
    # --------------------------------------------------------------

    print(
        "[04_normalize_motion] "
        + "=" * 70
    )

    log("DONE")

    log(
        f"Processed : {processed}"
    )

    log(
        f"Failed    : {failed}"
    )

    if failed_files:

        print(
            "[04_normalize_motion] "
            "Failed files:"
        )

        for path in failed_files:

            print(
                "[04_normalize_motion]   "
                f"{path}"
            )

    print(
        "[04_normalize_motion] "
        + "=" * 70
    )


if __name__ == "__main__":
    main()