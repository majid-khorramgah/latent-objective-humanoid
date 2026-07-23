# External Dependencies


## Overview

This directory contains external resources required for the human motion processing pipeline.

The main external dependency is the **SMPL-X parametric human body model**, which is used to reconstruct 3D human body geometry and joint structures from AMASS motion capture data.


Due to licensing restrictions and large file sizes, external models and repositories are not included directly in this GitHub repository.

Users should download them from their official sources and place them according to the structure described below.



---

# SMPL-X Human Body Model


## Official Resources


SMPL-X Official Project:

https://smpl-x.is.tue.mpg.de/


SMPL-X GitHub Repository:

https://github.com/vchoutas/smplx



The SMPL-X model provides:

- Full human body representation
- Body pose modeling
- Hand articulation
- Facial expression modeling
- 3D joint regression



---

# Required Registration


SMPL-X requires registration before downloading.


Steps:


1. Visit:

```
https://smpl-x.is.tue.mpg.de/
```


2. Create an account.

3. Accept the license agreement.

4. Download the SMPL-X model files.



---

# Required Files


After downloading SMPL-X models, the structure should be:


```
external/

└── smplx/

    │

    ├── models/

    │   ├── SMPLX_NEUTRAL.npz

    │   ├── SMPLX_MALE.npz

    │   ├── SMPLX_FEMALE.npz

    │   └── md5sum.txt

    │

    └── smplx_repository/

        ├── smplx/

        ├── examples/

        ├── tools/

        ├── setup.py

        └── requirements.txt
```


---

# Installation


Create the research environment:


```
conda create -n human_motion python=3.10

conda activate human_motion
```


Install required packages:


```
pip install torch numpy scipy matplotlib tqdm
```


Install SMPL-X:


Navigate to:


```
external/smplx/smplx_repository/
```


Run:


```
pip install -e .
```



Verify installation:


```python
import smplx

print("SMPL-X installed successfully")
```


Expected output:


```
SMPL-X installed successfully
```



---

# Usage in This Project


The SMPL-X model is used in:


```
scripts/

└── 03_smpl_forward.py

└── 04_export_motion.py

└── process_all_amass.py
```


The pipeline:


```
AMASS Pose Parameters

        ↓

SMPL-X Forward Model

        ↓

3D Human Mesh

        ↓

3D Joint Representation

        ↓

Motion Features
```



---

# Model Output


SMPL-X reconstruction generates:


## Vertices


Full human body surface:


```
10475 vertices
```


## Joints


Human kinematic structure:


```
127 joints
```



These outputs are used for:

- Human motion representation
- Motion feature extraction
- Future motion encoder training



---

# Why External Files Are Not Included


The following files are intentionally excluded from GitHub:


```
*.npz

SMPL-X model files

Large pretrained assets
```


Reasons:

- License restrictions
- Large storage requirements
- Reproducibility through official download sources



---

# Directory Purpose


The external directory provides:


```
external/

│

├── smplx/

│   ├── models/

│   │   Human body model files

│   │

│   └── smplx_repository/

│       Official SMPL-X implementation
```


These resources allow the project to convert human motion capture data into physically meaningful 3D human representations.



---

# Research Role


SMPL-X is the bridge between:


```
Human Motion Capture

        ↓

Physical Human Representation

        ↓

Motion Representation Learning

        ↓

Humanoid Intelligence
```


It provides the human body prior required for future research stages:

- Motion Encoder
- Latent Objective Discovery
- Humanoid Robot Learning



---

# References


SMPL-X Paper:

https://smpl-x.is.tue.mpg.de/


SMPL-X Implementation:

https://github.com/vchoutas/smplx


AMASS Dataset:

https://amass.is.tue.mpg.de/
