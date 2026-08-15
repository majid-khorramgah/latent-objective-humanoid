# SMPL-X Joint Structure and Extraction Specification

**Project:** `latent-objective-humanoid`

**Stage:** `03_human_motion`

**Purpose:** Definitive documentation of the SMPL-X joint structure used by the project, including the 127 output joints, their origin, kinematic parents, naming, and the proposed extraction policy.

---

## 1. Model Configuration

The SMPL-X model used in this project is located at:

`03_human_motion/external/smplx/models`

The repository containing the Python implementation is located at:

`03_human_motion/external/smplx/smplx_repository`

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

---

# 2. Important Discovery: 54 vs 55 vs 127

One of the most important findings during implementation is that several different quantities must not be confused.

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

print("NUM_JOINTS =", m.NUM_JOINTS)
print("output test =", m().joints.shape)
```

Output:

```text
NUM_JOINTS = 54
output test = torch.Size([1, 127, 3])
```

At first this appears contradictory.

It is not.

The reason is that `NUM_JOINTS` is not the final number of joints returned by the SMPL-X forward pass.

---

# 3. Actual Construction of the 127 Output Joints

The SMPL-X forward pass was inspected in:

`smplx/body_models.py`

The relevant code is:

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
    joints = self.joint_mapper(joints=joints, vertices=vertices)
```

Therefore the final output is constructed in three stages.

---

## 3.1 Stage A — LBS joints

The model contains:

```text
J_regressor.shape = (55, 10475)
```

Therefore the LBS stage produces:

```text
55 joints
```

These correspond to the SMPL-X kinematic skeleton.

---

## 3.2 Stage B — Extra vertex-based joints

The `VertexJointSelector` adds:

```text
21 extra joints
```

These are selected directly from mesh vertices.

They include:

- 5 face keypoints
- 6 foot keypoints
- 10 hand fingertip keypoints

Therefore:

```text
55 + 21 = 76
```

---

## 3.3 Stage C — Facial landmarks

The model contains:

```text
51 landmarks
```

These are generated using:

```python
vertices2landmarks(
    vertices,
    self.faces_tensor,
    lmk_faces_idx,
    lmk_bary_coords,
)
```

Therefore:

```text
76 + 51 = 127
```

Hence:

```text
55 LBS joints
+ 21 extra vertex joints
+ 51 facial landmarks
--------------------------------
127 final output joints
```

This is the actual source of the tensor:

```text
torch.Size([batch_size, 127, 3])
```

---

# 4. Verification Commands

## 4.1 Check model output

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

print("output:", o.joints.shape)
print("NUM_JOINTS:", m.NUM_JOINTS)
```

Expected:

```text
output: torch.Size([1, 127, 3])
NUM_JOINTS: 54
```

---

## 4.2 Check the three components

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

print("NUM_JOINTS:", m.NUM_JOINTS)
print("J_regressor:", m.J_regressor.shape)
print("extra joints:", len(m.vertex_joint_selector.extra_joints_idxs))
print("landmarks:", len(m.lmk_faces_idx))

print(
    "total:",
    m.J_regressor.shape[0]
    + len(m.vertex_joint_selector.extra_joints_idxs)
    + len(m.lmk_faces_idx)
)
```

Expected:

```text
NUM_JOINTS: 54
J_regressor: torch.Size([55, 10475])
extra joints: 21
landmarks: 51
total: 127
```

---

# 5. SMPL-X Model File

The actual model file is:

```text
03_human_motion/external/smplx/models/smplx/SMPLX_NEUTRAL.npz
```

The model contains:

```python
import numpy as np

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

d = np.load(p, allow_pickle=True)

print(d.files)
```

The relevant keys are:

```text
J_regressor
kintree_table
joint2num
lmk_faces_idx
lmk_bary_coords
dynamic_lmk_faces_idx
dynamic_lmk_bary_coords
v_template
shapedirs
posedirs
weights
f
```

The complete list observed in the model is:

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

# 6. Kinematic Joint Mapping

The model contains:

```python
joint2num
```

which maps joint names to numerical indices.

The extracted mapping is:

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

# 7. Kinematic Parent Structure

The model contains:

```python
kintree_table.shape == (2, 55)
```

The parent array observed from the model is:

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

The complete table is given below.

---

# 8. Complete Kinematic Skeleton Table

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
| 13 | L_Collar | 9 | Spine3 | Auxiliary Upper Body |
| 14 | R_Collar | 9 | Spine3 | Auxiliary Upper Body |
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

# 9. Important Note About the 55th LBS Joint

The SMPL-X model reports:

```text
J_regressor.shape = (55, 10475)
```

while:

```text
joint2num
```

contains named kinematic joints indexed from:

```text
0 ... 54
```

The 55 LBS joints therefore occupy output positions:

```text
0 ... 54
```

The numerical indexing in the model's `kintree_table` is the authoritative source for the kinematic hierarchy.

Do not infer the final 127-joint structure from `NUM_JOINTS` alone.

The actual tensor output is the authoritative representation:

```text
[batch, 127, 3]
```

---

# 10. Extra Vertex-Based Joints

The SMPL-X `VertexJointSelector` was inspected.

The implementation is:

```python
class VertexJointSelector(nn.Module):

    def __init__(
        self,
        vertex_ids=None,
        use_hands=True,
        use_feet_keypoints=True,
        **kwargs
    ):
        super(VertexJointSelector, self).__init__()

        extra_joints_idxs = []

        face_keyp_idxs = np.array([
            vertex_ids['nose'],
            vertex_ids['reye'],
            vertex_ids['leye'],
            vertex_ids['rear'],
            vertex_ids['lear']
        ], dtype=np.int64)

        extra_joints_idxs = np.concatenate([
            extra_joints_idxs,
            face_keyp_idxs
        ])

        if use_feet_keypoints:
            feet_keyp_idxs = np.array([
                vertex_ids['LBigToe'],
                vertex_ids['LSmallToe'],
                vertex_ids['LHeel'],
                vertex_ids['RBigToe'],
                vertex_ids['RSmallToe'],
                vertex_ids['RHeel']
            ], dtype=np.int32)

            extra_joints_idxs = np.concatenate([
                extra_joints_idxs,
                feet_keyp_idxs
            ])

        if use_hands:
            self.tip_names = [
                'thumb',
                'index',
                'middle',
                'ring',
                'pinky'
            ]

            tips_idxs = []

            for hand_id in ['l', 'r']:
                for tip_name in self.tip_names:
                    tips_idxs.append(
                        vertex_ids[hand_id + tip_name]
                    )

            extra_joints_idxs = np.concatenate([
                extra_joints_idxs,
                tips_idxs
            ])

        self.register_buffer(
            'extra_joints_idxs',
            to_tensor(
                extra_joints_idxs,
                dtype=torch.long
            )
        )
```

The actual vertex indices in the loaded neutral model are:

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

These are not kinematic joints.

They are mesh vertices selected to represent useful keypoints.

---

# 11. Complete Extra Joint Table

The extra joints are appended after the 55 LBS joints.

Therefore their final output indices are:

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
| 60 | L_BigToe | Vertex | 5770 | Foot |
| 61 | L_SmallToe | Vertex | 5780 | Foot |
| 62 | L_Heel | Vertex | 8846 | Foot |
| 63 | R_BigToe | Vertex | 8463 | Foot |
| 64 | R_SmallToe | Vertex | 8474 | Foot |
| 65 | R_Heel | Vertex | 8635 | Foot |
| 66 | L_Thumb_Tip | Vertex | 5361 | Hand |
| 67 | L_Index_Tip | Vertex | 4933 | Hand |
| 68 | L_Middle_Tip | Vertex | 5058 | Hand |
| 69 | L_Ring_Tip | Vertex | 5169 | Hand |
| 70 | L_Pinky_Tip | Vertex | 5286 | Hand |
| 71 | R_Thumb_Tip | Vertex | 8079 | Hand |
| 72 | R_Index_Tip | Vertex | 7669 | Hand |
| 73 | R_Middle_Tip | Vertex | 7794 | Hand |
| 74 | R_Ring_Tip | Vertex | 7905 | Hand |
| 75 | R_Pinky_Tip | Vertex | 8022 | Hand |

---

# 12. Facial Landmarks

The model contains:

```text
51 facial landmarks
```

Verified with:

```python
print(m.lmk_faces_idx.shape)
```

Expected:

```text
torch.Size([51])
```

The landmarks are generated using:

```python
landmarks = vertices2landmarks(
    vertices,
    self.faces_tensor,
    lmk_faces_idx,
    lmk_bary_coords
)
```

They are then appended to the joints:

```python
joints = torch.cat([joints, landmarks], dim=1)
```

Therefore the facial landmarks occupy:

```text
76 ... 126
```

---

# 13. Facial Landmark Names

The package's joint-name table provides the following facial landmark names after the first 76 joints.

The relevant sequence is:

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

These landmarks are facial geometry landmarks rather than kinematic body joints.

---

# 14. Complete 127-Joint Output Layout

The final output tensor is:

```text
joints.shape = [batch_size, 127, 3]
```

The index ranges are:

```text
0 ... 54
    55 LBS / kinematic joints

55 ... 75
    21 extra vertex-based keypoints

76 ... 126
    51 facial landmarks
```

Therefore:

```text
0   - 54   = Kinematic/LBS skeleton
55  - 75   = Extra mesh keypoints
76  - 126  = Facial landmarks
```

---

# 15. Complete 127-Index Reference Table

| Index Range | Count | Representation | Purpose |
|---|---:|---|---|
| 0–54 | 55 | SMPL-X LBS joints | Body + hands + jaw/eyes |
| 55–59 | 5 | Vertex keypoints | Nose, eyes, ears |
| 60–65 | 6 | Vertex keypoints | Toes and heels |
| 66–75 | 10 | Vertex keypoints | Hand fingertips |
| 76–126 | 51 | Facial landmarks | Detailed face geometry |
| **0–126** | **127** | **Complete output** | **All joints/keypoints** |

---

# 16. Why We Should NOT Throw Away the Other Joints

The project should not destroy the complete 127-joint representation.

Instead, the recommended architecture is:

```text
SMPL-X reconstruction
        |
        v
127-joint canonical representation
        |
        +--------------------+
        |                    |
        v                    v
   Core body view       Auxiliary views
        |                    |
        v                    +--> Hands
    24-joint body            +--> Feet
        |                    +--> Face
        |                    +--> Facial landmarks
        |
        v
Motion normalization
        |
        v
Feature extraction
        |
        v
Segmentation
        |
        v
Latent objective learning
```

The 127-joint representation should therefore be considered the **canonical reconstruction output**.

The smaller representations should be derived from it.

---

# 17. Proposed 24-Joint Core Body Representation

For the main human-motion representation, the recommended core is a body-centric 24-joint representation.

The goal is to retain:

- global body position
- pelvis
- lower body
- spine
- feet
- neck
- head
- shoulders
- elbows
- wrists

while excluding:

- facial articulation
- eyes
- jaw
- finger joints
- detailed facial landmarks

The proposed core joint list is:

| Core Index | SMPL-X Index | Name |
|---:|---:|---|
| 0 | 0 | Pelvis |
| 1 | 1 | L_Hip |
| 2 | 2 | R_Hip |
| 3 | 3 | Spine1 |
| 4 | 4 | L_Knee |
| 5 | 5 | R_Knee |
| 6 | 6 | Spine2 |
| 7 | 7 | L_Ankle |
| 8 | 8 | R_Ankle |
| 9 | 9 | Spine3 |
| 10 | 10 | L_Foot |
| 11 | 11 | R_Foot |
| 12 | 12 | Neck |
| 13 | 13 | L_Collar |
| 14 | 14 | R_Collar |
| 15 | 15 | Head |
| 16 | 16 | L_Shoulder |
| 17 | 17 | R_Shoulder |
| 18 | 18 | L_Elbow |
| 19 | 19 | R_Elbow |
| 20 | 20 | L_Wrist |
| 21 | 21 | R_Wrist |
| 22 | 60 | L_BigToe |
| 23 | 63 | R_BigToe |

### Note

There are different conventions for a "24-joint human skeleton".

Therefore the exact project convention must be explicitly defined rather than assumed.

For this project, the important principle is:

```text
Do not overwrite the 127-joint representation.
Create the project-specific 24-joint representation by indexing the canonical output.
```

If a different 24-joint convention is chosen later, only the extraction index list changes.

---

# 18. Recommended Data Views

The canonical representation should remain:

```text
127 joints × 3 coordinates
```

From this representation we can derive several views.

## View A — Core body

Recommended for:

- motion modeling
- locomotion
- body dynamics
- latent objective learning
- general motion features

Contains approximately:

```text
24 joints
```

---

## View B — Full body

Contains:

```text
body
+
hands
+
feet keypoints
+
face keypoints
```

This can be used when more detailed body information is needed.

---

## View C — Hand

Contains:

```text
finger joints
+
finger tips
```

Useful for:

- manipulation
- object interaction
- hand-object interaction
- fine-grained motion

---

## View D — Feet

Contains:

```text
ankles
+
feet
+
big toes
+
small toes
+
heels
```

Useful for:

- contact detection
- locomotion
- gait
- support polygon estimation

---

## View E — Face

Contains:

```text
jaw
eyes
nose
ears
facial landmarks
```

This should be kept separate from the main body representation unless facial motion becomes relevant to the research objective.

---

# 19. What Should Be Kept vs Separated

The recommendation is **not to delete anything at reconstruction time**.

Instead:

| Component | Keep? | Main representation? | Separate representation? |
|---|---|---|---|
| Pelvis | Yes | Yes | No |
| Hips | Yes | Yes | No |
| Knees | Yes | Yes | No |
| Ankles | Yes | Yes | No |
| Feet | Yes | Yes | No |
| Spine | Yes | Yes | No |
| Neck | Yes | Yes | No |
| Head | Yes | Yes | No |
| Shoulders | Yes | Yes | No |
| Elbows | Yes | Yes | No |
| Wrists | Yes | Yes | No |
| Finger joints | Yes | No | Yes |
| Finger tips | Yes | No | Yes |
| Jaw | Yes | No | Yes |
| Eyes | Yes | No | Yes |
| Nose | Yes | No | Yes |
| Ears | Yes | No | Yes |
| Toe keypoints | Yes | Optional | Yes |
| Heel keypoints | Yes | Optional | Yes |
| Facial landmarks | Yes | No | Yes |

The rule is:

```text
Preserve everything.
Select what is needed later.
Do not lose information during reconstruction.
```

---

# 20. Why This Design Is Better

If the reconstruction stage saves only 24 joints:

```text
127 -> 24
```

then information is permanently lost.

For example:

```text
finger motion
facial geometry
heel position
toe position
eye landmarks
ear landmarks
```

cannot be recovered later.

But if reconstruction saves:

```text
127 joints
```

then later stages can create:

```text
127 -> 24
127 -> hand
127 -> feet
127 -> face
127 -> custom representation
```

This makes the pipeline much more flexible.

---

# 21. `JOINT_NAMES` vs `joint2num`

The Python package exposes:

```python
import smplx.joint_names as j

print(len(j.JOINT_NAMES))
print(list(enumerate(j.JOINT_NAMES)))
```

The observed result was:

```text
JOINT_NAMES: 144
```

The first 127 entries correspond to the useful sequence described above.

However, the package contains additional names beyond the 127-joint forward output.

Therefore:

```text
JOINT_NAMES
```

should not be treated as:

```text
number of output joints
```

The authoritative runtime output is:

```python
m().joints.shape
```

which is:

```text
[1, 127, 3]
```

For the model's actual kinematic hierarchy, use:

```text
joint2num
kintree_table
J_regressor
```

---

# 22. Command to Inspect JOINT_NAMES

```python
import smplx
import smplx.joint_names as j

print("smplx:", smplx.__file__)
print("JOINT_NAMES:", len(j.JOINT_NAMES))

for i, name in enumerate(j.JOINT_NAMES):
    print(i, name)
```

Observed:

```text
JOINT_NAMES: 144
```

---

# 23. Command to Inspect `joint2num`

```python
import numpy as np

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

d = np.load(p, allow_pickle=True)

joint2num = d["joint2num"].item()

print(joint2num)
```

---

# 24. Command to Inspect the Kinematic Tree

```python
import numpy as np

p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

d = np.load(p, allow_pickle=True)

print("kintree_table shape:", d["kintree_table"].shape)
print(d["kintree_table"])
```

Observed:

```text
kintree_table shape: (2, 55)
```

---

# 25. Command to Inspect Parent Indices

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

print("parents shape:", m.parents.shape)
print("parents:", m.parents.tolist())
```

Observed:

```text
parents shape: torch.Size([55])

parents:
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

# 26. Command to Inspect the Vertex Joint Selector

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

print("vertex_joint_selector =", m.vertex_joint_selector)

print(
    "extra idx =",
    m.vertex_joint_selector.extra_joints_idxs.tolist()
)

print(
    "landmarks =",
    len(m.lmk_faces_idx)
)

print(
    "use_face_contour =",
    m.use_face_contour
)
```

Observed:

```text
NUM_JOINTS = 54

extra idx =
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

landmarks = 51

use_face_contour = False
```

---

# 27. Command to Verify the 127 Output

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

print("J_regressor:", m.J_regressor.shape)

print(
    "extra:",
    len(m.vertex_joint_selector.extra_joints_idxs)
)

print(
    "landmarks:",
    len(m.lmk_faces_idx)
)

print(
    "expected:",
    m.J_regressor.shape[0]
    + len(m.vertex_joint_selector.extra_joints_idxs)
    + len(m.lmk_faces_idx)
)

print(
    "actual:",
    o.joints.shape[1]
)
```

Expected:

```text
shape: torch.Size([1, 127, 3])

J_regressor:
torch.Size([55, 10475])

extra:
21

landmarks:
51

expected:
127

actual:
127
```

---

# 28. SMPL-X Forward-Pass Structure

The effective pipeline inside the model is:

```text
SMPL-X parameters
      |
      v
Linear Blend Skinning (LBS)
      |
      +--> 55 regressed joints
      |
      v
VertexJointSelector
      |
      +--> 21 mesh-based keypoints
      |
      v
Face landmark extraction
      |
      +--> 51 facial landmarks
      |
      v
Optional joint mapper
      |
      v
Final output
      |
      v
[batch, 127, 3]
```

In mathematical form:

```text
J_final =
    concat(
        J_LBS,
        J_extra,
        J_landmarks
    )
```

with:

```text
J_LBS       ∈ R^(55 × 3)
J_extra     ∈ R^(21 × 3)
J_landmarks ∈ R^(51 × 3)

J_final     ∈ R^(127 × 3)
```

---

# 29. `joint_mapper`

The loaded model reports:

```python
print(m.joint_mapper)
```

Result:

```text
None
```

Therefore there is no additional dataset-specific joint mapping applied at runtime.

The relevant model code is:

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

the 127-joint output is not remapped after construction.

This is important for reproducibility.

---

# 30. Face Contour

The loaded model reports:

```python
print(m.use_face_contour)
```

Result:

```text
False
```

Therefore the dynamic face contour landmarks are not additionally appended.

The 51 landmarks correspond to the configured static landmark set.

This explains why:

```text
55 + 21 + 51 = 127
```

rather than a larger number.

---

# 31. Recommended Canonical Storage Format

The reconstruction stage should store the canonical representation without deleting joints.

Recommended structure:

```text
data/
└── processed/
    └── smplx/
        └── <dataset>/
            └── <subject>/
                └── <motion>.npz
```

The canonical motion file should contain enough information to reproduce downstream representations.

Recommended fields:

```text
joints
fps
gender
source_file
joint_names
joint_indices
model_type
representation
```

Example conceptual structure:

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

---

# 32. Important Principle for `03_extract_joints.py`

The purpose of:

```text
03_extract_joints.py
```

should NOT be to reconstruct SMPL-X again.

SMPL-X reconstruction has already been completed by:

```text
02_smplx_reconstruction.py
```

The responsibility of:

```text
03_extract_joints.py
```

should be:

```text
Canonical SMPL-X output
        |
        v
Select/index joints
        |
        +--> core body
        +--> hands
        +--> feet
        +--> face
        +--> optional custom representations
```

Therefore the script should operate on the processed SMPL-X data.

---

# 33. Separation Policy

The project should use the following conceptual hierarchy:

```text
                 SMPL-X 127
                     |
       +-------------+-------------+
       |             |             |
       v             v             v
   Core Body      Hands          Face
       |
       v
   24-joint
   representation
```

Additional derived representations may include:

```text
Feet
Full Body
Body + Hands
Body + Feet
Body + Hands + Feet
```

---

# 34. Do Not Hard-Code Meaningless Numeric Ranges

Avoid code such as:

```python
joints = joints[:, :24]
```

unless the exact 24-joint convention has been explicitly defined.

Instead use named index mappings.

For example:

```python
CORE_JOINTS = [
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

Then explicitly add whichever foot/contact keypoints are part of the final 24-joint convention.

---

# 35. Why Named Index Lists Are Important

Using:

```python
joints[:, [0, 1, 2, ...]]
```

without comments makes the code difficult to audit.

Prefer:

```python
CORE_JOINTS = [
    0,   # pelvis
    1,   # left hip
    2,   # right hip
    3,   # spine1
    4,   # left knee
    5,   # right knee
    6,   # spine2
    7,   # left ankle
    8,   # right ankle
    9,   # spine3
    10,  # left foot
    11,  # right foot
    12,  # neck
    13,  # left collar
    14,  # right collar
    15,  # head
    16,  # left shoulder
    17,  # right shoulder
    18,  # left elbow
    19,  # right elbow
    20,  # left wrist
    21,  # right wrist
]
```

This makes the representation auditable.

---

# 36. Current Project Decision

The current decision is:

## Canonical representation

```text
SMPL-X 127 joints
```

Keep all reconstructed joints.

---

## Main motion representation

Use a body-centric representation derived from the canonical 127-joint representation.

Target:

```text
24-joint core body representation
```

The exact 24-joint index list must be stored as a named project constant.

---

## Hands

Keep separately.

Do not delete the finger joints or fingertips.

---

## Feet

Keep separately because they are useful for:

- contact detection
- locomotion
- gait
- support estimation

---

## Face

Keep separately.

Do not include detailed facial landmarks in the main body representation.

---

# 37. Final Representation Hierarchy

The intended data hierarchy is:

```text
                    AMASS
                      |
                      v
             SMPL-X Reconstruction
                      |
                      v
               SMPL-X 127 joints
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       Body        Hands        Face
          |
          v
    Core 24 joints
          |
          v
   Normalization
          |
          v
   Feature extraction
          |
          v
 Contact detection
          |
          v
 Motion segmentation
          |
          v
 Dataset creation
          |
          v
 Latent objective learning
```

---

# 38. Reproducibility Checklist

Before changing the extraction code, verify:

```text
[ ] SMPL-X model path is correct
[ ] SMPLX_NEUTRAL.npz exists
[ ] J_regressor.shape == (55, 10475)
[ ] m.NUM_JOINTS == 54
[ ] len(extra_joints) == 21
[ ] len(landmarks) == 51
[ ] m().joints.shape[-2] == 127
[ ] joint_mapper is None
[ ] use_face_contour is False
[ ] kintree_table.shape == (2, 55)
[ ] parent array length == 55
[ ] canonical output is preserved
[ ] downstream extraction uses explicit index lists
```

---

# 39. Definitive Numbers

The following numbers should be treated as the reference for this project:

```text
SMPL-X NUM_JOINTS:
54

J_regressor:
55 × 10475

LBS output joints:
55

Extra vertex joints:
21

Facial landmarks:
51

Final output:
127 × 3

Kinematic parent array:
55 entries

joint2num:
55 named kinematic entries

JOINT_NAMES in Python package:
144 entries

joint_mapper:
None

use_face_contour:
False
```

Most importantly:

```text
55 + 21 + 51 = 127
```

---

# 40. Final Decision

The project will treat:

```text
SMPL-X 127-joint output
```

as the **canonical reconstructed human-motion representation**.

No joint is discarded at reconstruction time.

`03_extract_joints.py` will perform deterministic extraction into downstream representations.

The main body representation will be a project-defined 24-joint representation.

Hands, feet, and facial landmarks will remain available as separate representations.

This guarantees that future stages can change their representation without having to rerun the expensive SMPL-X reconstruction stage.

---

# 41. One-Line Summary

```text
AMASS → SMPL-X → 55 LBS joints + 21 vertex keypoints + 51 facial landmarks = 127 canonical joints → derive 24-joint body / hands / feet / face representations
```
