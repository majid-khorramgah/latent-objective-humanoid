# SMPL-X Joint Structure, Canonical Representation and Extraction Specification

**Project:** `latent-objective-humanoid`

**Stage:** `03_human_motion`

**Stage 3 Script:** [`03_extract_joints.py`](./03_extract_joints.py)

**Purpose:** Definitive documentation of the SMPL-X joint structure used by the project, the construction of the 127-joint output, the kinematic hierarchy, and the project-specific extraction policy.

---

# 1. Stage 3 — Joint Extraction

The implementation responsible for extracting project-specific joint representations is:

[`03_extract_joints.py`](./03_extract_joints.py)

Stage 3 is **not responsible for reconstructing SMPL-X**.

Its responsibility is to take the already reconstructed canonical SMPL-X representation and derive different views from it.

The conceptual responsibility is:

    Canonical SMPL-X 127
            |
            +-------------------+
            |                   |
            v                   v
        Core Body            Auxiliary
                                |
                +---------------+---------------+
                |               |               |
                v               v               v
              Hands           Feet            Face

The important principle is:

    Reconstruction preserves information.
    Extraction selects information.

Therefore Stage 3 must never destroy the canonical 127-joint representation.

---

# 2. Overall Motion Pipeline

The current project architecture is:

    AMASS
      |
      v
    SMPL-X Reconstruction
      |
      v
    SMPL-X 127 canonical joints
      |
      +-------------------+-------------------+
      |                   |                   |
      v                   v                   v
    Body                Hands               Face
      |
      v
    Core Body
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

Feet are maintained as a separate representation because they are especially important for contact detection and locomotion.

The detailed structure is therefore:

    SMPL-X 127
        |
        +--> Core Body
        |
        +--> Hands
        |
        +--> Feet
        |
        +--> Face

This allows future stages to combine these representations when necessary.

---

# 3. Main Design Decision

The project will use:

    SMPL-X 127 joints

as the **canonical reconstructed representation**.

No information is discarded during reconstruction.

The canonical representation can later be transformed into:

    127 -> Core Body
    127 -> Hands
    127 -> Feet
    127 -> Face
    127 -> Full Body + Hands
    127 -> Full Body + Feet
    127 -> Custom representation

This is intentionally designed so that future research decisions do not require rerunning SMPL-X reconstruction.

---

# 4. Important Discovery: 54 vs 55 vs 127

Several different numbers appear in the SMPL-X implementation.

They must not be confused.

The loaded model reports:

    m.NUM_JOINTS == 54

but:

    m.J_regressor.shape == (55, 10475)

and:

    m().joints.shape == (1, 127, 3)

These numbers represent different concepts.

The actual final output is constructed as:

    55 LBS joints
    + 21 extra vertex-based joints
    + 51 facial landmarks
    --------------------------------
    127 final output joints

Therefore:

    55 + 21 + 51 = 127

The final tensor is:

    [batch_size, 127, 3]

The runtime output tensor is the authoritative representation for the final joint count.

---

# 5. Model Configuration

The SMPL-X model used by the project is located at:

    03_human_motion/external/smplx/models

The Python repository is located at:

    03_human_motion/external/smplx/smplx_repository

The model is loaded using:

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

The actual neutral model file is:

    03_human_motion/external/smplx/models/smplx/SMPLX_NEUTRAL.npz

---

# 6. Verification of the Final Output

The following command was used:

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
    print("selector:", len(m.vertex_joint_selector.extra_joints_idxs))
    print("landmarks:", len(m.lmk_faces_idx))
    print("output:", o.joints.shape)

Expected result:

    NUM_JOINTS: 54
    J_regressor: torch.Size([55, 10475])
    selector: 21
    landmarks: 51
    output: torch.Size([1, 127, 3])

---

# 7. How the 127 Joints Are Constructed

The relevant SMPL-X forward-pass code is located in:

    03_human_motion/external/smplx/smplx_repository/smplx/body_models.py

The important part is:

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

Therefore the construction is:

    SMPL-X parameters
          |
          v
    LBS
          |
          +--> 55 joints
          |
          v
    VertexJointSelector
          |
          +--> 21 extra joints
          |
          v
    Facial landmark extraction
          |
          +--> 51 landmarks
          |
          v
    Final output
          |
          v
    127 joints

Mathematically:

    J_final = concat(J_LBS, J_extra, J_landmarks)

where:

    J_LBS       = 55 x 3
    J_extra     = 21 x 3
    J_landmarks = 51 x 3

and:

    J_final     = 127 x 3

---

# 8. Canonical 127-Joint Index Ranges

The final output is organized as:

    0 ... 54
        55 LBS / kinematic joints

    55 ... 75
        21 extra mesh-based keypoints

    76 ... 126
        51 facial landmarks

Therefore:

    0   - 54   = Kinematic/LBS skeleton
    55  - 75   = Extra vertex keypoints
    76  - 126  = Facial landmarks

This index layout must be treated as the canonical output layout for this project.

---

# 9. SMPL-X Kinematic Joint Mapping

The model contains a `joint2num` mapping.

The verified mapping is:

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

---

# 10. Complete Kinematic Parent Table

The verified parent array is:

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

The complete hierarchy is:

| Index | Name | Parent Index | Parent Name | Functional Group |
|---:|---|---:|---|---|
| 0 | Pelvis | -1 | Root | Core Body |
| 1 | L_Hip | 0 | Pelvis | Core Body |
| 2 | R_Hip | 0 | Pelvis | Core Body |
| 3 | Spine1 | 0 | Pelvis | Core Body |
| 4 | L_Knee | 1 | L_Hip | Core Body |
| 5 | R_Knee | 2 | R_Hip | Core Body |
| 6 | Spine2 | 3 | Spine1 | Core Body |
| 7 | L_Ankle | 4 | L_Knee | Core Body |
| 8 | R_Ankle | 5 | R_Knee | Core Body |
| 9 | Spine3 | 6 | Spine2 | Core Body |
| 10 | L_Foot | 7 | L_Ankle | Core Body |
| 11 | R_Foot | 8 | R_Ankle | Core Body |
| 12 | Neck | 9 | Spine3 | Core Body |
| 13 | L_Collar | 9 | Spine3 | Core Body |
| 14 | R_Collar | 9 | Spine3 | Core Body |
| 15 | Head | 12 | Neck | Core Body |
| 16 | L_Shoulder | 13 | L_Collar | Core Body |
| 17 | R_Shoulder | 14 | R_Collar | Core Body |
| 18 | L_Elbow | 16 | L_Shoulder | Core Body |
| 19 | R_Elbow | 17 | R_Shoulder | Core Body |
| 20 | L_Wrist | 18 | L_Elbow | Core Body |
| 21 | R_Wrist | 19 | R_Elbow | Core Body |
| 22 | Jaw | 15 | Head | Face |
| 23 | L_Eye | 15 | Head | Face |
| 24 | R_Eye | 15 | Head | Face |
| 25 | L_Index1 | 20 | L_Wrist | Hands |
| 26 | L_Index2 | 25 | L_Index1 | Hands |
| 27 | L_Index3 | 26 | L_Index2 | Hands |
| 28 | L_Middle1 | 20 | L_Wrist | Hands |
| 29 | L_Middle2 | 28 | L_Middle1 | Hands |
| 30 | L_Middle3 | 29 | L_Middle2 | Hands |
| 31 | L_Pinky1 | 20 | L_Wrist | Hands |
| 32 | L_Pinky2 | 31 | L_Pinky1 | Hands |
| 33 | L_Pinky3 | 32 | L_Pinky2 | Hands |
| 34 | L_Ring1 | 20 | L_Wrist | Hands |
| 35 | L_Ring2 | 34 | L_Ring1 | Hands |
| 36 | L_Ring3 | 35 | L_Ring2 | Hands |
| 37 | L_Thumb1 | 20 | L_Wrist | Hands |
| 38 | L_Thumb2 | 37 | L_Thumb1 | Hands |
| 39 | L_Thumb3 | 38 | L_Thumb2 | Hands |
| 40 | R_Index1 | 21 | R_Wrist | Hands |
| 41 | R_Index2 | 40 | R_Index1 | Hands |
| 42 | R_Index3 | 41 | R_Index2 | Hands |
| 43 | R_Middle1 | 21 | R_Wrist | Hands |
| 44 | R_Middle2 | 43 | R_Middle1 | Hands |
| 45 | R_Middle3 | 44 | R_Middle2 | Hands |
| 46 | R_Pinky1 | 21 | R_Wrist | Hands |
| 47 | R_Pinky2 | 46 | R_Pinky1 | Hands |
| 48 | R_Pinky3 | 47 | R_Pinky2 | Hands |
| 49 | R_Ring1 | 21 | R_Wrist | Hands |
| 50 | R_Ring2 | 49 | R_Ring1 | Hands |
| 51 | R_Ring3 | 50 | R_Ring2 | Hands |
| 52 | R_Thumb1 | 21 | R_Wrist | Hands |
| 53 | R_Thumb2 | 52 | R_Thumb1 | Hands |
| 54 | R_Thumb3 | 53 | R_Thumb2 | Hands |

---

# 11. Kinematic Tree

The model contains:

    kintree_table.shape == (2, 55)

The first row contains the parent indices.

The second row contains the joint indices.

The complete parent structure is:

    Joint 0  -> Parent -1
    Joint 1  -> Parent 0
    Joint 2  -> Parent 0
    Joint 3  -> Parent 0
    Joint 4  -> Parent 1
    Joint 5  -> Parent 2
    Joint 6  -> Parent 3
    Joint 7  -> Parent 4
    Joint 8  -> Parent 5
    Joint 9  -> Parent 6
    Joint 10 -> Parent 7
    Joint 11 -> Parent 8
    Joint 12 -> Parent 9
    Joint 13 -> Parent 9
    Joint 14 -> Parent 9
    Joint 15 -> Parent 12
    Joint 16 -> Parent 13
    Joint 17 -> Parent 14
    Joint 18 -> Parent 16
    Joint 19 -> Parent 17
    Joint 20 -> Parent 18
    Joint 21 -> Parent 19
    Joint 22 -> Parent 15
    Joint 23 -> Parent 15
    Joint 24 -> Parent 15
    Joint 25 -> Parent 20
    Joint 26 -> Parent 25
    Joint 27 -> Parent 26
    Joint 28 -> Parent 20
    Joint 29 -> Parent 28
    Joint 30 -> Parent 29
    Joint 31 -> Parent 20
    Joint 32 -> Parent 31
    Joint 33 -> Parent 32
    Joint 34 -> Parent 20
    Joint 35 -> Parent 34
    Joint 36 -> Parent 35
    Joint 37 -> Parent 20
    Joint 38 -> Parent 37
    Joint 39 -> Parent 38
    Joint 40 -> Parent 21
    Joint 41 -> Parent 40
    Joint 42 -> Parent 41
    Joint 43 -> Parent 21
    Joint 44 -> Parent 43
    Joint 45 -> Parent 44
    Joint 46 -> Parent 21
    Joint 47 -> Parent 46
    Joint 48 -> Parent 47
    Joint 49 -> Parent 21
    Joint 50 -> Parent 49
    Joint 51 -> Parent 50
    Joint 52 -> Parent 21
    Joint 53 -> Parent 52
    Joint 54 -> Parent 53

---

# 12. Extra Vertex-Based Joints

The SMPL-X `VertexJointSelector` adds 21 additional keypoints.

These are NOT kinematic joints.

They are selected directly from mesh vertices.

The verified vertex indices are:

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

They are appended after the 55 LBS joints.

Therefore their final output indices are:

    55 ... 75

---

# 13. Complete Extra-Joint Table

| Output Index | Name | Source | Vertex Index | Group |
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

# 14. Facial Landmarks

The model contains:

    51 facial landmarks

Verified by:

    m.lmk_faces_idx.shape

which gives:

    torch.Size([51])

These landmarks are generated from mesh faces and barycentric coordinates.

The relevant operation is conceptually:

    landmarks = vertices2landmarks(
        vertices,
        faces,
        lmk_faces_idx,
        lmk_bary_coords
    )

The landmarks are then appended:

    joints = torch.cat([joints, landmarks], dim=1)

Therefore they occupy:

    76 ... 126

---

# 15. Facial Landmark Index Layout

The 51 facial landmarks occupy:

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

These landmarks are considered facial geometry features, not primary motion-modeling joints.

---

# 16. Face Contour Configuration

The loaded model reports:

    m.use_face_contour == False

Therefore dynamic face-contour landmarks are not additionally appended.

This is consistent with:

    55 + 21 + 51 = 127

The project should preserve this configuration unless there is a deliberate future decision to enable dynamic face contours.

---

# 17. Joint Mapper

The loaded model reports:

    m.joint_mapper == None

Therefore no dataset-specific joint remapping is applied after the 127-joint structure is constructed.

This is important for reproducibility.

The current canonical output therefore remains:

    [batch, 127, 3]

without an additional runtime joint mapper.

---

# 18. Why the Canonical 127 Must Be Preserved

The project should NOT immediately reduce:

    127 -> 22
or
    127 -> 24

and save only the reduced representation.

Doing so would permanently remove information.

For example, we would lose:

    finger articulation
    fingertip positions
    toe positions
    heel positions
    facial articulation
    eye information
    ear information
    facial landmarks

Instead:

    127
     |
     +--> Core Body
     +--> Hands
     +--> Feet
     +--> Face

This makes the system reversible at the representation-selection level.

---

# 19. Correct Project-Level Segmentation

The final recommended segmentation is:

    1. Core Body
    2. Hands
    3. Feet
    4. Face

This is preferable to forcing everything into arbitrary numeric groups such as "24 joints".

The number of joints in each representation is determined by the purpose of that representation.

---

# 20. Core Body Representation

The Core Body is intended to describe the main human-body motion.

It contains:

    Pelvis
    L_Hip
    R_Hip
    Spine1
    L_Knee
    R_Knee
    Spine2
    L_Ankle
    R_Ankle
    Spine3
    L_Foot
    R_Foot
    Neck
    L_Collar
    R_Collar
    Head
    L_Shoulder
    R_Shoulder
    L_Elbow
    R_Elbow
    L_Wrist
    R_Wrist

Therefore the core kinematic body currently contains:

    22 joints

These are exactly the primary body joints from SMPL-X indices:

    0 ... 21

The important point is that this is NOT an arbitrary first-22 slice.

These 22 joints form the main articulated body chain.

---

# 21. Why Core Body Is 22 Rather Than Forcing 24

Earlier, a 24-joint representation was considered.

However, the project does not need to force the canonical SMPL-X structure into exactly 24 joints.

The more logical separation is:

    Core Body = primary articulated body
    Feet      = contact-related points
    Hands     = fine articulation
    Face      = facial articulation

The 22 core joints naturally correspond to:

    pelvis
    hips
    knees
    ankles
    feet
    spine
    neck
    head
    shoulders
    elbows
    wrists

The extra foot points:

    L_BigToe
    L_SmallToe
    L_Heel
    R_BigToe
    R_SmallToe
    R_Heel

are better preserved in the Feet representation because they are particularly useful for contact detection.

Therefore there is no reason to artificially move two arbitrary points into the Core Body merely to reach 24.

---

# 22. Core Body Index List

The project-defined Core Body is:

    CORE_BODY_INDICES = [
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

Shape:

    [T, 22, 3]

or, for batched data:

    [B, T, 22, 3]

depending on the storage convention used by Stage 3.

---

# 23. Hands Representation

Hands should remain separate from Core Body.

The kinematic finger joints are:

    Left Hand:
        L_Index1
        L_Index2
        L_Index3
        L_Middle1
        L_Middle2
        L_Middle3
        L_Pinky1
        L_Pinky2
        L_Pinky3
        L_Ring1
        L_Ring2
        L_Ring3
        L_Thumb1
        L_Thumb2
        L_Thumb3

    Right Hand:
        R_Index1
        R_Index2
        R_Index3
        R_Middle1
        R_Middle2
        R_Middle3
        R_Pinky1
        R_Pinky2
        R_Pinky3
        R_Ring1
        R_Ring2
        R_Ring3
        R_Thumb1
        R_Thumb2
        R_Thumb3

These occupy:

    25 ... 54

Additionally, fingertip keypoints occupy:

    66 ... 75

Therefore the Hands representation can contain both:

    finger articulation joints
    +
    fingertip keypoints

This is useful for future manipulation and interaction tasks.

---

# 24. Hands Index Groups

Left hand:

    LEFT_HAND_JOINTS = [
        25, 26, 27,
        28, 29, 30,
        31, 32, 33,
        34, 35, 36,
        37, 38, 39,
    ]

Right hand:

    RIGHT_HAND_JOINTS = [
        40, 41, 42,
        43, 44, 45,
        46, 47, 48,
        49, 50, 51,
        52, 53, 54,
    ]

Left fingertips:

    LEFT_HAND_TIPS = [
        66, 67, 68, 69, 70
    ]

Right fingertips:

    RIGHT_HAND_TIPS = [
        71, 72, 73, 74, 75
    ]

Complete hands representation:

    HAND_JOINTS = (
        LEFT_HAND_JOINTS
        + RIGHT_HAND_JOINTS
        + LEFT_HAND_TIPS
        + RIGHT_HAND_TIPS
    )

---

# 25. Feet Representation

Feet should be maintained separately.

This is particularly important because the project will later perform:

    Contact Detection

and foot contact is one of the most important sources of information for:

    locomotion
    gait
    support
    stance
    motion segmentation

The Feet representation should include:

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

The corresponding canonical indices are:

    FEET_INDICES = [
        7,   # L_Ankle
        8,   # R_Ankle
        10,  # L_Foot
        11,  # R_Foot
        60,  # L_BigToe
        61,  # L_SmallToe
        62,  # L_Heel
        63,  # R_BigToe
        64,  # R_SmallToe
        65,  # R_Heel
    ]

This representation has:

    10 points

---

# 26. Why Feet Are Separate

The Core Body already contains:

    L_Ankle
    R_Ankle
    L_Foot
    R_Foot

but contact detection benefits from more detailed geometry.

Therefore the additional points:

    BigToe
    SmallToe
    Heel

are retained in Feet.

This gives the contact detector more information without contaminating the main body representation with unnecessary detail.

---

# 27. Contact Detection Representation

The recommended input to the future contact detector is:

    Feet representation

rather than only:

    Core Body

The detector can use:

    ankle velocity
    foot velocity
    toe velocity
    heel velocity
    height above ground
    relative foot motion
    temporal stability

The exact contact algorithm will be defined in a later stage.

The important current decision is:

    Preserve all foot keypoints now.

---

# 28. Face Representation

Face information is kept separately.

The Face representation contains:

    Jaw
    L_Eye
    R_Eye
    Nose
    L_Eye_Keypoint
    R_Eye_Keypoint
    L_Ear
    R_Ear
    51 facial landmarks

The kinematic face joints are:

    22 = Jaw
    23 = L_Eye
    24 = R_Eye

The extra face keypoints are:

    55 = Nose
    56 = R_Eye_Keypoint
    57 = L_Eye_Keypoint
    58 = R_Ear
    59 = L_Ear

The detailed facial landmarks are:

    76 ... 126

---

# 29. Eyes Policy

Both eyes are preserved.

The project must NOT make the mistake of keeping only one eye.

The canonical representation contains:

    L_Eye = 23
    R_Eye = 24

and additional mesh keypoints:

    R_Eye_Keypoint = 56
    L_Eye_Keypoint = 57

The detailed facial landmark representation also contains landmarks around both eyes.

Therefore there is no reason to discard either eye.

The Face representation remains optional for the main motion-learning pipeline.

---

# 30. Face Is Not Part of Core Body

The following are intentionally excluded from Core Body:

    Jaw
    L_Eye
    R_Eye
    Nose
    Ears
    Facial landmarks

Reason:

The main research objective is human motion representation.

Detailed facial articulation has a different temporal and semantic structure and should not unnecessarily increase the dimensionality of the main body-motion representation.

However, the information is preserved for future use.

---

# 31. Canonical Representation vs Derived Representations

This distinction is fundamental.

## Canonical

    SMPL-X 127

This is the source of truth.

## Derived

    Core Body
    Hands
    Feet
    Face

These are views generated from the canonical representation.

The derived representations can change later without changing the reconstruction stage.

---

# 32. Recommended Data Architecture

The data flow should conceptually be:

    AMASS
      |
      v
    SMPL-X reconstruction
      |
      v
    canonical_127
      |
      +--> core_body
      |
      +--> hands
      |
      +--> feet
      |
      +--> face

The canonical representation should remain available in the processed dataset.

---

# 33. Recommended Storage

A processed motion file can conceptually contain:

    joints_127
    core_body
    hands
    feet
    face
    fps
    model_type
    gender
    source_file
    representation_version

However, if storage efficiency is important, the derived representations do not necessarily need to be duplicated.

The safest architecture is:

    Save canonical 127
    Save metadata
    Derive views when required

or, if Stage 3 is intended to be a caching stage:

    Save canonical 127
    Save selected derived representations

The canonical 127 remains mandatory.

---

# 34. Suggested Metadata

The output metadata should include:

    model_type = "smplx"

    representation = "smplx_127"

    gender = "neutral"

    num_betas = 16

    use_pca = False

    use_face_contour = False

    joint_mapper = None

    canonical_joint_count = 127

    lbs_joint_count = 55

    extra_joint_count = 21

    facial_landmark_count = 51

This makes the processed dataset self-describing.

---

# 35. Recommended Named Index Definitions

Stage 3 should use named lists rather than unexplained numeric slices.

Recommended definitions:

    CORE_BODY_INDICES = [
        0, 1, 2, 3, 4, 5,
        6, 7, 8, 9, 10, 11,
        12, 13, 14, 15,
        16, 17, 18, 19, 20, 21,
    ]

    LEFT_HAND_JOINTS = [
        25, 26, 27,
        28, 29, 30,
        31, 32, 33,
        34, 35, 36,
        37, 38, 39,
    ]

    RIGHT_HAND_JOINTS = [
        40, 41, 42,
        43, 44, 45,
        46, 47, 48,
        49, 50, 51,
        52, 53, 54,
    ]

    LEFT_HAND_TIPS = [
        66, 67, 68, 69, 70,
    ]

    RIGHT_HAND_TIPS = [
        71, 72, 73, 74, 75,
    ]

    FEET_INDICES = [
        7, 8,
        10, 11,
        60, 61, 62,
        63, 64, 65,
    ]

    FACE_INDICES = [
        22, 23, 24,
        55, 56, 57, 58, 59,
        *range(76, 127),
    ]

---

# 36. Important Rule About Numeric Ranges

Do NOT use code such as:

    core = joints[:, :24]

because this assumes that the first 24 joints are the desired project representation.

Instead:

    core = joints[:, CORE_BODY_INDICES]

This makes the definition explicit and reproducible.

Likewise:

    hands = joints[:, HAND_JOINTS]
    feet = joints[:, FEET_INDICES]
    face = joints[:, FACE_INDICES]

---

# 37. Example Extraction Logic

The conceptual Stage 3 logic is:

    core_body = joints[:, CORE_BODY_INDICES]

    left_hand = joints[:, LEFT_HAND_JOINTS + LEFT_HAND_TIPS]

    right_hand = joints[:, RIGHT_HAND_JOINTS + RIGHT_HAND_TIPS]

    hands = joints[:, HAND_JOINTS]

    feet = joints[:, FEET_INDICES]

    face = joints[:, FACE_INDICES]

The exact tensor dimension handling depends on whether the input is:

    [127, 3]

    [T, 127, 3]

or:

    [B, T, 127, 3]

Stage 3 should preserve the leading dimensions.

---

# 38. No Information Loss Principle

The following transformation is allowed:

    127 -> Core Body

    127 -> Hands

    127 -> Feet

    127 -> Face

The following is NOT acceptable as the only stored representation:

    127 -> 22
    delete everything else

because this permanently loses information.

The canonical 127 representation must remain accessible.

---

# 39. Relationship to Normalization

Normalization comes AFTER extraction of the representation required for a specific task.

The conceptual pipeline is:

    SMPL-X 127
        |
        +--> Core Body
                |
                v
            Normalization
                |
                v
            Features
                |
                v
            Segmentation
                |
                v
            Dataset
                |
                v
            Latent Objective

For contact detection:

    SMPL-X 127
        |
        v
       Feet
        |
        v
    Normalization
        |
        v
    Contact Detection

For hand-related tasks:

    SMPL-X 127
        |
        v
      Hands
        |
        v
    Normalization
        |
        v
    Hand Features

---

# 40. Relationship to Motion Segmentation

Motion segmentation should primarily operate on the body-motion representation.

The recommended starting representation is:

    Core Body

with optional additional information from:

    Feet

This allows segmentation to consider:

    body pose
    body velocity
    foot contacts
    stance/swing transitions

Hands and Face should not automatically influence the main segmentation pipeline unless the research objective later requires them.

---

# 41. Relationship to Latent Objective Learning

The main latent objective learning pipeline should initially use:

    Core Body

and potentially:

    Core Body + Feet/Contact Features

This keeps the primary representation focused on:

    human motion
    body dynamics
    locomotion
    interaction-relevant motion

Hands and Face remain available for future experiments.

This is important because the project can later test:

    Core Body only

versus:

    Core Body + Hands

versus:

    Core Body + Feet

versus:

    Core Body + Hands + Feet

without changing the underlying reconstruction data.

---

# 42. Future Extension Policy

The current representation is intentionally modular.

If future experiments require:

    hand-object interaction

then use:

    Core Body + Hands

If future experiments require:

    locomotion

then use:

    Core Body + Feet + Contact

If future experiments require:

    human communication

then Face can be added.

If future experiments require:

    full-body interaction

then:

    Core Body + Hands + Feet

can be used.

The canonical 127 representation remains unchanged.

---

# 43. Model File Inspection Commands

## Inspect model keys

    import numpy as np

    p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

    d = np.load(p, allow_pickle=True)

    print(d.files)

Observed keys include:

    bs_type
    bs_style
    J_regressor_prior
    f
    J_regressor
    kintree_table
    J
    weights_prior
    weights
    vert_sym_idxs
    posedirs
    v_template
    shapedirs
    hands_meanr
    hands_meanl
    lmk_bary_coords
    vt
    part2num
    hands_coeffsr
    lmk_faces_idx
    dynamic_lmk_faces_idx
    hands_componentsr
    dynamic_lmk_bary_coords
    ft
    hands_componentsl
    joint2num
    allow_pickle
    hands_coeffsl

---

# 44. Inspect J_regressor

    import numpy as np

    p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

    d = np.load(p, allow_pickle=True)

    print("J_regressor shape:", d["J_regressor"].shape)

Expected:

    J_regressor shape: (55, 10475)

---

# 45. Inspect Kinematic Tree

    import numpy as np

    p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

    d = np.load(p, allow_pickle=True)

    print("kintree_table shape:", d["kintree_table"].shape)
    print(d["kintree_table"])

Expected:

    kintree_table shape: (2, 55)

---

# 46. Inspect joint2num

    import numpy as np

    p = r"D:\1405\latent-objective-humanoid\03_human_motion\external\smplx\models\smplx\SMPLX_NEUTRAL.npz"

    d = np.load(p, allow_pickle=True)

    joint2num = d["joint2num"].item()

    for name, index in sorted(
        joint2num.items(),
        key=lambda x: x[1]
    ):
        print(index, name)

---

# 47. Inspect Parent Array

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

Expected:

    parents shape: torch.Size([55])

---

# 48. Inspect Extra Vertex Joints

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

    print(
        "extra joints:",
        m.vertex_joint_selector.extra_joints_idxs.tolist()
    )

Expected:

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

---

# 49. Inspect Landmark Count

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

    print("landmarks:", len(m.lmk_faces_idx))

Expected:

    landmarks: 51

---

# 50. Final Verification Script

The complete verification command is:

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

    lbs = m.J_regressor.shape[0]
    extra = len(m.vertex_joint_selector.extra_joints_idxs)
    landmarks = len(m.lmk_faces_idx)

    expected = lbs + extra + landmarks
    actual = o.joints.shape[1]

    print("========================================")
    print("SMPL-X JOINT VERIFICATION")
    print("========================================")
    print("NUM_JOINTS       :", m.NUM_JOINTS)
    print("LBS joints       :", lbs)
    print("Extra joints     :", extra)
    print("Face landmarks   :", landmarks)
    print("Expected total   :", expected)
    print("Actual output    :", actual)
    print("Output shape     :", tuple(o.joints.shape))
    print("Parent count     :", len(m.parents))
    print("Joint mapper     :", m.joint_mapper)
    print("Face contour     :", m.use_face_contour)
    print("========================================")

Expected:

    ========================================
    SMPL-X JOINT VERIFICATION
    ========================================
    NUM_JOINTS       : 54
    LBS joints       : 55
    Extra joints     : 21
    Face landmarks   : 51
    Expected total   : 127
    Actual output    : 127
    Output shape     : (1, 127, 3)
    Parent count     : 55
    Joint mapper     : None
    Face contour     : False
    ========================================

---

# 51. Definitive Representation Table

| Representation | Canonical Indices | Count | Main Purpose |
|---|---|---:|---|
| Canonical | 0–126 | 127 | Complete information |
| Core Body | 0–21 | 22 | Main human motion |
| Hands | 25–54 + 66–75 | 40 | Hand articulation |
| Feet | 7,8,10,11,60–65 | 10 | Contact and locomotion |
| Face | 22–24,55–59,76–126 | 59 | Facial information |

Note:

The representations overlap intentionally.

For example:

    L_Ankle

belongs to Core Body and Feet.

This is not duplication of information at the canonical level.

It is simply a task-specific view.

---

# 52. Why Overlapping Representations Are Correct

A joint can be relevant to more than one task.

For example:

    L_Ankle

is:

    Core Body information

and:

    Feet/contact information

Similarly:

    L_Wrist

belongs to:

    Core Body

and is the root of:

    Hand articulation

Therefore the representations are not mutually exclusive partitions.

They are **functional views** of the canonical representation.

This is the correct design for the project.

---

# 53. Canonical vs Functional Partition

The project should NOT think of the 127 joints as:

    Body OR Hands OR Feet OR Face

Instead:

    Canonical 127
          |
          +--> functional view: Core Body
          |
          +--> functional view: Hands
          |
          +--> functional view: Feet
          |
          +--> functional view: Face

This distinction is important.

The same canonical joint may appear in more than one downstream view when logically useful.

---

# 54. Stage 3 Responsibilities

`03_extract_joints.py` should:

    1. Load the canonical SMPL-X output.
    2. Validate that it contains 127 joints.
    3. Define named joint-index mappings.
    4. Extract Core Body.
    5. Extract Hands.
    6. Extract Feet.
    7. Extract Face.
    8. Preserve metadata.
    9. Save the canonical representation.
    10. Save derived representations if required by the dataset pipeline.

It should NOT:

    - reconstruct SMPL-X
    - change the SMPL-X kinematic hierarchy
    - delete canonical information
    - invent a new joint ordering without documentation
    - assume 24 joints by slicing the first 24 indices

---

# 55. Future-Proof Design

The current design allows the following future experiments without rerunning reconstruction:

    Experiment A:
        Core Body

    Experiment B:
        Core Body + Feet

    Experiment C:
        Core Body + Contact

    Experiment D:
        Core Body + Hands

    Experiment E:
        Core Body + Hands + Feet

    Experiment F:
        Core Body + Hands + Feet + Face

All experiments can originate from:

    SMPL-X 127

---

# 56. Definitive Project Numbers

The following values are now considered verified:

    SMPL-X NUM_JOINTS:
        54

    J_regressor:
        (55, 10475)

    LBS joints:
        55

    Extra vertex joints:
        21

    Facial landmarks:
        51

    Final output:
        127

    Final tensor:
        [batch, 127, 3]

    Parent array:
        55 entries

    Kinematic joint mapping:
        55 entries

    joint_mapper:
        None

    use_face_contour:
        False

    Core Body:
        22 joints

    Hands:
        40 points

    Feet:
        10 points

    Face:
        59 points

---

# 57. Important Formula

The canonical representation is:

    55 LBS
    +
    21 extra vertex keypoints
    +
    51 facial landmarks
    =
    127 canonical joints

Therefore:

    SMPL-X 127 = Source of Truth

and:

    Core Body
    Hands
    Feet
    Face

are derived task-specific views.

---

# 58. Final Architecture

The final agreed architecture is:

                    AMASS
                      |
                      v
             SMPL-X Reconstruction
                      |
                      v
               SMPL-X 127
             Canonical Motion
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
     Core Body      Hands          Face
        |
        +-------------------+
        |
        v
       Feet
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

More precisely, Feet is a parallel functional representation derived from the canonical 127 and can feed Contact Detection independently.

---

# 59. Final Decision

The project does NOT commit to a mandatory 24-joint representation.

Instead:

    Canonical:
        127 joints

    Main body:
        22 Core Body joints

    Auxiliary:
        Hands
        Feet
        Face

This is a cleaner and more extensible design.

If a later experiment requires exactly 24, 25, 26, or another number of joints, a new named representation can be created from the canonical 127 without modifying the reconstruction stage.

---

# 60. Final One-Line Summary

    AMASS
    -> SMPL-X Reconstruction
    -> 127 canonical joints
    -> Core Body / Hands / Feet / Face
    -> task-specific normalization
    -> features
    -> contact detection
    -> motion segmentation
    -> dataset
    -> latent objective learning

The most important rule is:

    NEVER discard the canonical 127-joint representation.
    ALWAYS derive smaller representations from it.

---

# 61. Reproducibility Checklist

Before modifying Stage 3, verify:

    [ ] SMPL-X model path is correct
    [ ] SMPLX_NEUTRAL.npz exists
    [ ] J_regressor.shape == (55, 10475)
    [ ] m.NUM_JOINTS == 54
    [ ] extra joints == 21
    [ ] facial landmarks == 51
    [ ] final output == 127
    [ ] output shape == [batch, 127, 3]
    [ ] parent array length == 55
    [ ] kintree_table.shape == (2, 55)
    [ ] joint_mapper is None
    [ ] use_face_contour is False
    [ ] both eyes are preserved
    [ ] hands are preserved
    [ ] feet keypoints are preserved
    [ ] facial landmarks are preserved
    [ ] Core Body is defined by explicit indices
    [ ] no information is discarded from canonical data
    [ ] Stage 3 only performs extraction

---

# 62. Final Rule for Future Development

Any future representation must follow this pattern:

    CANONICAL_127
          |
          v
    explicit named indices
          |
          v
    new representation

Never change the canonical ordering merely to make a downstream representation convenient.

The canonical SMPL-X ordering remains fixed.

All project-specific conventions belong in Stage 3 and later.

---

# 63. Final Status

This document records the verified SMPL-X structure and the current project-level extraction policy.

The current source of truth is:

    SMPL-X 127-joint output

The current primary representation is:

    Core Body = 22 joints

The current auxiliary representations are:

    Hands
    Feet
    Face

The architecture remains open to future additions.

No future representation decision should require changing the canonical SMPL-X reconstruction.

---

# 64. Stage 3 Reference

Implementation:

[03_extract_joints.py](./03_extract_joints.py)

Documentation:

[SMPL-X Joint Structure and Extraction Specification](./SMPLX_JOINT_SPECIFICATION.md)

Canonical principle:

    127 -> derive views

not:

    127 -> delete information
