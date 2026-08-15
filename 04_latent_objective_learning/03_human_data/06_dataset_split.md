# Dataset Split

## 1. Purpose

The purpose of this stage is to define how the processed human motion
data is divided into training, validation, and held-out evaluation sets.

The main goal is to prevent data leakage and ensure that objective
inference is evaluated on motion that was not used during training.

The split must therefore be performed at the appropriate motion,
sequence, and subject level rather than by randomly splitting individual
frames.

---

## 2. Input

The input to this stage is the segmented human motion dataset produced
by:

    05_segmentation.md

Each sample may contain:

    motion
    features
    contacts
    metadata

Example:

    segment_00001
    segment_00002
    segment_00003
    ...

Each segment must retain information about its original source sequence
and subject where available.

---

## 3. Why Random Frame Splitting Is Not Allowed

Human motion is highly correlated over time.

For example:

    Sequence A

    Frame 1
    Frame 2
    Frame 3
       ...
    Frame 1000

Randomly placing frames from the same sequence into different datasets
would result in:

    Training
        ↓
    Frame 1, 2, 5, 10, ...

    Test
        ↓
    Frame 3, 4, 6, 11, ...

The model would therefore see extremely similar motion during training
and evaluation.

This would produce an overly optimistic estimate of generalization.

Therefore:

> Individual frames from the same source sequence must not be
> independently distributed across train, validation, and test sets.

---

## 4. Primary Split Principle

The primary split should be performed using the highest-level reliable
identity available in the dataset.

Preferred hierarchy:

    Subject
       ↓
    Motion Sequence
       ↓
    Segments

This means that segments originating from the same sequence should
remain in the same split.

When subject identity is reliably available, subject-level separation
should be preferred.

---

## 5. Dataset Structure

The resulting dataset should have the structure:

    data/

    ├── processed/
    │
    │   └── segments/
    │
    └── splits/
        ├── train/
        ├── validation/
        └── test/

The exact storage format may be adjusted during implementation.

---

## 6. Training Set

The training set contains motion segments used to develop and fit the
initial objective inference method.

The training set may be used for:

- Feature analysis
- Objective parameter estimation
- Model fitting
- Hyperparameter development

Training data must not contain samples from held-out evaluation
sequences.

---

## 7. Validation Set

The validation set is used for decisions made during development.

It may be used for:

- Hyperparameter selection
- Model selection
- Feature selection
- Representation comparison
- Threshold selection
- Early stopping

The validation set must remain separate from the final held-out
evaluation set.

---

## 8. Held-Out Test Set

The test set is reserved for final evaluation.

It should not be used to:

- Select features
- Tune hyperparameters
- Select the final model
- Adjust thresholds
- Make repeated development decisions

The purpose of the held-out test set is to estimate how well the
learned objective generalizes to previously unseen motion.

---

## 9. Subject-Level Generalization

If subject identifiers are available and sufficiently reliable, the
preferred split is:

    Training Subjects
          ↓
    Validation Subjects
          ↓
    Held-Out Subjects

For example:

    Subject A ──→ Train
    Subject B ──→ Train
    Subject C ──→ Validation
    Subject D ──→ Test

This tests whether the method can learn a behavioral structure that is
not specific to one individual.

---

## 10. Sequence-Level Generalization

When reliable subject identity is unavailable, the split should be
performed at the sequence level.

For example:

    Sequence 1 ──→ Train
    Sequence 2 ──→ Train
    Sequence 3 ──→ Validation
    Sequence 4 ──→ Test

All segments originating from a sequence must remain in the same split.

---

## 11. Dataset-Level Considerations

AMASS combines multiple motion capture datasets.

Different subsets may contain differences in:

- Subjects
- Recording protocols
- Motion styles
- Capture systems
- FPS
- Available metadata

Therefore, the split must preserve the source metadata.

Each sample should retain at least:

    dataset
    subject_id (when available)
    sequence_id
    segment_id

This information is required for leakage detection and later analysis.

---

## 12. Cross-Dataset Evaluation

A separate cross-dataset evaluation may be useful for testing stronger
generalization.

For example:

    Training:
        CMU
        KIT

    Evaluation:
        HumanEva

This evaluates whether the learned representation or objective
generalizes across different motion-capture datasets.

However, this should be treated as an additional evaluation protocol
rather than automatically replacing the primary split.

---

## 13. Recommended Initial Split

For the first experiments, the project should use:

    Train
        ↓
    Validation
        ↓
    Held-Out Test

with approximately:

    70% Train
    15% Validation
    15% Test

when the available number of subjects or sequences is sufficiently
large.

These percentages are guidelines rather than fixed requirements.

The actual split should be determined by the number of independent
subjects and sequences available.

---

## 14. Small Dataset Consideration

If the number of independent subjects or sequences is too small for a
reliable fixed split, a simple percentage split may not be appropriate.

In that case, subject-level or sequence-level cross-validation may be
considered.

For example:

    Fold 1:
        Train → Subjects A,B,C
        Test  → Subject D

    Fold 2:
        Train → Subjects A,B,D
        Test  → Subject C

The final evaluation procedure must be defined before reporting results.

---

## 15. Avoiding Feature Leakage

Feature normalization must also respect the dataset split.

For example, if standardization is used:

    Training Data
        ↓
    Estimate mean / std
        ↓
    Apply to Train
    Apply to Validation
    Apply to Test

The validation and test sets must not be used to estimate normalization
parameters.

Incorrect:

    Train + Validation + Test
            ↓
       Compute Statistics

Correct:

    Train
      ↓
    Compute Statistics
      ↓
    Apply to all splits

---

## 16. Avoiding Segmentation Leakage

Segmentation must be completed before the final dataset split.

However, all segments originating from the same source sequence must
remain within the same split.

For example:

    Sequence A

    ├── Segment 1
    ├── Segment 2
    ├── Segment 3
    └── Segment 4

Correct:

    Train
    └── Sequence A
        ├── Segment 1
        ├── Segment 2
        ├── Segment 3
        └── Segment 4

Incorrect:

    Train
    ├── Segment 1
    └── Segment 2

    Test
    ├── Segment 3
    └── Segment 4

The incorrect approach creates strong temporal leakage.

---

## 17. Metadata Manifest

A dataset manifest should be generated describing every sample.

Example:

    sample_id
    dataset
    subject_id
    sequence_id
    segment_id
    split
    start_frame
    end_frame
    duration
    fps

Example:

    sample_00001
        dataset: CMU
        subject: 31
        sequence: 31_01
        segment: 03
        split: train

This manifest provides a reproducible record of the dataset split.

---

## 18. Split Reproducibility

The split procedure must be deterministic.

A fixed random seed should be used whenever random selection is required.

Example:

    random_seed = 42

The seed and split configuration should be stored with the experiment
metadata.

The same source data and configuration should therefore produce the
same dataset split.

---

## 19. Split Validation

After creating the splits, the system should automatically verify:

### Sequence Leakage

No sequence appears in more than one split.

### Subject Leakage

When subject identifiers are available, no held-out subject appears in
training.

### Segment Leakage

No segments from the same source sequence are distributed across
different splits.

### Feature Leakage

Normalization and preprocessing statistics are computed only from the
training set where applicable.

### Metadata Integrity

Every sample has valid:

    dataset
    sequence_id
    segment_id
    split

---

## 20. Split Statistics

The following statistics should be generated:

- Number of subjects
- Number of sequences
- Number of segments
- Number of frames
- Motion duration
- Dataset distribution
- Feature distribution

Example:

    Split        Subjects    Sequences    Segments
    ------------------------------------------------
    Train           20          150          1200
    Validation       5           35           280
    Test              5           35           290

The actual values will depend on the available AMASS data.

---

## 21. Dataset Balance

The split should avoid severe imbalance when possible.

Potential sources of imbalance include:

- Different numbers of sequences per subject
- Different sequence lengths
- Different motion types
- Different AMASS subsets

The project should report these distributions rather than silently
assuming that the dataset is balanced.

---

## 22. Relationship to Objective Learning

The purpose of the split is particularly important for the research
question.

The intended pipeline is:

    Human Demonstrations
            ↓
    Motion Representation
            ↓
    Feature Extraction
            ↓
    Segmentation
            ↓
    Dataset Split
            ↓
    Objective Inference
            ↓
    Held-Out Evaluation

The held-out data must represent motion that was not used to construct
the objective model.

Otherwise, it would be difficult to determine whether the learned
objective captures a general behavioral principle or simply memorizes
motion patterns.

---

## 23. Generalization Questions

The dataset split should allow the project to investigate several levels
of generalization.

### Within-Sequence

Not used as the primary evaluation because of strong temporal
correlation.

### Unseen Sequence

Can the method generalize to a new motion sequence?

### Unseen Subject

Can the method generalize to a different person?

### Unseen Dataset

Can the method generalize to motion captured under a different dataset
or protocol?

### Unseen Condition

Can the inferred objective explain motion under conditions not used
during development?

These levels should be evaluated separately when the available data
supports them.

---

## 24. Initial Research Decision

The initial dataset policy is:

1. Never randomly split individual frames.
2. Keep all segments from one source sequence in the same split.
3. Prefer subject-level separation when reliable subject identity exists.
4. Keep the final test set untouched during development.
5. Compute normalization statistics using training data only.
6. Store complete split metadata.
7. Validate the split automatically before objective learning.

This provides a clean foundation for objective inference and later
generalization experiments.

---

## 25. Expected Output

The dataset preparation stage should produce:

    data/
    └── splits/
        ├── train/
        ├── validation/
        └── test/

and:

    results/
    └── statistics/
        ├── split_statistics.json
        └── dataset_manifest.csv

Optional visualization outputs may include:

    results/
    └── visualizations/
        └── dataset_distribution/

---

## 26. Next Step

After the dataset split is validated, the human-data preparation stage
is complete.

The resulting pipeline is:

    AMASS
      ↓
    Preprocessing
      ↓
    Motion Representation
      ↓
    Feature Extraction
      ↓
    Motion Segmentation
      ↓
    Dataset Split
      ↓
    Human Objective Learning

The next stage is to construct the objective representation and determine
how candidate behavioral variables can be converted into a model that
can be inferred from human demonstrations.

---

## Status

Dataset preparation:

**Defined**

Data leakage policy:

**Defined**

Primary split:

**Subject-level when possible, otherwise sequence-level**

Held-out evaluation:

**Required**

Final objective:

**Not yet established**

Next stage:

**Objective Representation / Objective Learning**
