# Latent Objective Humanoid

**Repository:** [latent-objective-humanoid](../../../..)

This project investigates a latent-objective framework for human motion processing and learning, with a focus on transforming motion-capture data into structured representations suitable for downstream latent-space learning and humanoid motion modeling.

---

## Human Motion Data Pipeline

The human-motion processing pipeline is organized under:

[04_latent_objective_learning](../../..)

The current human-data processing stage is located at:

[03_human_data](../..)

The corresponding experiment and processing statistics are stored under:

[results](..)

and specifically:

[statistics](.)

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

[02_smplx_reconstruction.py](../../scripts/02_smplx_reconstruction.py)

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
- `127` = canonical SMPL-X joint/keypoint output used by this project
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

The complete structure of the 127-joint representation is documented in:

[smplx_joint_structure.json](./smplx_joint_structure.json)

This JSON file is the project-level reference for the reconstructed SMPL-X joint structure, including the joint categories, indices, names, parent relationships, and extraction-related metadata.

---

# SMPL-X 127-Joint Canonical Representation

The project treats the complete SMPL-X output as the **canonical reconstructed human-motion representation**.

The important distinction is that several different joint counts exist inside the SMPL-X implementation.

The project therefore does not use `NUM_JOINTS` alone to define the final output.

The canonical output is verified at runtime as:

~~~text
joints.shape = (N, 127, 3)
~~~

The 127 output elements are composed of:

~~~text
55 LBS / kinematic joints
+
21 extra vertex-based keypoints
+
51 facial landmarks
--------------------------------
127 total output joints/keypoints
~~~

Therefore:

~~~text
55 + 21 + 51 = 127
~~~

The three components are:

| Component | Count | Description |
|---|---:|---|
| LBS / kinematic joints | 55 | Body, hands, jaw, and eyes represented by the SMPL-X kinematic structure |
| Extra vertex-based keypoints | 21 | Face keypoints, foot keypoints, and hand fingertips |
| Facial landmarks | 51 | Detailed facial geometry landmarks |
| **Total** | **127** | **Canonical SMPL-X output** |

The complete index-level specification is maintained separately in:

[smplx_joint_structure.json](./smplx_joint_structure.json)

---

# Why the Canonical Representation Is 127

The SMPL-X implementation exposes a model-level joint count that should not be confused with the final tensor returned by the forward pass.

For this project, the reconstruction pipeline explicitly verifies the final representation rather than inferring it from a single model constant.

The effective construction is:

~~~text
SMPL-X parameters
      |
      v
Linear Blend Skinning
      |
      +--> 55 LBS / kinematic joints
      |
      v
Extra vertex-based keypoint selection
      |
      +--> 21 additional keypoints
      |
      v
Facial landmark extraction
      |
      +--> 51 facial landmarks
      |
      v
Canonical output
      |
      v
(N, 127, 3)
~~~

This distinction is important for reproducibility because:

~~~text
SMPL-X model joint constant
        !=
final project output joint count
~~~

The final output used by the project is:

~~~text
127 joints/keypoints
