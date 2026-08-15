# Feature Extraction

## 1. Purpose

The purpose of this stage is to extract measurable quantities from the
human motion representation that can later be evaluated as candidate
variables for human objective inference.

The goal is NOT to define the final human objective.

Instead:

    Human Motion Representation
            ↓
    Measurable Motion Features
            ↓
    Candidate Objective Variables
            ↓
    Objective Inference
            ↓
    Experimental Validation

The extracted features should describe properties of human movement while
remaining as independent from any predefined objective as possible.

---

## 2. Input

The input to this stage is the structured human motion representation
defined in:

    03_motion_representation.md

The primary inputs are:

- 3D joint positions
- Root motion
- Joint velocities
- Joint accelerations
- Contact information
- Temporal information / FPS

Example:

    positions
    velocity
    acceleration
    root_motion
    contacts
    fps

---

## 3. Feature Categories

The initial feature extraction will consider several categories.

These categories are candidate measurements, NOT predefined components
of the final human objective.

### 3.1 Task / Locomotion Features

Possible measurements include:

- Root displacement
- Forward velocity
- Walking speed
- Direction of movement
- Step length
- Step timing
- Locomotion duration

These features describe what the person is trying to accomplish at the
behavioral level.

---

### 3.2 Kinematic Features

Kinematic features describe the configuration and movement of the body.

Possible measurements include:

- Joint positions
- Joint velocities
- Joint accelerations
- Joint ranges of motion
- Relative joint motion
- Body orientation
- Root orientation

These features describe how the movement is physically performed.

---

### 3.3 Temporal Features

Human movement is strongly dependent on temporal structure.

Possible measurements include:

- Motion duration
- Step duration
- Cadence
- Stride period
- Phase duration
- Velocity profiles
- Acceleration profiles

Temporal features may help distinguish different movement strategies
that achieve the same task.

---

### 3.4 Contact Features

Contact information is extracted primarily from the feet.

Possible measurements include:

- Contact duration
- Swing duration
- Contact timing
- Step timing
- Foot-ground transitions
- Double-support duration
- Single-support duration

These measurements provide information about locomotion structure and
interaction with the ground.

---

### 3.5 Whole-Body Motion Features

Additional features may describe movement at the body level.

Possible measurements include:

- Center-of-mass trajectory
- Center-of-mass velocity
- Center-of-mass acceleration
- Body orientation
- Whole-body displacement
- Whole-body motion magnitude

These features may be useful when studying movement strategies that are
not visible from individual joints alone.

---

## 4. Feature Computation

Features should be computed directly from the processed motion data.

For a joint position:

    p_j(t)

velocity can be approximated as:

    v_j(t) =
        [p_j(t) - p_j(t-1)] / Δt

Acceleration can be approximated as:

    a_j(t) =
        [v_j(t) - v_j(t-1)] / Δt

where:

    Δt = 1 / FPS

These quantities provide temporal information about the movement.

---

## 5. Sequence-Level Features

Not every feature needs to remain a time series.

For objective analysis, some features can be summarized over a complete
motion segment.

For example:

    Mean velocity
    Maximum velocity
    Mean acceleration
    Maximum acceleration
    Motion duration
    Step frequency
    Contact duration

Therefore, two representations may be retained:

### Frame-Level Representation

    feature(t)

Useful for:

- Temporal analysis
- Motion segmentation
- Phase analysis

### Sequence-Level Representation

    Feature(sequence)

Useful for:

- Comparing demonstrations
- Statistical analysis
- Objective inference
- Dataset construction

---

## 6. Candidate Behavioral Variables

The purpose of feature extraction is to create measurable variables that
could potentially explain differences between human demonstrations.

For example:

    Demonstration A
        ↓
    Feature Vector A

    Demonstration B
        ↓
    Feature Vector B

The resulting feature vectors can be compared across demonstrations.

This allows us to investigate questions such as:

- Which movement properties remain consistent?
- Which properties change across demonstrations?
- Which properties correlate with task conditions?
- Which properties differ between successful and unsuccessful behavior?
- Which properties may explain different movement strategies?

No feature is assumed to represent the human objective automatically.

---

## 7. Objective Features vs. Descriptive Features

An important distinction is maintained.

### Descriptive Feature

A feature simply describes the observed movement.

For example:

    Walking speed = 1.2 m/s

### Candidate Objective Variable

A feature may become relevant to objective inference if differences in
that quantity help explain why one movement is preferred over another.

For example:

    Demonstration A → lower effort
    Demonstration B → higher effort

If both achieve the same task, effort may become a candidate explanatory
variable.

Therefore:

    Feature
       ↓
    Evidence
       ↓
    Candidate Objective Variable

A feature is NOT considered an objective merely because it can be
computed.

---

## 8. Avoiding a Predefined Human Objective

The project must avoid assuming:

    Objective =
    Energy
    +
    Stability
    +
    Smoothness
    +
    Robustness

Instead, the procedure is:

    Extract Candidate Features
              ↓
       Analyze Demonstrations
              ↓
       Identify Variations
              ↓
       Test Explanatory Power
              ↓
       Infer Objective

The extracted features therefore form a candidate measurement space,
not the final cost function.

---

## 9. Feature Normalization

Different features may have very different numerical scales.

For example:

    Position       → meters
    Velocity       → meters / second
    Acceleration   → meters / second²
    Contact        → binary

Before statistical comparison or learning, appropriate normalization
should be applied.

Possible approaches include:

- Dataset-level standardization
- Per-feature normalization
- Robust scaling

The normalization method must be recorded so that it can be reproduced
for validation and held-out evaluation.

---

## 10. Feature Quality Checks

Each extracted feature should be checked for:

### Numerical validity

- Missing values
- NaN values
- Infinite values
- Unexpected magnitudes

### Temporal validity

- Correct sequence length
- Consistent FPS
- No unexpected discontinuities

### Physical plausibility

- Reasonable joint velocities
- Reasonable accelerations
- Consistent contact signals

### Dataset consistency

- Same feature definition across datasets
- Same coordinate convention
- Same units
- Same normalization procedure

---

## 11. Feature Redundancy

Human motion features may be strongly correlated.

For example:

    Joint Position
          ↕
    Joint Velocity
          ↕
    Joint Acceleration

Similarly:

    Step Duration
          ↕
    Cadence

Therefore, feature correlations should be analyzed before using all
features simultaneously in objective inference.

Possible analyses include:

- Correlation matrices
- Feature variance
- Feature distributions
- Principal component analysis
- Redundancy analysis

Dimensionality reduction should be used as an analysis tool initially,
not assumed to be the final objective representation.

---

## 12. Feature Selection

Feature selection should be driven by the research question rather than
by convenience.

The initial candidate set should be broad enough to avoid prematurely
excluding potentially relevant information.

Later, features may be:

    Retained
    Removed
    Combined
    Reparameterized

based on:

- Statistical evidence
- Predictive value
- Interpretability
- Transferability
- Experimental validation

---

## 13. Relationship to Objective Learning

The complete logic is:

    AMASS
      ↓
    Human Motion
      ↓
    Motion Representation
      ↓
    Feature Extraction
      ↓
    Candidate Feature Space
      ↓
    Objective Inference
      ↓
    Human Objective
      ↓
    H1 Transfer

The critical point is that the feature extraction stage does not perform
objective inference.

It prepares the measurable information required by the next stages.

---

## 14. Initial Feature Set

For the first implementation, the following feature groups should be
available:

### Motion

- 3D joint positions
- Joint velocities
- Joint accelerations

### Locomotion

- Root displacement
- Root velocity
- Walking speed
- Direction of motion

### Temporal

- Motion duration
- Step timing
- Cadence / stride timing where detectable

### Contact

- Foot contact state
- Contact duration
- Swing duration

### Body-Level

- Center-of-mass trajectory where reliably available
- Center-of-mass velocity
- Body orientation

These are initial measurable variables.

They are NOT the final objective components.

---

## 15. Data Storage

Extracted features should be stored in a structured format.

Example:

    processed/

    └── features/

        ├── CMU/
        ├── KIT/
        ├── ACCAD/
        └── ...

A feature file may contain:

    positions
    velocity
    acceleration
    root_motion
    contacts
    locomotion_features
    temporal_features
    body_features
    metadata

Metadata should include at least:

    dataset
    sequence_id
    FPS
    coordinate_system
    normalization
    feature_version

---

## 16. Visualization

Feature distributions should be visualized before objective learning.

Useful visualizations include:

- Velocity profiles
- Acceleration profiles
- Root velocity
- Step timing
- Contact patterns
- Feature distributions
- Feature correlations

Example:

    Human Demonstrations
            ↓
       Feature Analysis
            ↓
      Visual Inspection
            ↓
      Statistical Analysis

These visualizations help identify data problems and understand the
structure of the human demonstrations.

---

## 17. What We Are Actually Trying to Discover

The central question is not:

> Which predefined feature is the human objective?

Instead, the question is:

> **Which measurable properties of human motion provide evidence for
> an underlying behavioral objective that can explain differences
> between human demonstrations?**

This distinction is important because the project is investigating
objective inference rather than simply calculating known movement
metrics.

---

## 18. Connection to AMASS

AMASS provides motion demonstrations but does not directly provide the
human objective behind each motion.

Therefore:

    AMASS
      ↓
    Observed Motion
      ↓
    Extract Measurable Properties
      ↓
    Search for Behavioral Structure
      ↓
    Infer Candidate Objective

The absence of explicit objective labels is an important characteristic
of the problem.

The objective must therefore be inferred indirectly from the observed
motion and its context.

---

## 19. Limitations

AMASS motion capture data does not necessarily provide all information
required to identify a human objective.

In particular, the dataset may not directly provide:

- Human subjective preferences
- Explicit task goals
- Environmental context
- Internal decision-making
- Human-perceived comfort
- Explicit success/failure labels

Therefore, feature extraction alone cannot prove what the human intended.

This limitation must be considered during objective inference and
validation.

---

## 20. Initial Research Decision

The project will initially construct a broad, interpretable feature
space from the available human motion data.

We will not commit to a final objective before evaluating the extracted
features.

The process is:

    Human Motion
          ↓
    Feature Space
          ↓
    Candidate Explanations
          ↓
    Objective Inference
          ↓
    Validation

If the initial feature space is insufficient, additional representations
or learned features may be investigated later.

---

## 21. Next Step

The next stage is:

    05_segmentation.md

The purpose is to divide continuous human motion into meaningful
motion segments that can be compared consistently across demonstrations.

The segmentation stage will provide:

    Continuous Motion
          ↓
    Motion Segments
          ↓
    Segment-Level Features
          ↓
    Objective Analysis

---

## Status

Feature extraction:

**Defined**

Initial feature space:

**Structured and interpretable**

Final objective:

**Not established**

Objective inference:

**Not performed yet**

Next step:

**Motion segmentation**
