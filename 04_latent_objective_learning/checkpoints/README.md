# Pretrained Checkpoint

This folder contains the pretrained weights of the **Multi-Branch Motion Foundation Encoder**.

Due to GitHub file size limitations, the checkpoint file is hosted externally.

---

## Foundation Encoder Model

**File name:**

```
foundation_encoder_best.pt
```

**Size:**

Approximately 885 MB

---

## Description

This checkpoint contains the trained parameters of the Multi-Branch Motion Foundation Encoder developed for physics-aware human motion representation learning.

The model is trained on human motion data and learns structured latent representations through multiple branches:

- Pose Encoder
- Dynamics Encoder
- Physics-aware Encoder
- Temporal Representation Branch
- Physics Representation Branch
- Fusion Latent Representation
- Motion Reconstruction Decoder

The learned representations are designed for:

- Human motion understanding
- Physics-aware representation learning
- Latent space analysis
- Future human objective discovery
- Objective-conditioned motion generation

---

## Download

The pretrained checkpoint is available here:

https://drive.google.com/file/d/1OjGrO3gz8_FU-gHyvcMj4U3HRHqlbJUy/view?usp=sharing

---

## Installation

After downloading the checkpoint, place the file in this directory:

```
04_latent_objective_learning/
│
└── checkpoints/
    │
    └── foundation_encoder_best.pt
```

---

## Loading the Model

Example:

```python
checkpoint = torch.load(
    "checkpoints/foundation_encoder_best.pt",
    map_location="cuda"
)

model.load_state_dict(
    checkpoint["model"]
)
```

---

## Training Information

Dataset:

- AMASS Human Motion Dataset

Training samples:

```
97,022 motion samples
```

Motion chunks:

```
190 chunks
```

Model:

```
Multi-Branch Motion Foundation Encoder
```

Number of parameters:

```
226.6 Million
```

---

## Learned Latent Representations

The encoder produces three main latent spaces:

### Temporal Latent

Shape:

```
[97022, 32, 1024]
```

Captures:

- Motion dynamics
- Temporal patterns
- Sequential dependencies


### Physics Latent

Shape:

```
[97022, 8, 256]
```

Captures:

- Physical constraints
- Motion efficiency
- Energy-related information


### Fusion Latent

Shape:

```
[97022, 512]
```

Captures:

- Combined motion representation
- High-level motion features

---

## Research Pipeline

This checkpoint corresponds to the foundation representation learning stage:

```
Human Motion Dataset
        |
        v
Physics-aware Feature Extraction
        |
        v
Multi-Branch Foundation Encoder
        |
        v
Latent Representation Learning
        |
        v
Latent Objective Discovery
        |
        v
Objective-conditioned Motion Generation
```

---

## Note

The checkpoint is provided for research reproducibility.

The AMASS dataset is not included in this repository and should be obtained separately according to its official license.
