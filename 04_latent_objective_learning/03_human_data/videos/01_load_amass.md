# 01 — AMASS Dataset Loading and Inventory

[▶️ Watch the execution video on YouTube](https://youtu.be/sf4N8_fzn04)

## Purpose

This step performs the initial inspection and inventory of the AMASS motion dataset used in the human-data pipeline.

The script recursively scans the available AMASS subsets, identifies motion `.npz` files, validates their required fields, and generates dataset-level statistics.

The raw AMASS files are not modified.

## What the Script Does

The pipeline performs the following operations:

1. Discovers available AMASS datasets.
2. Recursively searches for `.npz` files.
3. Identifies motion files.
4. Checks whether required AMASS fields are present.
5. Records the shape of the motion data.
6. Records the number of frames.
7. Records motion-capture frequency when available.
8. Separates valid and invalid files.
9. Computes dataset-level statistics.
10. Generates machine-readable inventory reports.

Required motion fields include:

- `poses`
- `trans`

Additional fields such as `betas`, `dmpls`, `gender`, and `mocap_framerate` are recorded when available.

## Dataset Inventory

The scan identified:

| Dataset | Files | Valid | Invalid |
|---|---:|---:|---:|
| ACCAD | 252 | 252 | 0 |
| BMLmovi | 1,887 | 1,801 | 86 |
| BMLrub | 3,061 | 3,061 | 0 |
| CMU | 2,088 | 2,082 | 6 |
| DanceDB | 173 | 153 | 20 |
| GRAB | 1,350 | 1,340 | 10 |
| HumanEva | 28 | 28 | 0 |
| KIT | 4,232 | 4,232 | 0 |
| MPI_HDM05 | 215 | 215 | 0 |
| **Total** | **13,286** | **13,164** | **122** |

The valid sequences contain a total of:

**16,894,522 frames**

## Output Reports

The execution generates two reports:

### Dataset Inventory

`results/statistics/amass_dataset_inventory.json`

This file contains:

- Dataset discovery information
- Total number of motion files
- Number of valid and invalid files
- Total frame count
- Dataset-level statistics
- Motion-capture frequencies
- Details of invalid files

### Motion File Inventory

`results/statistics/amass_motion_files.csv`

This file provides a row-level inventory of the discovered motion files, including:

- Dataset
- Relative file path
- Filename
- Validation status
- AMASS fields
- Pose shape
- Translation shape
- Body-shape information
- Number of frames
- Pose dimensionality
- Frame rate
- Gender

## Example Motion Record

A typical valid AMASS sequence contains:

- `poses`: `(N, 156)`
- `trans`: `(N, 3)`
- `betas`: `(16,)`
- `dmpls`: `(N, 8)`
- `mocap_framerate`: dataset-dependent

For example, one ACCAD sequence contains:

- 360 frames
- 156-dimensional pose representation
- 3D global translation
- 120 Hz motion-capture frequency

## Invalid Files

The validation stage identified 122 files that do not satisfy the required motion-file structure.

For example, some files such as `shape.npz` contain shape information but do not contain the required motion fields:

- `poses`
- `trans`

These files are therefore excluded from the valid motion inventory.

Importantly, they are not deleted or modified.

Their paths and validation errors are recorded in the generated reports for later inspection.

## Result

This step establishes a reproducible inventory of the human-motion data before any reconstruction, normalization, feature extraction, or segmentation is performed.

The result is:

```text
AMASS
  ↓
Dataset Discovery
  ↓
Motion File Validation
  ↓
13,286 files discovered
  ↓
13,164 valid motion files
  ↓
16,894,522 motion frames
  ↓
Dataset Inventory
