# Human Motion Preprocessing

## 1. Purpose

The purpose of preprocessing is to convert raw AMASS motion
sequences into clean, consistent, and learning-ready human motion
data.

The preprocessing stage prepares the demonstrations for subsequent
motion representation and objective learning.

The pipeline is:

    Raw AMASS
        ↓
    Load Motion
        ↓
    SMPL-X Reconstruction
        ↓
    Joint Extraction
        ↓
    Coordinate Normalization
        ↓
    Temporal Validation
        ↓
    Processed Human Motion


---

## 2. Input

The input consists of raw AMASS motion capture sequences.

Typical AMASS files contain:

    poses
    betas
    trans
    mocap_framerate
    gender

The raw files are stored under:

    data/raw/


Raw AMASS data is not modified directly.

All processed outputs are stored under:

    data/processed/


---

## 3. Preprocessing Pipeline

The complete preprocessing pipeline is:

    AMASS Raw Sequence
            ↓
    Load and Validate Input
            ↓
    SMPL-X Reconstruction
            ↓
    Extract Human Joints
            ↓
    Normalize Motion
            ↓
    Validate Temporal Sequence
            ↓
    Save Processed Motion


The implementation is organized through the scripts:

    01_load_amass.py
    02_smplx_reconstruction.py
    03_extract_joints.py
    04_normalize_motion.py


---

## 4. Step 1 — Load AMASS

The first step loads the AMASS `.npz` file and checks its contents.

The loader should identify:

- Pose parameters
- Body shape parameters
- Global translation
- Frame rate
- Sequence length
- Dataset and sequence identifiers

Example:

    poses:
    (T, 156)

    trans:
    (T, 3)

where `T` is the number of frames.

The loader should reject sequences that cannot be parsed correctly.


---

## 5. Step 2 — SMPL-X Reconstruction

AMASS pose parameters are converted into a 3D human body
representation using SMPL-X.

The transformation is:

    AMASS Pose Parameters
            ↓
          SMPL-X
            ↓
    3D Human Body
            ↓
    Human Joints


The reconstruction provides a consistent human body representation
for subsequent processing.

The full mesh may be generated for validation and visualization,
but downstream processing should primarily rely on the joint
representation when possible.


---

## 6. Step 3 — Joint Extraction

The reconstructed SMPL-X representation is converted into a
joint-based representation.

For each frame:

    J_t ∈ R^(N × 3)

where:

- `T` = number of frames
- `N` = number of selected joints
- `3` = XYZ coordinates

The complete sequence can therefore be represented as:

    J ∈ R^(T × N × 3)


The exact joint subset should be kept consistent across all
sequences.


---

## 7. Coordinate Representation

Human motion contains both global movement and body-relative
movement.

The preprocessing pipeline should preserve sufficient information
to distinguish:

- Global/root motion
- Relative joint configuration
- Temporal movement

The representation used for objective learning should therefore not
silently discard root information.

When normalization is applied, the transformation should be recorded
so that the original coordinate interpretation can be recovered when
necessary.


---

## 8. Step 4 — Motion Normalization

Human demonstrations may differ in:

- Global position
- Orientation
- Body scale
- Frame rate
- Sequence length

Normalization is applied to make sequences comparable.

The initial normalization should focus on removing irrelevant
coordinate differences while preserving movement characteristics.

Possible operations include:

- Root-centered coordinates
- Consistent coordinate orientation
- Temporal resampling when required
- Consistent numerical units

Normalization must not remove information that may later be relevant
to the objective.

For this reason, every normalization operation should be explicitly
documented and reproducible.


---

## 9. Temporal Processing

Human motion is inherently temporal.

The preprocessing stage must preserve the temporal ordering:

    x_1 → x_2 → x_3 → ... → x_T


Temporal information is required for later computation of:

- Velocity
- Acceleration
- Contact events
- Motion segments
- Dynamic movement characteristics


Therefore, preprocessing must not treat individual frames as
independent samples.


---

## 10. Frame Rate

AMASS sequences may have different motion capture frequencies.

The original frame rate should be stored as metadata.

If temporal resampling is required, the target frame rate must be
defined explicitly and applied consistently.

For a sequence sampled at:

    Δt

velocity can later be estimated as:

    v_t ≈ (x_t - x_(t-1)) / Δt


Therefore, frame rate information must not be discarded.


---

## 11. Missing and Invalid Data

Each sequence should be checked for:

- NaN values
- Infinite values
- Invalid joint coordinates
- Missing frames
- Invalid frame rate
- Failed SMPL-X reconstruction

Invalid sequences should be flagged or excluded from the processed
dataset.

The preprocessing pipeline should report exclusions rather than
silently removing data.


---

## 12. Motion Continuity

Human demonstrations should be checked for unreasonable temporal
discontinuities.

For example:

    x_t → x_(t+1)

should not contain unexplained numerical jumps caused by:

- Processing errors
- Corrupted input
- Coordinate discontinuities
- Reconstruction failures


Large changes should be detected and recorded for later inspection.

A detected discontinuity does not automatically mean that the motion
is invalid; it should first be distinguished from genuine rapid human
movement.


---

## 13. Subject and Sequence Identity

Metadata should be preserved during preprocessing.

Each processed sequence should retain information such as:

- Dataset
- Sequence ID
- Subject ID when available
- Original frame rate
- Number of frames
- Processing version

This information is important for preventing data leakage during
dataset splitting.


---

## 14. Output Format

Processed sequences should be stored under:

    data/processed/


A processed sequence should contain at minimum:

    joints
    root_motion
    fps
    metadata


Additional information may be added in later stages.

The exact feature representation is defined separately in:

    04_feature_extraction.md


---

## 15. Reproducibility

Preprocessing must be deterministic and reproducible.

The pipeline should record:

- Source dataset
- Source sequence
- SMPL-X model version
- Joint definition
- Coordinate convention
- Normalization procedure
- Target frame rate if resampling is used
- Processing version


The same raw input and preprocessing configuration should produce
the same processed representation.


---

## 16. Preprocessing Does Not Define the Human Objective

An important research boundary is maintained here.

Preprocessing produces:

    Human Demonstration
            ↓
    Structured Motion

It does NOT produce:

    Human Demonstration
            ↓
    Human Objective


The objective is investigated in later stages.

In particular, preprocessing does not assume that:

- Energy is the objective
- Stability is the objective
- Smoothness is the objective
- Robustness is the objective

These remain research hypotheses.


---

## 17. Quality Control

After preprocessing, the pipeline should generate basic validation
statistics.

Examples include:

- Number of processed sequences
- Number of rejected sequences
- Sequence duration
- Frame rate distribution
- Joint coordinate ranges
- Missing-value count
- Reconstruction failures
- Temporal discontinuities


These statistics should be stored under:

    results/statistics/


Visual inspection results should be stored under:

    results/visualizations/


---

## 18. Processing Scripts

The preprocessing stage uses:

### `01_load_amass.py`

Loads and validates raw AMASS sequences.

### `02_smplx_reconstruction.py`

Converts AMASS pose parameters into SMPL-X body and joint
representations.

### `03_extract_joints.py`

Extracts the selected joint representation.

### `04_normalize_motion.py`

Applies the defined coordinate and temporal normalization.

Later stages operate on the processed motion data.


---

## 19. Result

The output of preprocessing is:

    Raw AMASS
        ↓
    Validated Human Motion
        ↓
    SMPL-X Representation
        ↓
    Consistent Joint Coordinates
        ↓
    Normalized Temporal Motion
        ↓
    Processed Demonstrations


These demonstrations are then ready for:

    Motion Representation
            ↓
    Feature Extraction
            ↓
    Segmentation
            ↓
    Dataset Construction
            ↓
    Objective Representation
            ↓
    Objective Learning


---

## Status

Dataset selection:

**Defined**

Raw AMASS processing:

**Pipeline defined**

SMPL-X reconstruction:

**Required**

Joint representation:

**Defined at pipeline level**

Normalization:

**Preliminary**

Objective inference:

**Not part of preprocessing**

Next step:

**Define the human motion representation in
`03_motion_representation.md`.**
