# Human Motion Dataset Preparation


## Overview

This directory contains the human motion datasets required for the AMASS-based human motion representation pipeline.

Due to the large size of motion capture datasets, raw data files are **not included in this repository**.

Users should download the required datasets from their official sources and place them according to the structure described below.


---

# Dataset Source


The pipeline is built on the **AMASS (Archive of Motion Capture as Surface Shapes)** dataset.

AMASS is a large-scale human motion database that unifies multiple motion capture datasets into a common SMPL/SMPL-X representation.

Official project:

https://amass.is.tue.mpg.de/


The AMASS dataset requires user registration and acceptance of individual dataset licenses before downloading.



---

# Required Registration


Before downloading AMASS data:


1. Visit:

```
https://amass.is.tue.mpg.de/
```


2. Create an account.

3. Accept the dataset terms and licenses.

4. Download the required motion capture datasets.



---

# Included Motion Datasets


The current pipeline supports the following AMASS subsets:


```
AMASS/

├── ACCAD

├── BMLmovi

├── BMLrub

├── CMU

├── DanceDB

├── GRAB

├── HumanEva

├── KIT

└── MPI_HDM05
```


These datasets provide diverse human motions including:

- Walking
- Running
- Human interaction
- Object manipulation
- Daily activities
- Whole-body movements



---

# Download Strategy


Because AMASS contains multiple large datasets, downloading everything is optional.

For initial experiments, the recommended order is:


## Stage 1: Core Motion Datasets


Recommended first:


```
CMU

KIT

ACCAD

MPI_HDM05
```


These provide a broad range of human movements and are suitable for motion representation learning.


---

## Stage 2: Extended Motion Diversity


For larger-scale experiments:


```
BMLrub

BMLmovi

HumanEva

DanceDB

GRAB
```


These datasets increase motion diversity and improve generalization.



---

# Directory Structure


After downloading, organize the data as:


```
03_human_motion/

│
├── data/

│
│   └── AMASS/

│
│       └── raw/

│
│           ├── ACCAD/

│           ├── BMLmovi/

│           ├── BMLrub/

│           ├── CMU/

│           ├── DanceDB/

│           ├── GRAB/

│           ├── HumanEva/

│           ├── KIT/

│           └── MPI_HDM05/

│
└── README.md
```


---

# Expected AMASS File Format


Each motion sequence contains an `.npz` file.


Example:


```
CMU/

└── 31/

    └── 31_01_poses.npz
```


The file contains:


```
poses

betas

trans

dmpls

mocap_framerate

gender
```


Example:


```
poses:

(number_of_frames,156)


betas:

(16,)
```



---

# Dataset Processing Pipeline


After downloading the datasets, the processing pipeline automatically converts the raw motion files:


```
Raw AMASS Motion

        ↓

SMPL-X Forward Reconstruction

        ↓

3D Human Joints

        ↓

Motion Features

        ↓

Motion Encoder Training
```



---

# Running the Processing Pipeline


After placing datasets inside:


```
data/AMASS/raw/
```


Run:


```
python scripts/process_all_amass.py
```


The script automatically:


- Finds available datasets
- Loads AMASS motion files
- Applies SMPL-X reconstruction
- Extracts 3D joints
- Generates motion features



---

# Storage Requirements


Approximate storage requirements:


| Component | Storage |
|---|---:|
| Raw AMASS datasets | Hundreds of GB |
| SMPL-X models | ~400 MB |
| Processed features | Depends on dataset size |
| Full reconstructed meshes | Very large |



For this reason:

- Raw datasets are not uploaded to GitHub
- Large generated files should use external storage
- Only sample outputs and documentation are included



---

# License and Usage


Each AMASS component dataset has its own license agreement.

Users must:

- Download datasets individually
- Accept original dataset licenses
- Follow usage restrictions


Please refer to the official AMASS website for complete licensing information.


---

# Research Purpose


The prepared datasets are used for:

- Human motion understanding
- Motion representation learning
- Humanoid intelligence research
- Latent objective discovery
- Future humanoid robot learning


The goal is to transform large-scale human demonstrations into structured representations that can support generalizable humanoid intelligence.
