# Motion Representation

## 1. Purpose

The purpose of this stage is to define the representation used to describe
human motion after AMASS preprocessing and SMPL-X reconstruction.

The representation must preserve the information required for:

- Human motion analysis
- Feature extraction
- Motion segmentation
- Objective inference
- Future comparison with humanoid motion

The goal is NOT to directly learn a human objective at this stage.

---

## 2. Representation Pipeline

The human motion representation is constructed as:

    AMASS
      ↓
    SMPL-X Reconstruction
      ↓
    3D Joint Positions
      ↓
    Normalized Motion
      ↓
    Temporal Motion Representation
      ↓
    Feature Extraction

The resulting representation will be used by the later objective-learning
stages.

---

## 3. Primary Motion Representation

The primary representation is a temporal sequence of 3D human joint positions.

For a motion sequence:

    X = {x_1, x_2, ..., x_T}

where each frame is:

    x_t ∈ R^(J × 3)

with:

- T = number of frames
- J = number of selected joints
- 3 = XYZ spatial coordinates

Therefore:

    X ∈ R^(T × J × 3)

This representation describes how the human body configuration evolves
over time.

---

## 4. Coordinate Representation

The raw joint positions may contain global translation and orientation
effects that are not necessarily relevant to the behavioral analysis.

Therefore, the preprocessing stage should define a consistent coordinate
system.

The initial representation should preserve:

- Relative body configuration
- Temporal movement
- Global locomotion information when relevant

Possible normalization operations include:

- Root-relative joint positions
- Root orientation normalization
- Height normalization
- Translation normalization

These transformations must be applied consistently across the dataset.

---

## 5. Root and Body Representation

The human root is used as a reference for describing body configuration.

A root-relative representation can be written as:

    p_j'(t) = p_j(t) - p_root(t)

where:

- p_j(t) = position of joint j at time t
- p_root(t) = root position at time t

This separates body configuration from global translation.

However, global root motion should not be discarded completely because
locomotion-related information such as walking direction and forward
velocity may be important for later objective inference.

Therefore, the dataset may preserve both:

    Local Body Motion
          +
    Global Root Motion

---

## 6. Temporal Representation

Human movement is fundamentally temporal.

Therefore, a single pose is not considered sufficient to describe a
movement objective.

The representation preserves sequences:

    Pose(t-1)
        ↓
      Pose(t)
        ↓
    Pose(t+1)

This allows later stages to analyze:

- Movement direction
- Temporal coordination
- Velocity
- Acceleration
- Contact transitions
- Locomotion patterns

---

## 7. Derived Motion Quantities

Additional motion quantities are derived from the joint trajectories.

### Velocity

Approximate joint velocity:

    v_j(t) ≈ [p_j(t) - p_j(t-1)] / Δt

### Acceleration

Approximate joint acceleration:

    a_j(t) ≈ [v_j(t) - v_j(t-1)] / Δt

These quantities provide information about temporal dynamics that cannot
be obtained from static joint positions alone.

---

## 8. Contact Information

Foot-ground interaction is potentially important for locomotion.

Therefore, contact information may be extracted for selected foot joints.

A contact indicator can be represented as:

    c_foot(t) ∈ {0,1}

where:

- 1 = likely contact
- 0 = likely non-contact

Contact detection should be treated as an extracted motion feature rather
than as a predefined human objective.

The contact signal can later help identify:

- Stance phases
- Swing phases
- Foot placement
- Step timing

---

## 9. Motion Representation Used for Later Objective Learning

The representation provided to later stages should contain sufficient
information to evaluate candidate behavioral explanations.

Initial representation:

    R_human =
    {
        joint positions,
        root motion,
        velocity,
        acceleration,
        contact information
    }

Not every quantity must necessarily be used by the final objective model.

The purpose of this stage is to preserve the relevant information so that
later experiments can determine which quantities are actually useful.

---

## 10. Why This Representation?

This representation is intentionally structured rather than immediately
using a large neural latent space.

Advantages:

- Interpretable
- Physically meaningful
- Compatible with AMASS
- Suitable for temporal analysis
- Suitable for feature extraction
- Easier to validate
- Easier to compare across demonstrations
- Easier to connect with robot motion later

A learned latent representation can be introduced later if experiments
show that the structured representation is insufficient.

---

## 11. Human-to-Robot Consideration

The final research objective is not to transfer human joint trajectories
directly to the Unitree H1.

Therefore, the representation should distinguish between:

### Human-specific representation

    Human joint coordinates
    Human morphology
    Human kinematics

and:

### Behavioral information

    Movement patterns
    Task-related behavior
    Temporal structure
    Contact behavior
    Locomotion characteristics

The later objective-learning stage will investigate which information can
be transformed into a robot-compatible objective.

---

## 12. Representation vs. Objective

An important distinction is maintained:

    Motion Representation
            ≠
    Human Objective

The motion representation describes:

    "What did the human do?"

The objective attempts to explain:

    "What behavioral preference could explain why
     the human moved this way?"

Therefore:

    Human Motion
         ↓
    Representation
         ↓
    Objective Inference

The representation is evidence used for objective inference, not the
objective itself.

---

## 13. Output Format

Processed motion should be stored in a structured format containing at
least:

    positions
    velocity
    acceleration
    timestamps / FPS

Additional fields may include:

    root_motion
    contacts
    metadata

Example:

    motion.npz

    ├── positions
    ├── velocity
    ├── acceleration
    ├── root_motion
    ├── contacts
    ├── fps
    └── metadata

The exact storage format may be adjusted during implementation.

---

## 14. Validation Requirements

Before using the representation for objective learning, we must verify:

1. Joint dimensions are correct.
2. Temporal ordering is preserved.
3. No unexpected discontinuities exist.
4. Coordinate normalization is consistent.
5. Velocity and acceleration are numerically stable.
6. Contact detection is reasonable where used.
7. Different motion sequences can be represented consistently.

Validation results should be stored in:

    results/
        statistics/
        visualizations/

---

## 15. Initial Decision

For the initial experiments, the project will use a structured temporal
representation based primarily on:

    3D Joint Positions
          +
    Root Motion
          +
    Velocity
          +
    Acceleration
          +
    Contact Information

This representation is sufficient to begin feature extraction and motion
segmentation without committing to a specific neural architecture.

---

## 16. Next Step

The next stage is:

    04_feature_extraction.md

The goal is to determine which measurable quantities can be extracted
from the motion representation and may later serve as candidate variables
for human objective inference.

The important distinction is:

    Motion Representation
            ↓
    Extract Measurable Quantities
            ↓
    Test Candidate Explanations
            ↓
    Infer Human Objective

No final objective is assumed at this stage.

---

## Status

Motion representation:

**Defined**

Primary representation:

**Temporal 3D joint motion**

Additional information:

**Root motion, velocity, acceleration, and contact information**

Final human objective:

**Not yet determined**

Next step:

**Feature extraction**
