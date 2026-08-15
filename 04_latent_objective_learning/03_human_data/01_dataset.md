# Human Motion Dataset

## 1. Purpose

This stage defines the human motion data used for the latent human
objective learning pipeline.

The purpose is not to learn the human objective yet.

The purpose is to select and organize human motion demonstrations
that can later be used to investigate which behavioral properties
can explain the observed motion.

The resulting dataset will be used by the following stages:

    Human Demonstrations
            ↓
    Motion Representation
            ↓
    Objective Representation
            ↓
    Objective Learning


---

## 2. Dataset

The primary human motion dataset is:

**AMASS — Archive of Motion Capture as Surface Shapes**

AMASS provides a large collection of human motion capture data
represented using a common human body model representation.

The project uses AMASS as the source of human locomotion
demonstrations.

Official dataset:

https://amass.is.tue.mpg.de/


---

## 3. Research Role of AMASS

AMASS is used as a source of human demonstrations.

The role of the dataset in this project is:

    Human Motion Capture
            ↓
    Human Demonstrations
            ↓
    Structured Motion Representation
            ↓
    Objective Learning

We do NOT assume that AMASS directly contains human objectives.

The objective must be inferred from the observed movement.


---

## 4. Initial Dataset Scope

The initial experiments will focus on human motions relevant to
locomotion and whole-body movement.

The initial dataset should prioritize sequences containing:

- Walking
- Locomotion
- Standing-to-walking transitions
- Walking-related whole-body motion

Other motion categories may be retained in the raw dataset but will
not automatically be included in the initial objective-learning
dataset.

This keeps the first experiments focused and reduces unnecessary
variation.


---

## 5. AMASS Subsets

The existing processing pipeline supports multiple AMASS subsets:

    ACCAD
    BMLmovi
    BMLrub
    CMU
    DanceDB
    GRAB
    HumanEva
    KIT
    MPI_HDM05

These datasets provide different types of human motion.

For the initial research stage, the project should not require
processing the entire AMASS collection.

A smaller locomotion-focused subset can be used first for pipeline
development and validation.

The dataset can be expanded later if additional motion diversity is
required.


---

## 6. Raw Data

AMASS motion files are distributed as `.npz` files.

A typical sequence contains information such as:

    poses
    betas
    trans
    dmpls
    mocap_framerate
    gender

Example:

    poses:
    (number_of_frames, 156)

    betas:
    (16,)

The raw data will remain in:

    data/raw/


Raw AMASS files are not stored in the GitHub repository because of
dataset size and licensing requirements.


---

## 7. Human Body Representation

The raw AMASS motion parameters will be converted into a structured
3D human representation using SMPL-X.

The processing pipeline is:

    AMASS
       ↓
    SMPL-X
       ↓
    3D Human Body
       ↓
    3D Joint Motion


The resulting joint representation provides the basis for subsequent
motion analysis.

The project does not require the full human mesh for every downstream
experiment.

Where possible, joint-level representations will be used to reduce
storage and computational requirements.


---

## 8. Motion Representation

For the initial objective-learning pipeline, the primary representation
will be temporal human joint motion.

Conceptually:

    X = {x_t}_{t=1}^T

where:

    x_t = human joint state at time t

The representation may contain:

- Joint positions
- Joint velocities
- Joint accelerations
- Root/body motion
- Contact information

The exact feature set is defined in:

    04_feature_extraction.md

Therefore, this file does not assume that every available quantity
will necessarily be used for objective learning.


---

## 9. Why Use Human Demonstrations Instead of Trajectory Matching?

The research goal is not to reproduce a human trajectory directly.

Instead:

    Human Demonstration
            ↓
    Infer Behavioral Objective
            ↓
    Optimize Objective
            ↓
    Robot Generates Its Own Motion

Therefore, the dataset must preserve the information required to
reason about the characteristics of human movement rather than only
store target joint trajectories.


---

## 10. Demonstration Unit

The basic unit of the learning dataset will be a segmented human
motion sequence.

Conceptually:

    Full Motion Sequence
            ↓
        Segmentation
            ↓
    Motion Demonstration

Each demonstration should preserve:

- Temporal ordering
- Joint configuration
- Motion dynamics
- Relevant contact information
- Sequence metadata

The segmentation procedure is defined separately in:

    05_segmentation.md


---

## 11. Metadata

Each processed demonstration should maintain metadata describing the
source sequence.

Possible metadata includes:

- Dataset subset
- Sequence identifier
- Frame rate
- Number of frames
- Motion duration
- Subject identifier when available
- Motion category when available
- Processing status

Metadata is important for:

- Dataset analysis
- Train/validation/test splitting
- Reproducibility
- Held-out evaluation


---

## 12. Data Quality Requirements

Before a sequence enters the learning dataset, it should pass basic
quality checks.

The pipeline should verify:

- Valid motion file
- Valid SMPL-X reconstruction
- No unexpected missing values
- Valid joint dimensions
- Consistent temporal ordering
- Valid frame rate
- Reasonable motion duration
- Valid numerical values

Invalid or corrupted sequences should be excluded from the processed
dataset rather than silently used.


---

## 13. Data Leakage Prevention

Dataset splitting must be performed carefully.

Sequences from the same subject or highly related motion recordings
should not be arbitrarily distributed across training and test sets
if this would allow information leakage.

The objective is to evaluate whether the learned representation
generalizes beyond the exact demonstrations used during learning.

The detailed splitting strategy is defined in:

    06_dataset_split.md


---

## 14. Initial Dataset Strategy

The project will follow a staged dataset strategy.

### Stage 1 — Pipeline Validation

Use a small number of representative sequences to validate:

    Loading
      ↓
    SMPL-X reconstruction
      ↓
    Joint extraction
      ↓
    Feature extraction
      ↓
    Segmentation
      ↓
    Dataset creation


### Stage 2 — Locomotion Dataset

Expand to a larger set of locomotion-related demonstrations.

### Stage 3 — Diversity and Generalization

Introduce additional subjects, datasets, and motion variations to
evaluate whether the learned objective remains meaningful across
different demonstrations.


---

## 15. What We Are NOT Assuming

At this stage we do NOT assume:

- That all AMASS motions are relevant
- That every AMASS subset is required
- That walking has one universal objective
- That a particular feature is the human objective
- That energy is the objective
- That stability is the objective
- That smoothness is the objective
- That the objective can be directly read from AMASS
- That the entire AMASS dataset must be processed before experiments
  can begin

These questions will be addressed in later stages.


---

## 16. Dataset Pipeline

The resulting data pipeline is:

    AMASS Raw Data
          ↓
    Sequence Selection
          ↓
    SMPL-X Reconstruction
          ↓
    3D Joint Motion
          ↓
    Normalization
          ↓
    Feature Extraction
          ↓
    Contact Detection
          ↓
    Motion Segmentation
          ↓
    Dataset Split
          ↓
    Learning-Ready Demonstrations


---

## 17. Output

The processed dataset will be organized as:

    data/

    ├── raw/
    │
    ├── processed/
    │
    └── splits/

The processed dataset should contain the information required by the
next research stage:

    04_objective_representation/


---

## 18. Relation to the Research Question

The research question asks whether an objective inferred from human
locomotion can remain meaningful when optimized under the dynamics
and constraints of a different humanoid robot.

Therefore, this dataset stage provides the first required input:

    Human Locomotion Demonstrations
                ↓
        Objective Inference


The actual objective inference is NOT performed in this stage.

It begins in the subsequent objective representation and learning
stages.


---

## Status

Dataset source:

**AMASS**

Initial focus:

**Human locomotion demonstrations**

Primary representation:

**SMPL-X-based 3D joint motion**

Dataset preparation:

**In progress**

Objective learning:

**Not yet started**

Next step:

**Define the preprocessing pipeline in `02_preprocessing.md`.**
