# SMPL-X Joint Structure and Extraction Specification

**Project:** `latent-objective-humanoid`  
**Stage:** `03_human_motion`  
**Document:** SMPL-X 127-Joint Canonical Representation and Joint Extraction Policy  
**Status:** Reference / Implementation Specification  
**Last Updated:** 2026-08-15

---

# 0. Project References

## Video / Research Reference

[YouTube Video – SMPL-X / Human Motion Processing](https://youtu.be/Pw4jINaFT_M)

## Stage 3

**Stage 3 — Human Motion / Joint Extraction**

Project location:

```text
03_human_motion/
```

The purpose of this stage is to take the canonical SMPL-X reconstruction and generate deterministic downstream representations such as:

```text
SMPL-X 127
    |
    +--> Core Body
    +--> Hands
    +--> Feet
    +--> Face
    |
    v
Normalization
    |
    v
Feature Extraction
    |
    v
Contact Detection
    |
    v
Motion Segmentation
    |
    v
Dataset Creation
    |
    v
Latent Objective Learning
```

The canonical 127-joint representation must be preserved so that downstream representations can be changed later without repeating the expensive SMPL-X reconstruction.

---

# 1. Final Architectural Decision

The project uses the following architecture:

```text
                         AMASS
                           |
                           v
                  SMPL-X Reconstruction
                           |
                           v
                    SMPL-X 127 joints
                           |
             +-------------+-------------+
             |             |             |
             v             v             v
          Core Body      Hands         Face
             |
             v
       Main Body Skeleton
             |
             v
       Normalization
             |
             v
       Feature Extraction
             |
             v
       Contact Detection
             |
             v
       Motion Segmentation
             |
             v
       Dataset Creation
             |
             v
       Latent Objective Learning
```

The important design principle is:

```text
127 joints = canonical representation

Core / Hands / Feet / Face
    = derived representations
```

We do NOT permanently reduce:

```text
127 -> 24
```

during reconstruction.

Instead:

```text
127 -> Core
127 -> Hands
127 -> Feet
127 -> Face
127 -> Custom representation
```

can all be generated later.

---

# 2. Why the Canonical 127 Representation Is Preserved

The reconstruction stage contains more information than the main body-motion model may currently need.

For example:

```text
finger joints
finger tips
toe points
heel points
jaw
eyes
nose
ears
facial landmarks
```

may not be required for the first version of the latent objective.

However, deleting them permanently would prevent future experiments.

Therefore:

```text
KEEP EVERYTHING AT RECONSTRUCTION TIME
```

and perform reduction only when creating a specific downstream representation.

This gives us:

```text
One expensive reconstruction
        |
        +--> many possible representations
```

instead of:

```text
One reconstruction
        |
        +--> information permanently lost
```

---

# 3. SMPL-X Model Configuration

The SMPL-X model used by this project is located at:

```text
03_human_motion/external/smplx/models
```

The Python repository is located at:

```text
03_human_motion/external/smplx/smplx_repository
```

The model is loaded using:

```python
import smplx

model_path = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models"

model = smplx.create(
    model_path,
    model_type="smplx",
    gender="neutral",
    num_betas=16,
    use_pca=False,
    ext="npz",
)
```

The actual neutral model file is:

```text
03_human_motion/external/smplx/models/smplx/SMPLX_NEUTRAL.npz
```

---

# 4. Important Discovery: 54 vs 55 vs 127

One of the most important findings is that the following numbers are different:

```text
NUM_JOINTS = 54

J_regressor = 55 × 10475

Final output = 127 × 3
```

These numbers must NOT be treated as equivalent.

The following command was executed:

```python
import smplx

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models"

m = smplx.create(
    p,
    model_type="smplx",
    gender="neutral",
    num_betas=16,
    use_pca=False,
    ext="npz",
)

o = m()

print("NUM_JOINTS:", m.NUM_JOINTS)
print("J_regressor:", m.J_regressor.shape)
print("output:", o.joints.shape)
```

Observed:

```text
NUM_JOINTS: 54
J_regressor: torch.Size([55, 10475])
output: torch.Size([1, 127, 3])
```

The apparent discrepancy is caused by the way SMPL-X constructs the final output.

---

# 5. Construction of the 127 Output Joints

The SMPL-X forward pass was inspected in:

```text
03_human_motion/external/smplx/smplx_repository/smplx/body_models.py
```

The relevant implementation is:

```python
vertices, joints = lbs(
    shape_components,
    full_pose,
    self.v_template,
    shapedirs,
    self.posedirs,
    self.J_regressor,
    self.parents,
    self.lbs_weights,
    pose2rot=pose2rot,
)

joints = self.vertex_joint_selector(vertices, joints)

joints = torch.cat([joints, landmarks], dim=1)

if self.joint_mapper is not None:
    joints = self.joint_mapper(
        joints=joints,
        vertices=vertices
    )
```

Therefore the final output is constructed as:

```text
LBS joints
    +
Extra vertex joints
    +
Facial landmarks
    =
Final joints
```

Specifically:

```text
55 LBS joints
+
21 extra vertex joints
+
51 facial landmarks
=
127 joints
```

Therefore:

```text
55 + 21 + 51 = 127
```

---

# 6. Stage A — LBS Joints

The model contains:

```text
J_regressor.shape = (55, 10475)
```

Therefore the LBS stage produces:

```text
55 joints
```

These form the SMPL-X kinematic skeleton.

Their hierarchy is defined by:

```text
kintree_table
parents
```

and their names are defined by:

```text
joint2num
```

in the model file.

---

# 7. Stage B — Extra Vertex-Based Joints

The `VertexJointSelector` adds:

```text
21 extra joints
```

These are not regressed kinematic joints.

They are selected directly from mesh vertices.

They consist of:

```text
5 face keypoints
6 foot keypoints
10 hand fingertip keypoints
```

Therefore:

```text
55 + 21 = 76
```

---

# 8. Stage C — Facial Landmarks

The model contains:

```text
51 facial landmarks
```

They are generated using:

```python
landmarks = vertices2landmarks(
    vertices,
    self.faces_tensor,
    lmk_faces_idx,
    lmk_bary_coords,
)
```

The landmarks are then appended:

```python
joints = torch.cat([joints, landmarks], dim=1)
```

Therefore:

```text
76 + 51 = 127
```

---

# 9. Final Output Structure

The final SMPL-X output is:

```text
[batch_size, 127, 3]
```

For a batch size of one:

```text
[1, 127, 3]
```

The output consists of:

```text
0 ... 54
    55 LBS / kinematic joints

55 ... 75
    21 extra vertex-based keypoints

76 ... 126
    51 facial landmarks
```

---

# 10. Model File Inspection

The model file was inspected with:

```python
import numpy as np

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

d = np.load(p, allow_pickle=True)

print(d.files)
```

The observed keys were:

```text
[
    'bs_type',
    'bs_style',
    'J_regressor_prior',
    'f',
    'J_regressor',
    'kintree_table',
    'J',
    'weights_prior',
    'weights',
    'vert_sym_idxs',
    'posedirs',
    'v_template',
    'shapedirs',
    'hands_meanr',
    'hands_meanl',
    'lmk_bary_coords',
    'vt',
    'part2num',
    'hands_coeffsr',
    'lmk_faces_idx',
    'dynamic_lmk_faces_idx',
    'hands_componentsr',
    'dynamic_lmk_bary_coords',
    'ft',
    'hands_componentsl',
    'joint2num',
    'allow_pickle',
    'hands_coeffsl'
]
```

---

# 11. Model Shape Verification

The following command was used:

```python
import numpy as np

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

d = np.load(p, allow_pickle=True)

print("J_regressor shape:", d["J_regressor"].shape)
print("J shape:", d["J"].shape)
print("lmk_faces_idx shape:", d["lmk_faces_idx"].shape)
print("dynamic_lmk_faces_idx shape:", d["dynamic_lmk_faces_idx"].shape)
```

Observed:

```text
J_regressor shape: (55, 10475)
J shape: (55, 3)
lmk_faces_idx shape: (51,)
dynamic_lmk_faces_idx shape: (79, 17)
```

---

# 12. Kinematic Joint Mapping

The model contains:

```text
joint2num
```

which maps names to numerical indices.

The complete mapping is:

```text
Pelvis       = 0

L_Hip        = 1
R_Hip        = 2

Spine1       = 3

L_Knee       = 4
R_Knee       = 5

Spine2       = 6

L_Ankle      = 7
R_Ankle      = 8

Spine3       = 9

L_Foot       = 10
R_Foot       = 11

Neck         = 12

L_Collar     = 13
R_Collar     = 14

Head         = 15

L_Shoulder   = 16
R_Shoulder   = 17

L_Elbow      = 18
R_Elbow      = 19

L_Wrist      = 20
R_Wrist      = 21

Jaw          = 22

L_Eye        = 23
R_Eye        = 24

L_Index1     = 25
L_Index2     = 26
L_Index3     = 27

L_Middle1    = 28
L_Middle2    = 29
L_Middle3    = 30

L_Pinky1     = 31
L_Pinky2     = 32
L_Pinky3     = 33

L_Ring1      = 34
L_Ring2      = 35
L_Ring3      = 36

L_Thumb1     = 37
L_Thumb2     = 38
L_Thumb3     = 39

R_Index1     = 40
R_Index2     = 41
R_Index3     = 42

R_Middle1    = 43
R_Middle2    = 44
R_Middle3    = 45

R_Pinky1     = 46
R_Pinky2     = 47
R_Pinky3     = 48

R_Ring1      = 49
R_Ring2      = 50
R_Ring3      = 51

R_Thumb1     = 52
R_Thumb2     = 53
R_Thumb3     = 54
```

---

# 13. Complete Kinematic Parent Array

The model reports:

```text
parents.shape = (55,)
```

The exact parent array is:

```text
[
    -1,
     0,
     0,
     0,
     1,
     2,
     3,
     4,
     5,
     6,
     7,
     8,
     9,
     9,
     9,
    12,
    13,
    14,
    16,
    17,
    18,
    19,
    15,
    15,
    15,
    20,
    25,
    26,
    20,
    28,
    29,
    20,
    31,
    32,
    20,
    34,
    35,
    20,
    37,
    38,
    21,
    40,
    41,
    21,
    43,
    44,
    21,
    46,
    47,
    21,
    49,
    50,
    21,
    52,
    53
]
```

---

# 14. Complete Kinematic Skeleton Table

| Index | Name | Parent Index | Parent Name | Category |
|---:|---|---:|---|---|
| 0 | Pelvis | -1 | Root | Core |
| 1 | L_Hip | 0 | Pelvis | Core |
| 2 | R_Hip | 0 | Pelvis | Core |
| 3 | Spine1 | 0 | Pelvis | Core |
| 4 | L_Knee | 1 | L_Hip | Core |
| 5 | R_Knee | 2 | R_Hip | Core |
| 6 | Spine2 | 3 | Spine1 | Core |
| 7 | L_Ankle | 4 | L_Knee | Core |
| 8 | R_Ankle | 5 | R_Knee | Core |
| 9 | Spine3 | 6 | Spine2 | Core |
| 10 | L_Foot | 7 | L_Ankle | Core |
| 11 | R_Foot | 8 | R_Ankle | Core |
| 12 | Neck | 9 | Spine3 | Core |
| 13 | L_Collar | 9 | Spine3 | Upper Body |
| 14 | R_Collar | 9 | Spine3 | Upper Body |
| 15 | Head | 12 | Neck | Core |
| 16 | L_Shoulder | 13 | L_Collar | Core |
| 17 | R_Shoulder | 14 | R_Collar | Core |
| 18 | L_Elbow | 16 | L_Shoulder | Core |
| 19 | R_Elbow | 17 | R_Shoulder | Core |
| 20 | L_Wrist | 18 | L_Elbow | Core |
| 21 | R_Wrist | 19 | R_Elbow | Core |
| 22 | Jaw | 15 | Head | Face |
| 23 | L_Eye | 15 | Head | Face |
| 24 | R_Eye | 15 | Head | Face |
| 25 | L_Index1 | 20 | L_Wrist | Hand |
| 26 | L_Index2 | 25 | L_Index1 | Hand |
| 27 | L_Index3 | 26 | L_Index2 | Hand |
| 28 | L_Middle1 | 20 | L_Wrist | Hand |
| 29 | L_Middle2 | 28 | L_Middle1 | Hand |
| 30 | L_Middle3 | 29 | L_Middle2 | Hand |
| 31 | L_Pinky1 | 20 | L_Wrist | Hand |
| 32 | L_Pinky2 | 31 | L_Pinky1 | Hand |
| 33 | L_Pinky3 | 32 | L_Pinky2 | Hand |
| 34 | L_Ring1 | 20 | L_Wrist | Hand |
| 35 | L_Ring2 | 34 | L_Ring1 | Hand |
| 36 | L_Ring3 | 35 | L_Ring2 | Hand |
| 37 | L_Thumb1 | 20 | L_Wrist | Hand |
| 38 | L_Thumb2 | 37 | L_Thumb1 | Hand |
| 39 | L_Thumb3 | 38 | L_Thumb2 | Hand |
| 40 | R_Index1 | 21 | R_Wrist | Hand |
| 41 | R_Index2 | 40 | R_Index1 | Hand |
| 42 | R_Index3 | 41 | R_Index2 | Hand |
| 43 | R_Middle1 | 21 | R_Wrist | Hand |
| 44 | R_Middle2 | 43 | R_Middle1 | Hand |
| 45 | R_Middle3 | 44 | R_Middle2 | Hand |
| 46 | R_Pinky1 | 21 | R_Wrist | Hand |
| 47 | R_Pinky2 | 46 | R_Pinky1 | Hand |
| 48 | R_Pinky3 | 47 | R_Pinky2 | Hand |
| 49 | R_Ring1 | 21 | R_Wrist | Hand |
| 50 | R_Ring2 | 49 | R_Ring1 | Hand |
| 51 | R_Ring3 | 50 | R_Ring2 | Hand |
| 52 | R_Thumb1 | 21 | R_Wrist | Hand |
| 53 | R_Thumb2 | 52 | R_Thumb1 | Hand |
| 54 | R_Thumb3 | 53 | R_Thumb2 | Hand |

---

# 15. `kintree_table`

The model reports:

```text
kintree_table.shape = (2, 55)
```

The observed table is:

```text
[
    [
        4294967295,
        0,
        0,
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        9,
        9,
        12,
        13,
        14,
        16,
        17,
        18,
        19,
        15,
        15,
        15,
        20,
        25,
        26,
        20,
        28,
        29,
        20,
        31,
        32,
        20,
        34,
        35,
        20,
        37,
        38,
        21,
        40,
        41,
        21,
        43,
        44,
        21,
        46,
        47,
        21,
        49,
        50,
        21,
        52,
        53
    ],
    [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        44,
        45,
        46,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54
    ]
]
```

The first root value:

```text
4294967295
```

is the unsigned representation of:

```text
-1
```

Therefore the root joint is:

```text
Pelvis
```

---

# 16. Extra Vertex-Based Joints

The loaded model reports:

```python
m.vertex_joint_selector.extra_joints_idxs.tolist()
```

as:

```text
[
    9120,
    9929,
    9448,
    616,
    6,
    5770,
    5780,
    8846,
    8463,
    8474,
    8635,
    5361,
    4933,
    5058,
    5169,
    5286,
    8079,
    7669,
    7794,
    7905,
    8022
]
```

There are:

```text
21
```

extra joints.

---

# 17. Complete Extra Joint Table

These joints are appended after the 55 LBS joints.

Therefore their output indices are:

```text
55 ... 75
```

| Output Index | Name | Source | Vertex Index | Category |
|---:|---|---|---:|---|
| 55 | Nose | Vertex | 9120 | Face |
| 56 | R_Eye_Keypoint | Vertex | 9929 | Face |
| 57 | L_Eye_Keypoint | Vertex | 9448 | Face |
| 58 | R_Ear | Vertex | 616 | Face |
| 59 | L_Ear | Vertex | 6 | Face |
| 60 | L_BigToe | Vertex | 5770 | Feet |
| 61 | L_SmallToe | Vertex | 5780 | Feet |
| 62 | L_Heel | Vertex | 8846 | Feet |
| 63 | R_BigToe | Vertex | 8463 | Feet |
| 64 | R_SmallToe | Vertex | 8474 | Feet |
| 65 | R_Heel | Vertex | 8635 | Feet |
| 66 | L_Thumb_Tip | Vertex | 5361 | Hands |
| 67 | L_Index_Tip | Vertex | 4933 | Hands |
| 68 | L_Middle_Tip | Vertex | 5058 | Hands |
| 69 | L_Ring_Tip | Vertex | 5169 | Hands |
| 70 | L_Pinky_Tip | Vertex | 5286 | Hands |
| 71 | R_Thumb_Tip | Vertex | 8079 | Hands |
| 72 | R_Index_Tip | Vertex | 7669 | Hands |
| 73 | R_Middle_Tip | Vertex | 7794 | Hands |
| 74 | R_Ring_Tip | Vertex | 7905 | Hands |
| 75 | R_Pinky_Tip | Vertex | 8022 | Hands |

---

# 18. Facial Landmarks

The model reports:

```text
lmk_faces_idx.shape = (51,)
```

Therefore there are:

```text
51 static facial landmarks
```

These are appended after the 76 joints/keypoints created by the first two stages.

Therefore:

```text
76 ... 126
```

are facial landmarks.

The landmarks are generated using:

```python
landmarks = vertices2landmarks(
    vertices,
    self.faces_tensor,
    lmk_faces_idx,
    lmk_bary_coords
)
```

---

# 19. Facial Landmark Output Indices

The relevant facial landmark sequence is:

```text
76  right_eye_brow1
77  right_eye_brow2
78  right_eye_brow3
79  right_eye_brow4
80  right_eye_brow5

81  left_eye_brow5
82  left_eye_brow4
83  left_eye_brow3
84  left_eye_brow2
85  left_eye_brow1

86  nose1
87  nose2
88  nose3
89  nose4

90  right_nose_2
91  right_nose_1
92  nose_middle
93  left_nose_1
94  left_nose_2

95  right_eye1
96  right_eye2
97  right_eye3
98  right_eye4
99  right_eye5
100 right_eye6

101 left_eye4
102 left_eye3
103 left_eye2
104 left_eye1
105 left_eye6
106 left_eye5

107 right_mouth_1
108 right_mouth_2
109 right_mouth_3
110 mouth_top
111 left_mouth_3
112 left_mouth_2
113 left_mouth_1

114 left_mouth_5
115 left_mouth_4
116 mouth_bottom

117 right_mouth_4
118 right_mouth_5

119 right_lip_1
120 right_lip_2
121 lip_top
122 left_lip_2
123 left_lip_1
124 left_lip_3
125 lip_bottom
126 right_lip_3
```

These are facial geometry landmarks.

They are NOT part of the main body kinematic skeleton.

---

# 20. Complete 127-Joint Layout

```text
0 ... 54
    Kinematic / LBS skeleton
    Body + hands + jaw + eyes

55 ... 59
    Face vertex keypoints
    Nose + eyes + ears

60 ... 65
    Feet keypoints
    Big toes + small toes + heels

66 ... 75
    Hand fingertip keypoints

76 ... 126
    Facial landmarks
```

Total:

```text
55 + 5 + 6 + 10 + 51 = 127
```

---

# 21. Recommended Representation Separation

The project should use the following conceptual groups:

```text
                    SMPL-X 127
                         |
        +----------------+----------------+
        |                |                |
        v                v                v
      BODY             HANDS            FACE
        |                |                |
        |                |                +--> Jaw
        |                |                +--> Eyes
        |                |                +--> Nose
        |                |                +--> Ears
        |                |                +--> Landmarks
        |                |
        |                +--> Finger joints
        |                +--> Fingertips
        |
        +--> Pelvis
        +--> Hips
        +--> Knees
        +--> Ankles
        +--> Feet
        +--> Spine
        +--> Neck
        +--> Head
        +--> Shoulders
        +--> Elbows
        +--> Wrists
        |
        +--> Feet keypoints
```

---

# 22. Important Correction to the Previous 24-Joint Idea

The earlier idea of simply taking the first 24 joints is NOT the final project decision.

In particular:

```text
indices 22 and 23
```

are:

```text
Jaw
L_Eye
```

and:

```text
index 24
```

is:

```text
R_Eye
```

Therefore a naive:

```python
joints[:, :24]
```

would introduce facial joints into the main body representation.

This is not desirable for the main motion model.

Therefore the project will NOT define the main representation as:

```text
first 24 SMPL-X joints
```

Instead, the main body representation will be an explicitly defined body-centric subset.

---

# 23. Revised Main Body Representation

The main representation should prioritize:

```text
Pelvis
Hips
Knees
Ankles
Feet
Spine
Neck
Head
Shoulders
Elbows
Wrists
```

and exclude:

```text
Jaw
Eyes
Finger joints
Facial landmarks
```

This means the body representation must be created using explicit named indices.

Example:

```python
BODY_CORE = [
    0,   # Pelvis

    1,   # L_Hip
    2,   # R_Hip

    3,   # Spine1

    4,   # L_Knee
    5,   # R_Knee

    6,   # Spine2

    7,   # L_Ankle
    8,   # R_Ankle

    9,   # Spine3

    10,  # L_Foot
    11,  # R_Foot

    12,  # Neck

    13,  # L_Collar
    14,  # R_Collar

    15,  # Head

    16,  # L_Shoulder
    17,  # R_Shoulder

    18,  # L_Elbow
    19,  # R_Elbow

    20,  # L_Wrist
    21,  # R_Wrist
]
```

This gives:

```text
22 joints
```

before adding any additional body/contact keypoints.

---

# 24. Main Body + Contact Representation

Because contact detection is important for this project, the foot keypoints should remain available.

The most useful additional points are:

```text
L_BigToe
R_BigToe
L_Heel
R_Heel
```

These are:

```text
60 = L_BigToe
62 = L_Heel

63 = R_BigToe
65 = R_Heel
```

Therefore a practical body/contact representation can be:

```text
22 anatomical body joints
+
4 foot contact keypoints
=
26 points
```

However, the project should NOT force itself to a historical "24-joint" convention merely because 24 is a common number.

The correct representation should be selected according to the actual downstream objective.

---

# 25. Recommended Final Grouping

The project therefore uses the following grouping instead of forcing everything into exactly 24 joints:

## Group 1 — Core Body

```text
22 anatomical joints
```

Indices:

```text
0
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
```

---

## Group 2 — Feet / Contact

```text
L_BigToe
L_SmallToe
L_Heel
R_BigToe
R_SmallToe
R_Heel
```

Indices:

```text
60
61
62
63
64
65
```

These are kept separate because they are especially useful for contact detection.

---

## Group 3 — Hands

Kinematic finger joints:

```text
25 ... 39
40 ... 54
```

plus fingertips:

```text
66 ... 75
```

---

## Group 4 — Face

Kinematic facial joints:

```text
22 = Jaw
23 = L_Eye
24 = R_Eye
```

Face keypoints:

```text
55 = Nose
56 = R_Eye_Keypoint
57 = L_Eye_Keypoint
58 = R_Ear
59 = L_Ear
```

Facial landmarks:

```text
76 ... 126
```

---

# 26. Why This Grouping Is Better

This structure allows the project to support different experiments.

For example:

```text
Experiment A:
Core Body only

Experiment B:
Core Body + Feet

Experiment C:
Core Body + Hands

Experiment D:
Core Body + Feet + Hands

Experiment E:
Full 127

Experiment F:
Core Body + selected Face
```

No reconstruction has to be repeated.

---

# 27. Canonical Data Flow

The complete project pipeline should therefore be interpreted as:

```text
AMASS
  |
  v
SMPL-X Reconstruction
  |
  v
Canonical SMPL-X 127
  |
  +------------------+
  |                  |
  v                  v
Save Canonical     Extraction
Representation       |
                     +--> Core Body
                     |
                     +--> Feet / Contact
                     |
                     +--> Hands
                     |
                     +--> Face
                     |
                     +--> Custom
                              |
                              v
                         Normalization
                              |
                              v
                       Feature Extraction
                              |
                              v
                       Contact Detection
                              |
                              v
                       Motion Segmentation
                              |
                              v
                         Dataset Creation
                              |
                              v
                     Latent Objective Learning
```

---

# 28. Responsibility of Stage 3

The purpose of:

```text
03_human_motion
```

and specifically the joint extraction stage is NOT to redo SMPL-X reconstruction.

The responsibilities are:

```text
1. Load canonical SMPL-X reconstruction
2. Validate the 127-joint structure
3. Use explicit joint mappings
4. Generate derived representations
5. Preserve metadata
6. Save deterministic outputs
```

The reconstruction stage should be separated from extraction.

---

# 29. Important Rule for `03_extract_joints.py`

Do NOT write:

```python
joints = joints[:, :24]
```

because:

```text
22 = Jaw
23 = L_Eye
24 = R_Eye
```

and this would mix facial joints into the main body representation.

Instead use explicit index lists.

For example:

```python
BODY_CORE = [
    0,   # Pelvis
    1,   # L_Hip
    2,   # R_Hip
    3,   # Spine1
    4,   # L_Knee
    5,   # R_Knee
    6,   # Spine2
    7,   # L_Ankle
    8,   # R_Ankle
    9,   # Spine3
    10,  # L_Foot
    11,  # R_Foot
    12,  # Neck
    13,  # L_Collar
    14,  # R_Collar
    15,  # Head
    16,  # L_Shoulder
    17,  # R_Shoulder
    18,  # L_Elbow
    19,  # R_Elbow
    20,  # L_Wrist
    21,  # R_Wrist
]
```

---

# 30. Recommended Named Index Configuration

The extraction code should use a central configuration.

Example:

```python
JOINTS = {
    "Pelvis": 0,

    "L_Hip": 1,
    "R_Hip": 2,

    "Spine1": 3,

    "L_Knee": 4,
    "R_Knee": 5,

    "Spine2": 6,

    "L_Ankle": 7,
    "R_Ankle": 8,

    "Spine3": 9,

    "L_Foot": 10,
    "R_Foot": 11,

    "Neck": 12,

    "L_Collar": 13,
    "R_Collar": 14,

    "Head": 15,

    "L_Shoulder": 16,
    "R_Shoulder": 17,

    "L_Elbow": 18,
    "R_Elbow": 19,

    "L_Wrist": 20,
    "R_Wrist": 21,

    "Jaw": 22,
    "L_Eye": 23,
    "R_Eye": 24,

    "L_Index1": 25,
    "L_Index2": 26,
    "L_Index3": 27,

    "L_Middle1": 28,
    "L_Middle2": 29,
    "L_Middle3": 30,

    "L_Pinky1": 31,
    "L_Pinky2": 32,
    "L_Pinky3": 33,

    "L_Ring1": 34,
    "L_Ring2": 35,
    "L_Ring3": 36,

    "L_Thumb1": 37,
    "L_Thumb2": 38,
    "L_Thumb3": 39,

    "R_Index1": 40,
    "R_Index2": 41,
    "R_Index3": 42,

    "R_Middle1": 43,
    "R_Middle2": 44,
    "R_Middle3": 45,

    "R_Pinky1": 46,
    "R_Pinky2": 47,
    "R_Pinky3": 48,

    "R_Ring1": 49,
    "R_Ring2": 50,
    "R_Ring3": 51,

    "R_Thumb1": 52,
    "R_Thumb2": 53,
    "R_Thumb3": 54,
}
```

---

# 31. Extra Keypoint Configuration

```python
EXTRA_JOINTS = {
    "Nose": 55,
    "R_Eye_Keypoint": 56,
    "L_Eye_Keypoint": 57,
    "R_Ear": 58,
    "L_Ear": 59,

    "L_BigToe": 60,
    "L_SmallToe": 61,
    "L_Heel": 62,

    "R_BigToe": 63,
    "R_SmallToe": 64,
    "R_Heel": 65,

    "L_Thumb_Tip": 66,
    "L_Index_Tip": 67,
    "L_Middle_Tip": 68,
    "L_Ring_Tip": 69,
    "L_Pinky_Tip": 70,

    "R_Thumb_Tip": 71,
    "R_Index_Tip": 72,
    "R_Middle_Tip": 73,
    "R_Ring_Tip": 74,
    "R_Pinky_Tip": 75,
}
```

---

# 32. Landmark Range

Facial landmarks should be represented as:

```python
FACE_LANDMARKS = list(range(76, 127))
```

This is intentionally kept as a separate representation.

---

# 33. Suggested Extraction Groups

The extraction configuration should conceptually contain:

```python
GROUPS = {
    "core_body": [
        0, 1, 2, 3,
        4, 5,
        6,
        7, 8,
        9,
        10, 11,
        12,
        13, 14,
        15,
        16, 17,
        18, 19,
        20, 21,
    ],

    "feet": [
        60, 61, 62,
        63, 64, 65,
    ],

    "hands": list(range(25, 40))
             + list(range(40, 55))
             + list(range(66, 76)),

    "face": [
        22, 23, 24,
        55, 56, 57, 58, 59,
    ] + list(range(76, 127)),
}
```

---

# 34. Core Body Representation Size

The current explicit core body definition contains:

```text
22 joints
```

This is intentional.

We do not force an arbitrary 24-joint convention.

If future experiments demonstrate that two additional points improve the representation, they can be added explicitly.

For example:

```text
Core Body
+
L_BigToe
+
R_BigToe
```

would produce:

```text
24 points
```

but that should be considered a project-specific representation rather than assuming it is the universal SMPL-X 24-joint skeleton.

---

# 35. Contact Representation

For contact detection, the most useful points are expected to be:

```text
L_Ankle
R_Ankle

L_Foot
R_Foot

L_BigToe
L_SmallToe
L_Heel

R_BigToe
R_SmallToe
R_Heel
```

Corresponding indices:

```text
7
8
10
11
60
61
62
63
64
65
```

This representation should remain available independently of the main body representation.

---

# 36. Hand Representation

The hands consist of:

```text
Left hand:

25 L_Index1
26 L_Index2
27 L_Index3

28 L_Middle1
29 L_Middle2
30 L_Middle3

31 L_Pinky1
32 L_Pinky2
33 L_Pinky3

34 L_Ring1
35 L_Ring2
36 L_Ring3

37 L_Thumb1
38 L_Thumb2
39 L_Thumb3

66 L_Thumb_Tip
67 L_Index_Tip
68 L_Middle_Tip
69 L_Ring_Tip
70 L_Pinky_Tip
```

Right hand:

```text
40 R_Index1
41 R_Index2
42 R_Index3

43 R_Middle1
44 R_Middle2
45 R_Middle3

46 R_Pinky1
47 R_Pinky2
48 R_Pinky3

49 R_Ring1
50 R_Ring2
51 R_Ring3

52 R_Thumb1
53 R_Thumb2
54 R_Thumb3

71 R_Thumb_Tip
72 R_Index_Tip
73 R_Middle_Tip
74 R_Ring_Tip
75 R_Pinky_Tip
```

---

# 37. Face Representation

The face is separated into:

```text
Kinematic face:
22 Jaw
23 L_Eye
24 R_Eye
```

Vertex face keypoints:

```text
55 Nose
56 R_Eye_Keypoint
57 L_Eye_Keypoint
58 R_Ear
59 L_Ear
```

Detailed landmarks:

```text
76 ... 126
```

This separation prevents facial information from contaminating the main body representation.

---

# 38. `joint_mapper`

The loaded model reports:

```python
print(m.joint_mapper)
```

Result:

```text
None
```

Therefore there is no additional dataset-specific joint mapping applied after the 127-joint construction.

The relevant implementation is:

```python
if self.joint_mapper is not None:
    joints = self.joint_mapper(
        joints=joints,
        vertices=vertices
    )
```

Since:

```text
joint_mapper = None
```

the final 127-joint output is not remapped afterward.

---

# 39. Face Contour

The loaded model reports:

```python
print(m.use_face_contour)
```

Result:

```text
False
```

Therefore dynamic face contour landmarks are not additionally appended to the 51 static landmarks.

The observed output therefore remains:

```text
55 + 21 + 51 = 127
```

---

# 40. Verification Script

The following command verifies the entire structure:

```python
import smplx

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models"

m = smplx.create(
    p,
    model_type="smplx",
    gender="neutral",
    num_betas=16,
    use_pca=False,
    ext="npz",
)

o = m()

print("========== SMPL-X STRUCTURE ==========")
print("NUM_JOINTS:", m.NUM_JOINTS)
print("J_regressor:", tuple(m.J_regressor.shape))
print("parents:", tuple(m.parents.shape))
print("extra joints:", len(m.vertex_joint_selector.extra_joints_idxs))
print("landmarks:", len(m.lmk_faces_idx))
print("joint_mapper:", m.joint_mapper)
print("use_face_contour:", m.use_face_contour)
print("output:", tuple(o.joints.shape))

expected = (
    m.J_regressor.shape[0]
    + len(m.vertex_joint_selector.extra_joints_idxs)
    + len(m.lmk_faces_idx)
)

print("expected output joints:", expected)
print("actual output joints:", o.joints.shape[1])
print("=======================================")
```

Expected:

```text
NUM_JOINTS: 54
J_regressor: (55, 10475)
parents: (55,)
extra joints: 21
landmarks: 51
joint_mapper: None
use_face_contour: False
output: (1, 127, 3)
expected output joints: 127
actual output joints: 127
```

---

# 41. Command to Inspect the Model Mapping

```python
import numpy as np

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

d = np.load(p, allow_pickle=True)

joint2num = d["joint2num"].item()

print("joint2num:")
for name, index in sorted(joint2num.items(), key=lambda x: x[1]):
    print(f"{index:3d}  {name}")

print()
print("kintree_table shape:", d["kintree_table"].shape)
print("kintree_table:")
print(d["kintree_table"])
```

---

# 42. Command to Inspect the Extra Vertices

```python
import smplx

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models"

m = smplx.create(
    p,
    model_type="smplx",
    gender="neutral",
    num_betas=16,
    use_pca=False,
    ext="npz",
)

print("extra vertex indices:")
print(m.vertex_joint_selector.extra_joints_idxs.tolist())
```

---

# 43. Command to Inspect the 127 Output

```python
import smplx

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models"

m = smplx.create(
    p,
    model_type="smplx",
    gender="neutral",
    num_betas=16,
    use_pca=False,
    ext="npz",
)

o = m()

print("shape:", o.joints.shape)

for i in range(o.joints.shape[1]):
    print(i, o.joints[0, i].tolist())
```

This is useful for debugging and confirming that the output tensor contains exactly:

```text
127
```

points.

---

# 44. `JOINT_NAMES` Warning

The Python package reports:

```python
import smplx.joint_names as j

print(len(j.JOINT_NAMES))
```

Observed:

```text
144
```

This does NOT mean that the model outputs 144 joints.

The authoritative runtime output is:

```python
m().joints.shape
```

which is:

```text
[1, 127, 3]
```

Therefore:

```text
JOINT_NAMES length
```

must not be confused with:

```text
actual output joint count
```

---

# 45. Reproducibility Rules

The following values are reference values for this project:

```text
Model:
SMPL-X Neutral

NUM_JOINTS:
54

J_regressor:
55 × 10475

Kinematic joints:
55

Extra vertex joints:
21

Facial landmarks:
51

Final output:
127

Parent array:
55 entries

kintree_table:
2 × 55

joint_mapper:
None

use_face_contour:
False
```

The fundamental identity is:

```text
55 + 21 + 51 = 127
```

---

# 46. Canonical Storage Principle

The reconstruction stage should save the complete canonical output.

Conceptually:

```python
np.savez_compressed(
    output_file,
    joints=joints,
    fps=fps,
    gender=gender,
    model_type="smplx",
    representation="smplx_127_joints",
)
```

The exact storage schema may later include additional metadata such as:

```text
source_file
subject
sequence
frame_count
fps
model_type
gender
joint_names
joint_indices
parents
representation
```

The key requirement is that the 127-joint representation is not discarded.

---

# 47. Stage 3 Responsibility

Stage 3 should work conceptually as:

```text
Input:
Canonical SMPL-X reconstruction

        |
        v

Validation:
Is the representation 127 joints?

        |
        v

Named extraction:

        +--> Core Body
        |
        +--> Feet / Contact
        |
        +--> Hands
        |
        +--> Face
        |
        +--> Optional custom groups

        |
        v

Save derived representations
```

---

# 48. No Information Loss Rule

The following operation is prohibited at the canonical stage:

```python
canonical = joints[:, :24]
```

The canonical representation must remain:

```text
127
```

Reduction is allowed only when generating a specific derived representation.

---

# 49. Recommended Project Data Hierarchy

```text
03_human_motion/
│
├── external/
│   └── smplx/
│       ├── models/
│       └── smplx_repository/
│
├── scripts/
│   ├── 01_prepare_amass.py
│   ├── 02_smplx_reconstruction.py
│   └── 03_extract_joints.py
│
├── data/
│   ├── raw/
│   ├── reconstructed/
│   │   └── smplx_127/
│   └── extracted/
│       ├── core_body/
│       ├── feet/
│       ├── hands/
│       ├── face/
│       └── custom/
│
└── docs/
    └── SMPLX_JOINT_STRUCTURE.md
```

The exact directory structure may be adapted to the existing project, but the conceptual separation should remain.

---

# 50. Recommended Extraction Output

A reconstructed sequence should conceptually produce:

```text
reconstructed/
    sequence_001.npz

extracted/
    core_body/
        sequence_001.npz

    feet/
        sequence_001.npz

    hands/
        sequence_001.npz

    face/
        sequence_001.npz
```

This allows each downstream experiment to consume only what it needs.

---

# 51. Main Research Pipeline

The complete research pipeline is:

```text
AMASS
  |
  v
SMPL-X Reconstruction
  |
  v
Canonical 127-Joint Representation
  |
  +----------------------------+
  |            |               |
  v            v               v
Core Body    Hands           Face
  |
  v
Feet / Contact Information
  |
  v
Normalization
  |
  v
Feature Extraction
  |
  v
Contact Detection
  |
  v
Motion Segmentation
  |
  v
Dataset Creation
  |
  v
Latent Objective Learning
```

The exact downstream combination is intentionally left flexible.

---

# 52. Future Extensibility

The architecture intentionally supports future additions such as:

```text
Core Body + Hands
Core Body + Feet
Core Body + Hands + Feet
Full Body
Body + Face
Full 127
Custom subsets
```

without changing the reconstruction stage.

This is one of the main reasons for preserving the canonical 127-joint output.

---

# 53. Final Representation Policy

The final project policy is:

```text
1. Reconstruct SMPL-X once.

2. Preserve all 127 output joints.

3. Treat the 127-joint tensor as canonical.

4. Never use the first N joints as an implicit representation.

5. Use explicit named index mappings.

6. Keep body, hands, feet, and face logically separate.

7. Use feet/contact points explicitly for contact detection.

8. Keep facial information available but separate from the main body-motion representation.

9. Allow future experiments to add groups without rerunning SMPL-X reconstruction.

10. Keep all mappings documented in code and this MD file.
```

---

# 54. Definitive Numerical Summary

```text
====================================================
SMPL-X REFERENCE VALUES
====================================================

Model:
SMPL-X Neutral

NUM_JOINTS:
54

J_regressor:
55 × 10475

Kinematic / LBS joints:
55

Extra vertex keypoints:
21

Facial landmarks:
51

Final output:
127 × 3

Kinematic parent entries:
55

kintree_table:
2 × 55

joint_mapper:
None

use_face_contour:
False

JOINT_NAMES in Python package:
144

Main canonical representation:
127 joints

Main body group:
22 anatomical joints

Feet/contact group:
6 points

Hands:
30 kinematic finger joints + 10 fingertips

Face:
3 kinematic face joints
+ 5 face vertex keypoints
+ 51 facial landmarks
====================================================
```

---

# 55. Most Important Index Ranges

For quick reference:

```text
====================================================
INDEX RANGE        CONTENT
====================================================

0–54               55 LBS / kinematic joints

55–59              Face vertex keypoints

60–65              Feet keypoints

66–75              Hand fingertips

76–126             Facial landmarks

0–126              Complete canonical SMPL-X output
====================================================
```

---

# 56. Most Important Body Indices

```text
0   Pelvis

1   L_Hip
2   R_Hip

3   Spine1

4   L_Knee
5   R_Knee

6   Spine2

7   L_Ankle
8   R_Ankle

9   Spine3

10  L_Foot
11  R_Foot

12  Neck

13  L_Collar
14  R_Collar

15  Head

16  L_Shoulder
17  R_Shoulder

18  L_Elbow
19  R_Elbow

20  L_Wrist
21  R_Wrist
```

These are the core anatomical body joints.

---

# 57. Most Important Contact Indices

```text
7   L_Ankle
8   R_Ankle

10  L_Foot
11  R_Foot

60  L_BigToe
61  L_SmallToe
62  L_Heel

63  R_BigToe
64  R_SmallToe
65  R_Heel
```

These should remain available for future contact detection.

---

# 58. Most Important Hand Indices

```text
Left hand:
25–39
66–70

Right hand:
40–54
71–75
```

---

# 59. Most Important Face Indices

```text
22  Jaw
23  L_Eye
24  R_Eye

55  Nose
56  R_Eye_Keypoint
57  L_Eye_Keypoint
58  R_Ear
59  L_Ear

76–126
Facial landmarks
```

---

# 60. Final Decision

The project does NOT use:

```text
first 24 SMPL-X joints
```

as its canonical body representation.

Instead:

```text
SMPL-X 127
     |
     +--> explicit Core Body
     |
     +--> explicit Feet / Contact
     |
     +--> explicit Hands
     |
     +--> explicit Face
```

This avoids the earlier problem where:

```text
22 = Jaw
23 = L_Eye
24 = R_Eye
```

could accidentally enter the main body skeleton.

The core body is therefore explicitly selected from:

```text
0 ... 21
```

giving:

```text
22 anatomical body joints
```

and foot/contact points are maintained separately.

If a later experiment needs exactly 24 points, the additional two points will be explicitly selected according to the experiment rather than assuming that SMPL-X's first 24 indices constitute the correct representation.

---

# 61. Final One-Line Architecture

```text
AMASS → SMPL-X Reconstruction → Canonical SMPL-X 127 → {Core Body, Feet/Contact, Hands, Face} → Normalization → Feature Extraction → Contact Detection → Motion Segmentation → Dataset Creation → Latent Objective Learning
```

---

# 62. Final One-Line Numerical Definition

```text
SMPL-X 127 = 55 LBS joints + 21 vertex keypoints + 51 facial landmarks
```

---

# 63. Final Principle

```text
RECONSTRUCT ONCE.
PRESERVE 127.
EXTRACT MANY.
DELETE NOTHING AT THE CANONICAL STAGE.
```

This is the definitive joint-structure and extraction policy for the current `latent-objective-humanoid` implementation.
