"""
01_load_amass.py

AMASS Dataset Discovery and Validation
--------------------------------------

This script recursively scans the local AMASS dataset directory,
discovers all available motion files, validates their structure,
and generates lightweight dataset statistics.

The raw AMASS files are NOT copied or modified.

Expected project structure:

latent-objective-humanoid/
│
├── 03_human_motion/
│   ├── data/
│   │   └── AMASS/
│   │       └── raw/
│   │           ├── ACCAD/
│   │           ├── BMLmovi/
│   │           ├── BMLrub/
│   │           ├── CMU/
│   │           ├── DanceDB/
│   │           ├── GRAB/
│   │           ├── HumanEva/
│   │           ├── KIT/
│   │           └── MPI_HDM05/
│   │
│   ├── results/
│   │   └── statistics/
│   │
│   └── scripts/
│       └── 01_load_amass.py
│
"""

from pathlib import Path
import json
import csv
from datetime import datetime

import numpy as np


# ============================================================
# Configuration
# ============================================================

# Project root:
# E:\latent-objective-humanoid
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# AMASS raw data directory
AMASS_RAW_DIR = (
    PROJECT_ROOT
    / "03_human_motion"
    / "data"
    / "AMASS"
    / "raw"
)

# Output directory
RESULTS_DIR = (
    PROJECT_ROOT
    / "03_human_motion"
    / "results"
    / "statistics"
)

# Output files
JSON_OUTPUT = RESULTS_DIR / "amass_dataset_inventory.json"
CSV_OUTPUT = RESULTS_DIR / "amass_motion_files.csv"


# Expected AMASS datasets
EXPECTED_DATASETS = [
    "ACCAD",
    "BMLmovi",
    "BMLrub",
    "CMU",
    "DanceDB",
    "GRAB",
    "HumanEva",
    "KIT",
    "MPI_HDM05",
]


# Expected AMASS fields
EXPECTED_FIELDS = [
    "poses",
    "betas",
    "trans",
    "dmpls",
    "mocap_framerate",
    "gender",
]


# ============================================================
# Utility Functions
# ============================================================

def safe_shape(value):
    """Return shape as a list if possible."""
    try:
        return list(value.shape)
    except Exception:
        return None


def safe_value(value):
    """Convert NumPy values into JSON-compatible Python values."""

    if isinstance(value, np.ndarray):

        if value.size == 1:
            return value.reshape(-1)[0].item()

        return {
            "shape": list(value.shape),
            "dtype": str(value.dtype),
        }

    if isinstance(value, np.generic):
        return value.item()

    return value


def get_dataset_name(file_path):
    """
    Identify the AMASS dataset from the directory structure.

    Example:
        raw/CMU/31/31_01_poses.npz

    returns:
        CMU
    """

    try:
        relative = file_path.relative_to(AMASS_RAW_DIR)

        if len(relative.parts) >= 2:
            return relative.parts[0]

    except ValueError:
        pass

    return "UNKNOWN"


def inspect_motion_file(file_path):
    """
    Inspect a single AMASS .npz motion file.

    Only metadata is collected.
    The file itself is never copied.
    """

    dataset = get_dataset_name(file_path)

    record = {
        "dataset": dataset,
        "relative_path": str(
            file_path.relative_to(PROJECT_ROOT)
        ).replace("\\", "/"),
        "filename": file_path.name,
        "valid": False,
        "error": None,
        "keys": [],
        "poses_shape": None,
        "trans_shape": None,
        "betas_shape": None,
        "dmpls_shape": None,
        "num_frames": None,
        "pose_dimensions": None,
        "fps": None,
        "gender": None,
    }

    try:

        with np.load(file_path, allow_pickle=True) as data:

            record["keys"] = sorted(data.files)

            # ------------------------------------------------
            # Pose information
            # ------------------------------------------------

            if "poses" in data:

                poses = data["poses"]

                record["poses_shape"] = safe_shape(poses)

                if poses.ndim >= 1:
                    record["num_frames"] = int(poses.shape[0])

                if poses.ndim >= 2:
                    record["pose_dimensions"] = int(
                        poses.shape[1]
                    )

            # ------------------------------------------------
            # Translation
            # ------------------------------------------------

            if "trans" in data:

                record["trans_shape"] = safe_shape(
                    data["trans"]
                )

            # ------------------------------------------------
            # Body shape
            # ------------------------------------------------

            if "betas" in data:

                record["betas_shape"] = safe_shape(
                    data["betas"]
                )

            # ------------------------------------------------
            # DMPL
            # ------------------------------------------------

            if "dmpls" in data:

                record["dmpls_shape"] = safe_shape(
                    data["dmpls"]
                )

            # ------------------------------------------------
            # FPS
            # ------------------------------------------------

            if "mocap_framerate" in data:

                fps = data["mocap_framerate"]

                try:
                    record["fps"] = float(
                        np.asarray(fps).reshape(-1)[0]
                    )
                except Exception:
                    record["fps"] = None

            # ------------------------------------------------
            # Gender
            # ------------------------------------------------

            if "gender" in data:

                try:

                    gender = data["gender"]

                    if isinstance(gender, np.ndarray):
                        gender = gender.reshape(-1)[0]

                    if isinstance(gender, bytes):
                        gender = gender.decode(
                            "utf-8",
                            errors="ignore"
                        )

                    record["gender"] = str(gender)

                except Exception:
                    record["gender"] = None

            # ------------------------------------------------
            # Basic validation
            # ------------------------------------------------

            required = ["poses", "trans"]

            missing = [
                key
                for key in required
                if key not in data
            ]

            if missing:

                record["error"] = (
                    "Missing required fields: "
                    + ", ".join(missing)
                )

            else:

                record["valid"] = True

    except Exception as exc:

        record["error"] = (
            f"{type(exc).__name__}: {exc}"
        )

    return record


# ============================================================
# Main Dataset Scan
# ============================================================

def main():

    print("=" * 70)
    print("AMASS DATASET DISCOVERY AND VALIDATION")
    print("=" * 70)

    print(f"\nProject root:")
    print(PROJECT_ROOT)

    print(f"\nAMASS raw directory:")
    print(AMASS_RAW_DIR)

    print(f"\nResults directory:")
    print(RESULTS_DIR)

    # --------------------------------------------------------
    # Check AMASS directory
    # --------------------------------------------------------

    if not AMASS_RAW_DIR.exists():

        print("\nERROR:")
        print("AMASS raw directory was not found.")

        print("\nExpected:")
        print(AMASS_RAW_DIR)

        return

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Discover datasets
    # --------------------------------------------------------

    discovered_datasets = sorted(
        [
            path.name
            for path in AMASS_RAW_DIR.iterdir()
            if path.is_dir()
        ]
    )

    print("\nDiscovered datasets:")

    for dataset in discovered_datasets:
        print(f"  [FOUND] {dataset}")

    print("\nExpected datasets:")

    for dataset in EXPECTED_DATASETS:

        if dataset in discovered_datasets:
            print(f"  [OK]    {dataset}")
        else:
            print(f"  [MISSING] {dataset}")

    # --------------------------------------------------------
    # Discover all NPZ files
    # --------------------------------------------------------

    motion_files = sorted(
        AMASS_RAW_DIR.rglob("*.npz")
    )

    print("\n" + "-" * 70)
    print(
        f"Total .npz files discovered: "
        f"{len(motion_files)}"
    )
    print("-" * 70)

    if not motion_files:

        print("\nNo AMASS .npz files were found.")

        return

    # --------------------------------------------------------
    # Inspect files
    # --------------------------------------------------------

    records = []

    for index, file_path in enumerate(
        motion_files,
        start=1
    ):

        print(
            f"[{index}/{len(motion_files)}] "
            f"{file_path.relative_to(AMASS_RAW_DIR)}"
        )

        record = inspect_motion_file(
            file_path
        )

        records.append(record)

    # --------------------------------------------------------
    # Dataset statistics
    # --------------------------------------------------------

    dataset_statistics = {}

    for dataset in discovered_datasets:

        dataset_records = [
            record
            for record in records
            if record["dataset"] == dataset
        ]

        valid_records = [
            record
            for record in dataset_records
            if record["valid"]
        ]

        invalid_records = [
            record
            for record in dataset_records
            if not record["valid"]
        ]

        total_frames = sum(
            record["num_frames"]
            for record in valid_records
            if record["num_frames"] is not None
        )

        fps_values = [
            record["fps"]
            for record in valid_records
            if record["fps"] is not None
        ]

        dataset_statistics[dataset] = {
            "motion_files": len(dataset_records),
            "valid_files": len(valid_records),
            "invalid_files": len(invalid_records),
            "total_frames": total_frames,
            "fps_values": sorted(
                list(set(fps_values))
            ),
        }

    # --------------------------------------------------------
    # Global statistics
    # --------------------------------------------------------

    valid_files = [
        record
        for record in records
        if record["valid"]
    ]

    invalid_files = [
        record
        for record in records
        if not record["valid"]
    ]

    total_frames = sum(
        record["num_frames"]
        for record in valid_files
        if record["num_frames"] is not None
    )

    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    report = {

        "generated_at": datetime.now().isoformat(),

        "project_root": str(
            PROJECT_ROOT
        ),

        "amass_raw_directory": str(
            AMASS_RAW_DIR
        ),

        "expected_datasets":
            EXPECTED_DATASETS,

        "discovered_datasets":
            discovered_datasets,

        "dataset_count":
            len(discovered_datasets),

        "total_npz_files":
            len(records),

        "valid_files":
            len(valid_files),

        "invalid_files":
            len(invalid_files),

        "total_frames":
            total_frames,

        "datasets":
            dataset_statistics,

        "invalid_file_details":
            [
                {
                    "dataset": record["dataset"],
                    "relative_path":
                        record["relative_path"],
                    "error":
                        record["error"],
                }
                for record in invalid_files
            ],
    }

    # --------------------------------------------------------
    # Save JSON report
    # --------------------------------------------------------

    with open(
        JSON_OUTPUT,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    # --------------------------------------------------------
    # Save CSV inventory
    # --------------------------------------------------------

    if records:

        fieldnames = list(
            records[0].keys()
        )

        with open(
            CSV_OUTPUT,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()

            writer.writerows(records)

    # --------------------------------------------------------
    # Print summary
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("SCAN COMPLETE")
    print("=" * 70)

    print(
        f"\nDatasets found: "
        f"{len(discovered_datasets)}"
    )

    print(
        f"Motion files: "
        f"{len(records)}"
    )

    print(
        f"Valid files: "
        f"{len(valid_files)}"
    )

    print(
        f"Invalid files: "
        f"{len(invalid_files)}"
    )

    print(
        f"Total frames: "
        f"{total_frames:,}"
    )

    print("\nDataset statistics:")

    for dataset, stats in dataset_statistics.items():

        print(
            f"  {dataset:12s} "
            f"{stats['motion_files']:6d} files | "
            f"{stats['valid_files']:6d} valid | "
            f"{stats['invalid_files']:6d} invalid"
        )

    print("\nReports generated:")

    print(
        f"  {JSON_OUTPUT}"
    )

    print(
        f"  {CSV_OUTPUT}"
    )

    print("\nRaw AMASS files were not modified.")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    main()
