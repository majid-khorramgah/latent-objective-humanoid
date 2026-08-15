# Dataset Split

## 1. Purpose

The purpose of this stage is to define how the processed and segmented
human motion data is divided into training, validation, and held-out
evaluation sets.

The split must ensure that objective-learning experiments measure
generalization to unseen human motion rather than memorization of highly
similar motion sequences.

The main principle is:

    Human Motion Data
            ↓
        Grouped Split
            ↓
    Train / Validation / Held-Out
            ↓
    Objective Learning
            ↓
    Unseen Motion Evaluation

---

## 2. Input

The input to this stage is the segmented human motion dataset generated
by:

    05_segmentation.md

Each sample may contain:

- Motion sequence
- 3D joint positions
- Velocity
- Acceleration
- Root motion
- Contact information
- Extracted features
- Sequence metadata

Example:

    CMU_31_01_segment_0001
    CMU_31_01_segment_0002
    CMU_31_01_segment_0003

---

## 3. Main Requirement: Avoid Data Leakage

The most important requirement is to prevent highly related motion
segments from appearing in different dataset splits.

For example:

    Original Sequence
          ↓
    Segment 1
    Segment 2
    Segment 3

These segments must remain in the same split.

They must NOT be distributed as:

    Train     → Segment 1
    Validation → Segment 2
    Test      → Segment 3

because the model could effectively see almost the same motion during
training and evaluation.

Therefore, splitting must be performed at the sequence or higher-level
group rather than at the individual segment level.

---

## 4. Grouping Principle

Each motion sample should retain information about its origin.

At minimum:

    dataset
    sequence_id
    subject_id (when available)

This information is used to define groups.

Conceptually:

    Raw Sequence
         ↓
    Segmentation
         ↓
    Multiple Segments
         ↓
    Same Group
         ↓
    One Dataset Split

This preserves independence between training and evaluation data.

---

## 5. Initial Dataset Structure

The initial split will contain three subsets:

### Training Set

Used for:

- Objective representation development
- Objective learning
- Model fitting

### Validation Set

Used for:

- Hyperparameter selection
- Model comparison
- Feature selection
- Early stopping where applicable

### Held-Out Evaluation Set

Used only for final evaluation.

The held-out set must not be used to tune the objective model.

---

## 6. Conceptual Split

The initial organization is:

    Human Motion Dataset
            |
            +-------------------+
            |                   |
          Train              Validation
            |
            +-------------------+
                                |
                           Held-Out Test

A nominal starting ratio may be:

    Train       70%
    Validation  15%
    Held-Out    15%

However, the exact ratio is less important than preserving group-level
independence.

The final split should be determined after inspecting the available
datasets and subjects.

---

## 7. Subject-Level Separation

Where subject identity is available, subject-level separation should be
preferred when possible.

For example:

    Training Subjects
          ≠
    Validation Subjects
          ≠
    Held-Out Subjects

This provides a stronger test of whether the learned objective captures
behavioral structure rather than individual-specific motion patterns.

The project should preserve subject identity whenever the source dataset
provides it.

---

## 8. Sequence-Level Separation

If reliable subject identity is unavailable, splitting should occur at
the sequence level.

For example:

    Sequence A
    Sequence B
    Sequence C

may be assigned as:

    Train:
        A

    Validation:
        B

    Held-Out:
        C

All segments originating from a sequence remain together.

---

## 9. Dataset-Level Separation

The project may also contain multiple AMASS source datasets:

    CMU
    KIT
    ACCAD
    BMLrub
    BMLmovi
    HumanEva
    DanceDB
    GRAB
    MPI_HDM05

The source dataset identity should be preserved.

Dataset-level evaluation may later be used as an additional
generalization experiment.

For example:

    Train:
        CMU + KIT

    Held-Out:
        HumanEva

Such a split can test whether the learned representation transfers
across motion-capture datasets.

This should be treated as an additional experiment rather than assumed
to be the only evaluation protocol.

---

## 10. Initial Split Strategy

The initial dataset construction should follow this priority:

    1. Subject-level split when reliable subject IDs exist
            ↓
    2. Sequence-level split when subject IDs are unavailable
            ↓
    3. Dataset-level held-out experiments for additional analysis

The project should not randomly split individual motion frames.

---

## 11. Reproducibility

The split must be deterministic.

A fixed random seed should be recorded when randomized grouping is used.

Example metadata:

```text
split_seed
split_method
train_groups
validation_groups
heldout_groups
