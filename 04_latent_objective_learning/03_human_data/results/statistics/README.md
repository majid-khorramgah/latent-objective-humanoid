# Latent Objective Humanoid

**Repository:** [latent-objective-humanoid](https://github.com/majid-khorramgah/latent-objective-humanoid)

This project investigates a latent-objective framework for human motion processing and learning, with a focus on transforming motion-capture data into structured representations suitable for downstream latent-space learning and humanoid motion modeling.

---

## Human Motion Data Pipeline

The human-motion processing pipeline is organized under:

[04_latent_objective_learning](https://github.com/majid-khorramgah/latent-objective-humanoid/tree/main/04_latent_objective_learning)

The current human-data processing stage is located at:

[03_human_data](https://github.com/majid-khorramgah/latent-objective-humanoid/tree/main/04_latent_objective_learning/03_human_data)

The corresponding experiment and processing statistics are stored under:

[results](https://github.com/majid-khorramgah/latent-objective-humanoid/tree/main/04_latent_objective_learning/03_human_data/results)

and specifically:

[statistics](https://github.com/majid-khorramgah/latent-objective-humanoid/tree/main/04_latent_objective_learning/03_human_data/results/statistics)

---

# AMASS Dataset Processing

The project uses the **AMASS** motion-capture collection as the primary source of human motion data.

The raw AMASS files are intentionally **not stored in this GitHub repository** because the dataset is large and is distributed separately.

The processing pipeline operates on valid AMASS motion sequences and reconstructs them using the **SMPL-X** body model.

The overall transformation is:

~~~text
AMASS raw motion
       |
       v
AMASS SMPL+H 156-D pose representation
       |
       v
Explicit pose mapping
       |
       v
SMPL-X body model
       |
       v
3D human body joints
       |
       v
Processed SMPL-X motion representation
~~~

---

# Stage 03 — SMPL-X Reconstruction

Stage 03 reconstructs valid AMASS motion sequences using the available SMPL-X body models.

The reconstruction script is:

[02_smplx_reconstruction.py](https://github.com/majid-khorramgah/latent-objective-humanoid/blob/main/04_latent_objective_learning/03_human_data/scripts/02_smplx_reconstruction.py)

The source AMASS representation used by this stage is:

~~~text
AMASS SMPL+H-style pose
156 dimensions
~~~

with the following structure:

~~~text
3    global orientation
63   body pose
45   left hand pose
45   right hand pose
--------------------
156 total
~~~

The target representation is SMPL-X.

For each valid sequence, the AMASS pose parameters are mapped explicitly to SMPL-X inputs. Facial parameters such as jaw, eye poses, and expression are initialized to zero because they are not represented in the AMASS 156-D pose vector used by this pipeline.

---

# Reconstruction Output

The reconstruction produces 3D joint coordinates from the SMPL-X body model.

The primary output is:

~~~text
joints
~~~

with a typical shape of:

~~~text
(N, 127, 3)
~~~

where:

- `N` = number of motion frames
- `127` = SMPL-X joints / landmarks returned by the model
- `3` = XYZ coordinates

For example:

~~~text
360 frames
x
127 joints
x
3 coordinates
~~~

The processed files preserve the original AMASS directory hierarchy so that every reconstructed sequence can be traced back to its source sequence.

---

# Reconstruction Statistics

The reconstruction statistics are available in:

[statistics](https://github.com/majid-khorramgah/latent-objective-humanoid/tree/main/04_latent_objective_learning/03_human_data/results/statistics)

The main reconstruction report is:

[reconstruction_summary.json](https://github.com/majid-khorramgah/latent-objective-humanoid/blob/main/04_latent_objective_learning/03_human_data/results/statistics/reconstruction_summary.json)

The AMASS motion inventory is available at:

[amass_motion_files.csv](https://github.com/majid-khorramgah/latent-objective-humanoid/blob/main/04_latent_objective_learning/03_human_data/results/statistics/amass_motion_files.csv)

The dataset inventory is available at:

[amass_dataset_inventory.json](https://github.com/majid-khorramgah/latent-objective-humanoid/blob/main/04_latent_objective_learning/03_human_data/results/statistics/amass_dataset_inventory.json)

---

# Current Reconstruction Results

The current full-dataset reconstruction was executed using CUDA on an NVIDIA RTX 3090.

| Metric | Result |
|---|---:|
| Selected sequences | 13,164 |
| Successful sequences | 11,824 |
| Failed sequences | 1,340 |
| Successful frames | 15,263,074 |
| Model | SMPL-X |
| Source representation | AMASS SMPL+H 156-D |
| Output representation | 127 3D joints |
| Device | CUDA |
| Batch size | 1024 |
| Vertices saved | No |
| Runtime | ~1,345.6 seconds |
| Runtime | ~22.4 minutes |

The successful reconstruction covers the following AMASS datasets:

- ACCAD
- BMLmovi
- BMLrub
- CMU
- DanceDB
- HumanEva
- KIT
- MPI_HDM05

---

# GRAB Dataset Status

The current reconstruction pass did not reconstruct the GRAB sequences.

All 1,340 failed sequences belong to GRAB.

The current loader expects the field:

~~~text
mocap_framerate
~~~

However, the available GRAB files do not contain this field.

Therefore, GRAB sequences are currently excluded from the SMPL-X reconstruction result rather than assigning an assumed frame rate.

This is treated as a dataset-schema compatibility issue and is kept separate from the successful reconstruction of the other AMASS subsets.

---

# Repository Data Policy

Large datasets and generated motion data are intentionally excluded from GitHub.

The following are **not stored in the repository**:

~~~text
03_human_data/data/AMASS/raw/
03_human_data/data/processed/
SMPL-X model files
large generated motion files
~~~

Instead, the repository stores:

- Processing scripts
- Dataset inventories
- Reconstruction statistics
- Experiment metadata
- Documentation
- Configuration and reproducibility information

This keeps the repository lightweight while preserving the information necessary to understand and reproduce the processing pipeline.

---

# Reproducibility

The reconstruction pipeline supports:

- CPU execution
- CUDA execution
- Configurable batch size
- Deterministic sequence sampling
- Dataset filtering
- Optional vertex reconstruction
- Output validation
- Per-sequence failure reporting
- Preservation of source dataset hierarchy

A CUDA reconstruction can be run with:

~~~text
python 04_latent_objective_learning/03_human_data/scripts/02_smplx_reconstruction.py --batch-size 1024 --device cuda --overwrite
~~~

The exact command should be adjusted according to the local project structure and available GPU memory.

---

# Processing Architecture

The current human-motion processing pipeline can be summarized as:

~~~text
AMASS
 |
 |  Stage 01
 v
Dataset inventory and validation
 |
 v
Valid AMASS motion sequences
 |
 |  Stage 03
 v
AMASS SMPL+H 156-D
 |
 v
Explicit AMASS -> SMPL-X pose mapping
 |
 v
SMPL-X reconstruction
 |
 v
127 3D joints
 |
 v
Processed human-motion representation
 |
 v
Future latent-objective learning stages
~~~

The processed representation is intended to serve as an intermediate structured representation for subsequent human-motion learning and latent-objective modeling.

---

# Results and Experiment Records

The committed statistics provide a reproducible record of the current processing state without distributing the underlying datasets.

Current experiment records:

- [AMASS dataset inventory](https://github.com/majid-khorramgah/latent-objective-humanoid/blob/main/04_latent_objective_learning/03_human_data/results/statistics/amass_dataset_inventory.json)
- [AMASS motion inventory](https://github.com/majid-khorramgah/latent-objective-humanoid/blob/main/04_latent_objective_learning/03_human_data/results/statistics/amass_motion_files.csv)
- [SMPL-X reconstruction summary](https://github.com/majid-khorramgah/latent-objective-humanoid/blob/main/04_latent_objective_learning/03_human_data/results/statistics/reconstruction_summary.json)

---

# Next Steps

The next stages of the pipeline will build on the reconstructed SMPL-X human-motion representation.

Planned directions include:

1. Validation of the reconstructed joint representation.
2. Verification of left/right hand pose semantics.
3. Resolution of the GRAB dataset schema mismatch.
4. Standardization of motion representations.
5. Temporal preprocessing and normalization.
6. Human-motion feature extraction.
7. Latent representation learning.
8. Latent-objective learning for downstream humanoid motion modeling.

---

# Project Status

**Human-motion reconstruction: completed for the currently compatible AMASS subsets.**

~~~text
11,824 sequences
15,263,074 reconstructed frames
SMPL-X
127 3D joints
CUDA / RTX 3090
~~~

The generated processed motion data remains local and is intentionally excluded from this repository.
