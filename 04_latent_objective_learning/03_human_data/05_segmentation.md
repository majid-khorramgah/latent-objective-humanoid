# Motion Segmentation

## 1. Purpose

The purpose of this stage is to divide continuous human motion
sequences into meaningful and comparable motion segments.

The goal is NOT to infer the human objective at this stage.

Instead:

    Continuous Human Motion
            ↓
      Motion Segmentation
            ↓
      Meaningful Segments
            ↓
    Segment-Level Features
            ↓
      Objective Analysis

Segmentation provides a consistent unit of analysis for comparing
different human demonstrations.

---

## 2. Why Segmentation Is Necessary

AMASS contains continuous motion sequences that may contain multiple
movement phases or behaviors.

For example:

    Walking Sequence

    ├── Start
    ├── Walking
    ├── Turning
    ├── Walking
    └── Stop

Treating the entire sequence as one sample may hide important changes
in movement behavior.

Therefore, the motion should be divided into segments that can be
analyzed independently.

---

## 3. Segmentation Unit

The initial unit of analysis will be a motion segment.

A segment is defined as:

> A temporally continuous portion of a human motion sequence that
> represents a relatively consistent movement behavior or locomotion
> phase.

For a sequence:

    X = {x_1, x_2, ..., x_T}

segmentation produces:

    S_1, S_2, ..., S_N

where each segment contains a subset of consecutive frames.

---

## 4. Initial Segmentation Strategy

The first implementation should use a simple and reproducible
segmentation strategy.

The initial strategy is based primarily on:

- Motion continuity
- Locomotion state
- Foot contact patterns
- Changes in movement direction
- Changes in motion characteristics

The project should avoid introducing a complex learned segmentation
model before establishing a reliable baseline.

---

## 5. Locomotion-Based Segmentation

For the initial experiments, walking-related sequences should be
identified and separated from unrelated motion whenever possible.

Possible motion states include:

    Standing
       ↓
    Walking
       ↓
    Turning
       ↓
    Walking
       ↓
    Stopping

Only segments relevant to the research question should be retained for
the initial locomotion experiments.

---

## 6. Contact-Based Segmentation

Foot-ground contact information can provide useful temporal structure.

A foot contact signal can be represented as:

    c_foot(t) ∈ {0,1}

where:

    1 → contact
    0 → non-contact

Transitions in foot contact can help identify:

- Stance phases
- Swing phases
- Step boundaries
- Double-support phases
- Single-support phases

These signals should be treated as segmentation evidence rather than
as direct evidence of a human objective.

---

## 7. Step-Level Segmentation

For locomotion experiments, individual steps may provide a useful
fine-grained unit.

A simplified structure is:

    Step

    ├── Foot contact
    ├── Stance
    ├── Foot release
    ├── Swing
    └── Next contact

A step can therefore be represented as:

    S_k = [t_start, t_end]

where:

- t_start = beginning of the step
- t_end = end of the step

Step-level segmentation can later allow comparison of movement
strategies across different demonstrations.

---

## 8. Stride-Level Segmentation

A larger temporal unit may also be useful.

A stride can be defined approximately as the interval between two
successive contacts of the same foot.

For example:

    Left Foot Contact
            ↓
       One Stride
            ↓
    Left Foot Contact

Stride-level segments may provide a more stable unit for comparing
locomotion patterns than individual frames.

The appropriate unit will be determined experimentally.

---

## 9. Change-Based Segmentation

In addition to contact information, significant changes in motion may
indicate segment boundaries.

Possible signals include:

- Root velocity
- Root acceleration
- Body orientation
- Joint velocity
- Joint acceleration
- Movement direction

For example:

    Stable Forward Motion
            ↓
      Direction Change
            ↓
          Turning
            ↓
      Stable Forward Motion

A significant change may therefore define a new segment.

---

## 10. Segment Quality Requirements

Each segment should satisfy basic quality requirements.

A valid segment should have:

- Sufficient temporal duration
- No missing frames
- Consistent FPS
- Valid joint coordinates
- Reasonable motion continuity
- Valid feature values

Very short or corrupted segments should be excluded from the initial
dataset.

---

## 11. Minimum Segment Duration

The exact minimum duration should be determined based on the intended
analysis.

For initial experiments, segments should be long enough to contain
meaningful temporal motion information.

For example:

    Very short segment
        ↓
    Insufficient movement information
        ↓
    Exclude

while:

    Sufficiently long segment
        ↓
    Meaningful temporal behavior
        ↓
    Retain

The exact threshold should be recorded in the experiment configuration
rather than hard-coded into the research definition.

---

## 12. Segment-Level Features

After segmentation, the features extracted in:

    04_feature_extraction.md

can be associated with each segment.

For example:

    Segment S_k

    ├── Joint positions
    ├── Joint velocity
    ├── Joint acceleration
    ├── Root motion
    ├── Contact information
    └── Temporal features

This creates a segment-level representation:

    R(S_k)

which can later be used for objective analysis.

---

## 13. Segment Metadata

Each segment should contain metadata describing how it was created.

Example:

    segment_id
    source_dataset
    sequence_id
    start_frame
    end_frame
    duration
    fps
    segmentation_method

For locomotion segments, additional information may include:

    dominant_direction
    left_foot_contact
    right_foot_contact
    step_count

---

## 14. Avoiding Objective Leakage

Segmentation must not use the final human objective as an input.

For example, we should NOT define segments using:

    "lowest energy movement"

or:

    "most stable movement"

because this would assume the answer before objective inference.

Instead, segmentation should rely on observable motion properties:

    Motion
      ↓
    Contacts
      ↓
    Kinematics
      ↓
    Temporal Changes
      ↓
    Segments

This keeps the segmentation stage independent from objective learning.

---

## 15. Segment Consistency

Segments should be comparable across demonstrations.

For example:

    Demonstration A

        Step 1
        Step 2
        Step 3

    Demonstration B

        Step 1
        Step 2
        Step 3

The segmentation procedure should use the same rules for both
demonstrations.

This is important because later objective analysis will compare
different segments.

---

## 16. Segmentation Across Datasets

Different AMASS subsets may have different:

- Motion capture systems
- FPS
- Motion styles
- Recording conventions
- Available annotations

Therefore, segmentation should be applied after preprocessing and
normalization.

The procedure should remain consistent while allowing dataset-specific
quality checks.

---

## 17. Initial Segmentation Pipeline

The initial implementation follows:

    Raw AMASS
        ↓
    SMPL-X Reconstruction
        ↓
    Joint Representation
        ↓
    Feature Extraction
        ↓
    Contact Detection
        ↓
    Motion State Analysis
        ↓
    Segment Detection
        ↓
    Segment Validation
        ↓
    Segment Dataset

---

## 18. Segment Types

The initial dataset may contain several segment types.

### Locomotion Segment

Continuous walking or locomotion behavior.

### Step Segment

One step cycle or equivalent temporal unit.

### Stride Segment

A complete stride cycle.

### Transition Segment

A transition between movement states.

For the first experiments, the project should prioritize locomotion
segments and avoid unnecessary complexity.

---

## 19. Segment Representation

Each segment should preserve the original temporal structure.

For example:

    Segment S_k

    positions:
        T_k × J × 3

    velocity:
        T_k × J × 3

    acceleration:
        T_k × J × 3

    contacts:
        T_k × N_feet

where:

- T_k = number of frames in the segment
- J = number of joints
- N_feet = number of tracked feet

---

## 20. Segment Normalization

Segments may have different lengths.

Possible approaches include:

- Preserve original duration
- Temporal resampling
- Phase normalization
- Fixed-length windows

The initial implementation should preserve the original temporal
information whenever possible.

If fixed-length representations are required by a later learning
algorithm, temporal normalization can be introduced at that stage.

---

## 21. Visualization

Segmentation must be visually validated.

For selected sequences, the system should visualize:

- Original motion
- Detected segment boundaries
- Foot contacts
- Root trajectory
- Motion states

Example:

    Full Motion

    |---------|---------|---------|
       Walk      Turn      Walk

The purpose is to verify that the automatic segmentation corresponds
to meaningful changes in the observed motion.

---

## 22. Segmentation Validation

The segmentation procedure should be evaluated using:

### Boundary Quality

Are detected boundaries located near meaningful motion transitions?

### Temporal Consistency

Are segments continuous and free of unexpected gaps?

### Motion Consistency

Does each segment represent a reasonably consistent movement phase?

### Reproducibility

Does the same algorithm produce the same result when applied again?

---

## 23. Initial Implementation

The first implementation should prioritize:

1. Foot contact detection.
2. Step / stride boundary detection.
3. Basic motion-state segmentation.
4. Segment validation.
5. Segment-level feature generation.

A learned segmentation model is not required initially.

If later experiments show that rule-based segmentation is insufficient,
a learned or probabilistic segmentation method can be investigated.

---

## 24. Expected Output

The segmentation stage should generate:

    data/
        processed/
            segments/

and optionally:

    results/
        visualizations/
            segmentation/

Each segment should contain:

    motion data
    extracted features
    contact information
    metadata

Example:

    segment_00001.npz
    segment_00002.npz
    segment_00003.npz

---

## 25. Relationship to Objective Inference

Segmentation does not determine the human objective.

Instead, it creates comparable behavioral units.

The research pipeline becomes:

    Human Demonstrations
            ↓
    Motion Representation
            ↓
    Feature Extraction
            ↓
    Motion Segmentation
            ↓
    Comparable Motion Segments
            ↓
    Objective Inference
            ↓
    Human Objective

This separation is important for maintaining a clean experimental
design.

---

## 26. Research Question Enabled by Segmentation

After segmentation, we can begin asking:

> Do different human motion segments that accomplish similar locomotion
> tasks exhibit systematic differences in measurable movement
> properties?

This is an important step toward objective inference.

For example:

    Same Task
       +
    Different Demonstrations
       ↓
    Different Movement Strategies
       ↓
    Different Feature Patterns
       ↓
    Candidate Behavioral Explanation

The objective is not assumed in advance.

---

## 27. Limitations

AMASS does not necessarily provide explicit labels for:

- Human intention
- Behavioral preference
- Task success
- Environmental difficulty
- Subjective comfort
- Internal decision-making

Therefore, segmentation alone cannot determine whether a particular
movement pattern is preferred by the human.

It only creates structured motion samples for further analysis.

---

## 28. Initial Research Decision

The project will initially use a simple, interpretable and reproducible
segmentation strategy based on:

    Foot Contacts
          +
    Temporal Structure
          +
    Motion Changes
          +
    Locomotion State

The segmentation method will remain independent from the final
objective-learning method.

More sophisticated segmentation approaches may be introduced only if
the initial approach proves insufficient.

---

## 29. Next Step

The next stage is:

    06_dataset_split.md

The purpose is to define how motion segments are divided into training,
validation, and held-out evaluation sets.

The split must prevent information leakage between related motion
sequences and must support meaningful evaluation of objective inference.

The resulting pipeline is:

    AMASS
      ↓
    Preprocessing
      ↓
    Motion Representation
      ↓
    Feature Extraction
      ↓
    Segmentation
      ↓
    Dataset Split
      ↓
    Objective Learning
