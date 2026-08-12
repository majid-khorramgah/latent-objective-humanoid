## Video Demonstrations

The following videos demonstrate the main stages of the AMASS-based human motion representation pipeline.

These experiments validate the complete process from raw human motion capture data to structured human motion representations using SMPL-X.

The developed pipeline provides the foundation for future research on:

- Human Motion Representation Learning
- Physics-aware Motion Understanding
- Latent Human Objective Discovery
- Humanoid Robot Learning


---

## 1. Complete AMASS Human Motion Representation Pipeline

🎥 Video:
https://youtu.be/7GXgjzQQz9M


This video presents the complete human motion processing pipeline developed in this milestone.

The pipeline transforms large-scale motion capture data from the AMASS dataset into structured representations suitable for humanoid intelligence research.

Pipeline:

AMASS Motion Capture Dataset

↓

SMPL-X Human Body Reconstruction

↓

3D Joint Extraction

↓

Motion Feature Generation


The generated representations include:

- 3D joint positions
- Temporal motion information
- Velocity
- Acceleration
- Motion energy


This milestone establishes the data foundation required for future Motion Encoder development and latent objective discovery.


---

## 2. Human Motion Skeleton Visualization using SMPL-X Joints

🎥 Video:
https://youtu.be/xa4SqUcY-bc


This video demonstrates the joint-based representation extracted from reconstructed human motion.

The SMPL-X body model converts AMASS pose parameters into a structured 3D skeletal representation.

The visualization shows:

- Human joint locations
- Temporal joint movement
- Human kinematic structure


This representation will be used as the input for future motion representation learning models.


---

## 3. SMPL-X Human Motion Reconstruction from AMASS Dataset

🎥 Video:
https://youtu.be/qbFpotjyROE


This video demonstrates the reconstruction of human motion using the SMPL-X parametric human body model.

The experiment validates the conversion from AMASS motion capture parameters into physically meaningful 3D human body motion.


Pipeline:

AMASS Pose Parameters

↓

SMPL-X Forward Model

↓

3D Human Mesh Reconstruction


This reconstruction serves as the first validation stage before learning compact motion representations for humanoid intelligence.
