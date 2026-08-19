# Stage 04 — Human Motion Normalization

**Project:** Latent Objective Humanoid  
**Pipeline:** Human Data Processing  
**Stage:** 04 — Motion Normalization  
**Script:** `04_normalize_motion.py`  
**Canonical Representation:** SMPL-X 127 Joints  
**Status:** Completed  
**Video:** https://youtu.be/Gka6i7_VcUs

---

# 1. Purpose

Stage 04 converts the canonical SMPL-X 127-joint motion representation from Stage 03 into a normalized representation suitable for later processing and learning stages.

The central design is:

    Local Body Motion
        +
    Preserved Global Root Motion

The canonical representation is not reduced.

The input:

    full
    [T,127,3]

is transformed into:

    full
    [T,127,3]

where `full` becomes a root-centered, sequence-level body-scale-normalized representation.

At the same time, the original root trajectory and several global-motion representations are explicitly preserved.

The transformation is deterministic and does not use a learned model.

---

# 2. What This Stage Actually Does

For every input NPZ:

1. Load the canonical `full` tensor.
2. Validate that it has shape `[T,127,3]`.
3. Extract root joint index `0`.
4. Root-center the complete motion.
5. Compute one body scale for the entire sequence.
6. Normalize the root-centered local motion.
7. Compute global root-motion features.
8. Reconstruct the original motion.
9. Measure reconstruction error.
10. Reject the file if reconstruction error exceeds `1e-4`.
11. Preserve the Stage 03 derived representations unchanged.
12. Save the normalized NPZ.
13. Record processing information in `_normalization_summary.json`.

---

# 3. Input

Default input root:

    data/processed/joints/

The script recursively searches for:

    *.npz

using:

    input_root.rglob("*.npz")

The input directory hierarchy is preserved in the output.

For example:

    data/processed/joints/ACCAD/Female1General_c3d/A1 - Stand_poses.npz

becomes:

    data/processed/normalized/ACCAD/Female1General_c3d/A1 - Stand_poses.npz

---

# 4. Output

Default output root:

    data/processed/normalized/

The relative path of every input NPZ is preserved.

A processing summary is also written to:

    data/processed/normalized/_normalization_summary.json

---

# 5. Canonical Representation

The script explicitly defines:

    CANONICAL_KEY = "full"

    CANONICAL_JOINT_COUNT = 127

    COORD_DIM = 3

Therefore the required canonical tensor is:

    full
    [T,127,3]

The script does not attempt to guess which tensor is canonical.

If `full` is missing, processing fails.

This is important because the input NPZ may contain multiple representations such as:

    full
    body_core
    body_contact
    hands
    face

Only `full` is treated as the canonical SMPL-X tensor.

---

# 6. Canonical Tensor Validation

Before normalization, `full` is validated.

The following conditions are required:

    1. It must be a NumPy array.
    2. It must have exactly 3 dimensions.
    3. Dimension 1 must contain 127 joints.
    4. Dimension 2 must contain 3 coordinates.
    5. The sequence must contain at least one frame.
    6. It must contain no NaN values.
    7. It must contain no Inf values.

Required shape:

    [T,127,3]

If any condition fails, that file is marked as failed.

---

# 7. Root Joint

The script explicitly defines:

    ROOT_JOINT_INDEX = 0

Therefore the root is always:

    joints[:,0,:]

The extracted root positions have shape:

    [T,3]

They are stored as:

    root_positions

---

# 8. Original Root Positions

The function:

    compute_root_positions()

extracts:

    joints[:,0,:]

and converts the result to `float32`.

The important property is that these values are not modified.

Therefore:

    root_positions

contains the original global root/pelvis trajectory from the input `full` tensor.

It is not centered.

It is not scale-normalized.

It remains in the original dataset coordinate system.

---

# 9. Root-Centering

The local normalization starts by subtracting the root position from every joint in every frame.

Conceptually:

    root_positions[t] = joints[t,0]

and:

    centered[t,j] =
        joints[t,j] - root_positions[t]

The resulting tensor is still:

    [T,127,3]

The root of every frame becomes:

    [0,0,0]

because the root position has been subtracted from itself.

---

# 10. Local Representation

After root-centering, the script computes one body scale for the entire sequence.

Then:

    normalized =
        centered / body_scale

The normalized tensor is stored as:

    full

Therefore the output `full` means:

    root-centered
    +
    sequence-level body-scale normalized
    +
    SMPL-X 127 joints

It is the primary local-motion representation produced by Stage 04.

---

# 11. Exact Body Scale Definition

The code computes:

    distances = norm(centered_joints, axis=-1)

Then:

    body_scale = max(distances)

Therefore:

    body_scale =
        maximum distance of any centered joint
        across the complete sequence

This produces exactly one scalar for the entire motion sequence.

It is not computed independently per frame.

It is not computed independently per joint.

It is not a learned parameter.

---

# 12. Sequence-Level Scaling

The body scale is deliberately sequence-level.

For example, if a sequence has:

    T = 1000

frames, there is still only:

    one body_scale

for all 1000 frames.

The script does not perform:

    frame 1 -> scale 1
    frame 2 -> scale 2
    frame 3 -> scale 3

Instead:

    entire sequence -> one scalar

This preserves temporal scale consistency.

---

# 13. Exact Local Normalization Formula

The complete local transformation is:

    root_positions[t] = joints[t,0]

    centered[t,j] =
        joints[t,j] - root_positions[t]

    body_scale =
        max(norm(centered))

    full[t,j] =
        centered[t,j] / body_scale

Therefore:

    full =
        (original - root_position) / body_scale

with broadcasting over the joint dimension.

---

# 14. What Happens to the Root in `full`

Because:

    centered[t,0] =
        joints[t,0] - joints[t,0]

the root joint in normalized `full` is:

    [0,0,0]

for every frame.

Therefore the global translation of the root is intentionally removed from `full`.

This is not considered loss of global motion because the root trajectory is stored separately.

---

# 15. Global Motion Is Preserved Separately

The script explicitly computes global root-motion features.

These are:

    root_positions
    root_positions_normalized
    root_displacement
    root_displacement_normalized
    root_velocity
    root_velocity_normalized

Therefore the output separates:

    Local body motion

from:

    Global root motion

---

# 16. `root_positions`

Key:

    root_positions

Shape:

    [T,3]

Meaning:

    Original global root trajectory.

It is directly extracted from:

    joints[:,0,:]

No initial-offset removal is applied.

No body-scale normalization is applied.

---

# 17. `root_displacement`

Key:

    root_displacement

Shape:

    [T,3]

Definition:

    root_displacement[t] =
        root_positions[t] - root_positions[0]

Therefore:

    root_displacement[0] =
        [0,0,0]

This removes only the arbitrary initial global offset.

The movement occurring after the first frame remains.

It can represent:

    forward motion
    backward motion
    left/right motion
    vertical movement
    rising/falling
    jumping
    other root translation

---

# 18. `root_positions_normalized`

Key:

    root_positions_normalized

Shape:

    [T,3]

Important:

Despite its name, this is not the original root position simply divided by scale.

The implementation is:

    root_positions_normalized =
        root_displacement / body_scale

Therefore the initial root position is first removed.

At frame 0:

    root_positions_normalized[0] =
        [0,0,0]

The representation is therefore:

    initial-offset removed
    +
    sequence body-scale normalized

---

# 19. `root_displacement_normalized`

Key:

    root_displacement_normalized

Shape:

    [T,3]

Definition:

    root_displacement_normalized =
        root_displacement / body_scale

Therefore, in the current implementation:

    root_displacement_normalized
        ==
    root_positions_normalized

numerically, because both are computed from the same displacement and the same body scale.

Both are nevertheless saved explicitly under separate keys.

---

# 20. `root_velocity`

Key:

    root_velocity

Shape:

    [T,3]

The implementation computes frame-to-frame root displacement:

    root_velocity[t] =
        root_positions[t]
        - root_positions[t-1]

The first frame is explicitly initialized as:

    root_velocity[0] =
        [0,0,0]

Therefore this tensor represents:

    displacement per frame

It is not physical velocity in meters/second.

---

# 21. Root Velocity Units

The script explicitly stores the metadata:

    root_velocity_unit =
        dataset_units_per_frame

This means the interpretation is:

    dataset coordinate units / frame

The script does not know FPS.

It does not convert the values to:

    meters/second

Therefore the term `velocity` in this stage should be understood as frame-to-frame root displacement.

---

# 22. `root_velocity_normalized`

Key:

    root_velocity_normalized

Shape:

    [T,3]

Definition:

    root_velocity_normalized =
        root_velocity / body_scale

Therefore this represents frame-to-frame root displacement after sequence body-scale normalization.

Its units are effectively:

    normalized dataset units / frame

with the normalization determined by `body_scale`.

---

# 23. Complete Global Feature Set

The exact global feature dictionary generated by the code is:

    root_positions
    root_positions_normalized
    root_displacement
    root_displacement_normalized
    root_velocity
    root_velocity_normalized

All six are saved into every successfully processed NPZ.

---

# 24. Complete Output NPZ Structure

A successful normalized NPZ contains the following categories.

## Main local representation

    full

## Global root motion

    root_positions
    root_positions_normalized
    root_displacement
    root_displacement_normalized
    root_velocity
    root_velocity_normalized

## Scale

    body_scale

## Metadata

    source
    representation
    normalization
    root_joint_index
    global_motion
    root_velocity_unit

## Reconstruction metrics

    reconstruction_max_abs_error
    reconstruction_mean_abs_error
    reconstruction_rmse

## Preserved Stage 03 representations

    body_core
    body_contact
    hands
    face

The last four are included only if they existed in the input NPZ.

---

# 25. Derived Representations

The script defines:

    DERIVED_KEYS = (
        "body_core",
        "body_contact",
        "hands",
        "face",
    )

These tensors are loaded from the input.

The code does not normalize them.

It does not root-center them.

It does not divide them by `body_scale`.

It simply preserves them and writes them into the output NPZ.

Therefore their values remain exactly as supplied by Stage 03.

This is an important distinction:

    `full`
        -> normalized by Stage 04

    body_core
    body_contact
    hands
    face
        -> preserved unchanged

---

# 26. `body_scale`

Key:

    body_scale

Type:

    float32 scalar

Meaning:

    Sequence-level maximum centered-joint distance

This scalar is required to reconstruct the original `full` representation.

---

# 27. Metadata: `source`

Key:

    source

Meaning:

    Original input file path

It provides traceability between the normalized file and the source NPZ.

---

# 28. Metadata: `representation`

Key:

    representation

Value:

    smplx_127

This explicitly identifies the canonical representation.

---

# 29. Metadata: `normalization`

Key:

    normalization

Value:

    local_root_centered_sequence_body_scale

This records the exact normalization convention used by the script.

---

# 30. Metadata: `root_joint_index`

Key:

    root_joint_index

Value:

    0

This explicitly records which canonical joint was treated as the root.

---

# 31. Metadata: `global_motion`

Key:

    global_motion

Value:

    preserved

This records that global root motion was intentionally retained.

---

# 32. Metadata: `root_velocity_unit`

Key:

    root_velocity_unit

Value:

    dataset_units_per_frame

This prevents later stages from incorrectly interpreting `root_velocity` as physical velocity.

---

# 33. Reconstruction

One of the most important parts of Stage 04 is that the transformation is reversible.

The local normalization is:

    full =
        (original - root_position) / body_scale

Therefore the original motion can be reconstructed as:

    reconstructed =
        full * body_scale
        + root_positions

More explicitly:

    reconstructed[t,j] =
        full[t,j] * body_scale
        + root_positions[t]

---

# 34. Reconstruction Error

After normalization, the script reconstructs the original motion.

It then computes three metrics:

    max_abs_error
    mean_abs_error
    rmse

The difference is calculated between:

    reconstructed

and:

    original

using float64 for the error calculation.

---

# 35. Reconstruction Safety Threshold

The script has an explicit safety check:

    max_abs_error <= 1e-4

If:

    max_abs_error > 1e-4

the file fails processing.

Therefore reconstruction is not merely logged.

It is an actual validity condition for the output.

---

# 36. Reconstruction Metrics Saved in NPZ

The following keys are written into every successful output:

    reconstruction_max_abs_error

    reconstruction_mean_abs_error

    reconstruction_rmse

Therefore the output file itself contains evidence of reconstruction quality.

---

# 37. What Reconstruction Proves

The reconstruction check verifies that:

    normalized local representation
    +
    body scale
    +
    original root trajectory

are sufficient to reconstruct the original canonical motion within the defined numerical tolerance.

The important relationship is:

    original ≈ full * body_scale + root_positions

---

# 38. No Canonical Information Reduction

The script explicitly reports:

    Canonical joint information will NOT be reduced.

The output remains:

    [T,127,3]

There is no transformation such as:

    127 -> 22

inside Stage 04.

The canonical SMPL-X 127 representation is retained.

---

# 39. Temporal Dimension

The script does not perform temporal resampling.

It does not:

    crop frames
    remove frames
    interpolate frames
    reorder frames
    downsample frames

Therefore:

    input T
        ==
    output T

For example:

    [2399,127,3]

remains:

    [2399,127,3]

---

# 40. No Learned Model

Stage 04 does not train or execute a neural network.

There is:

    no encoder
    no decoder
    no latent model
    no optimizer
    no training loop
    no learned normalization

Everything is deterministic NumPy-based preprocessing.

---

# 41. Data Flow

The exact conceptual flow is:

    Input NPZ
        |
        v
    Read `full`
        |
        v
    Validate [T,127,3]
        |
        v
    Extract joint 0
        |
        +------------------------------+
        |                              |
        v                              v
    root_positions              Root-center motion
        |                              |
        |                              v
        |                       Compute body_scale
        |                              |
        |                              v
        |                       Normalize `full`
        |                              |
        |                              v
        |                         normalized full
        |
        +--> root_displacement
        |
        +--> root_positions_normalized
        |
        +--> root_velocity
        |
        +--> root_velocity_normalized
        |
        +--> root_displacement_normalized
        |
        v
    Reconstruction
        |
        v
    Error calculation
        |
        v
    Safety threshold
        |
        v
    Preserve Stage 03 derived tensors
        |
        v
    Save normalized NPZ

---

# 42. Local vs Global

The fundamental separation is:

    LOCAL

    full

versus:

    GLOBAL

    root_positions
    root_positions_normalized
    root_displacement
    root_displacement_normalized
    root_velocity
    root_velocity_normalized

This allows later stages to decide whether they need local body motion, global locomotion, or both.

---

# 43. Example: Walking Forward

Suppose:

    root_positions:

        frame 0 -> X = 0.0
        frame 1 -> X = 0.1
        frame 2 -> X = 0.2
        frame 3 -> X = 0.3

Then:

    root_displacement:

        0.0
        0.1
        0.2
        0.3

The local `full` representation does not contain this absolute root translation because it is root-centered.

The global information remains in the root-motion tensors.

---

# 44. Example: Starting at a Different Global Position

Suppose another sequence starts at:

    X = 100

and then moves:

    100.0
    100.1
    100.2
    100.3

Its:

    root_displacement

is still:

    0.0
    0.1
    0.2
    0.3

Therefore the arbitrary initial world offset is separated from the actual movement.

The original starting location remains available through:

    root_positions

while the offset-independent trajectory is available through:

    root_displacement

and the normalized global trajectory is available through:

    root_positions_normalized

---

# 45. Example: Standing Still

If the root does not move:

    root_positions[t]
        ≈
    root_positions[0]

then:

    root_displacement
        ≈ 0

and:

    root_velocity
        ≈ 0

while `full` still contains the root-centered body configuration.

---

# 46. Example: Jumping

A jump can involve changes in the root's global position.

Those changes remain in:

    root_displacement

and:

    root_velocity

The local body configuration remains in:

    full

Therefore the global vertical component is not removed from the overall Stage 04 representation.

---

# 47. Important Clarification About Visualization

The Python script itself does not create a visualization.

It performs:

    loading
    validation
    normalization
    global feature extraction
    reconstruction
    error checking
    NPZ saving
    JSON summary generation

Therefore any visual execution shown in the Stage 04 video should not be described as a rendering operation performed directly by `04_normalize_motion.py`.

The script itself is a preprocessing and validation script.

---

# 48. Output Path Preservation

For every input:

    input_path

the script computes its path relative to:

    input_root

and appends that relative path to:

    output_root

Therefore the dataset hierarchy is preserved.

This allows normalized samples to remain directly traceable to their original location.

---

# 49. Processing Multiple Files

The script recursively finds all NPZ files.

They are sorted before processing.

For every file:

    process_one()

is called independently.

If processing succeeds:

    processed += 1

If an exception occurs:

    failed += 1

The failed file is recorded and processing continues.

---

# 50. `--limit`

The script supports:

    --limit N

This limits the number of NPZ files processed.

For example:

    python 04_normalize_motion.py --limit 5

processes at most five files.

The option is useful for:

    debugging
    validation
    testing
    quick pipeline checks

It does not change the normalization algorithm.

---

# 51. Default Paths

If no command-line paths are supplied:

    input_root =
        project_root/data/processed/joints

    output_root =
        project_root/data/processed/normalized

The project root is derived from the script location.

---

# 52. Summary JSON

At the end of processing, the script writes:

    _normalization_summary.json

The summary includes:

    script
    project_root
    input_root
    output_root
    canonical_key
    canonical_representation
    canonical_shape
    root_joint_index
    local_normalization
    global_motion
    global_normalization
    root_velocity
    canonical_information_reduced
    reconstruction_check
    processed
    failed
    files_found
    failed_files
    results

---

# 53. Summary Configuration

The summary explicitly records:

    canonical_key:
        full

    canonical_representation:
        SMPL-X 127

    canonical_shape:
        [T,127,3]

    root_joint_index:
        0

    local_normalization:
        root-centered + sequence-level body scale

    global_motion:
        preserved

    global_normalization:
        root displacement from first frame + sequence body scale

    root_velocity:
        frame-to-frame displacement

    canonical_information_reduced:
        false

    reconstruction_check:
        true

---

# 54. Per-File Summary

For every successful file, the summary records:

    input
    output
    frames
    input_shape
    output_shape
    body_scale
    global_features
    derived_shapes
    reconstruction
    status

A successful file has:

    status:
        success

A failed file has:

    status:
        failed

and includes the error message.

---

# 55. Failure Behavior

The following can cause a file to fail:

    missing `full`
    wrong dimensionality
    wrong joint count
    wrong coordinate dimension
    zero frames
    NaN
    Inf
    invalid body scale
    reconstruction error > 1e-4
    other processing exceptions

A failed file does not stop the processing of the remaining files.

---

# 56. Exact Output Contract

A successfully processed file follows this structure:

    full
        [T,127,3]
        root-centered
        sequence-scale normalized

    root_positions
        [T,3]
        original root trajectory

    root_positions_normalized
        [T,3]
        root displacement / body scale

    root_displacement
        [T,3]
        root position relative to first frame

    root_displacement_normalized
        [T,3]
        root displacement / body scale

    root_velocity
        [T,3]
        frame-to-frame root displacement

    root_velocity_normalized
        [T,3]
        frame-to-frame displacement / body scale

    body_scale
        scalar float32

    body_core
        preserved from Stage 03 if present

    body_contact
        preserved from Stage 03 if present

    hands
        preserved from Stage 03 if present

    face
        preserved from Stage 03 if present

    metadata
        source
        representation
        normalization
        root_joint_index
        global_motion
        root_velocity_unit

    reconstruction metrics
        reconstruction_max_abs_error
        reconstruction_mean_abs_error
        reconstruction_rmse

---

# 57. What Is Actually Normalized?

Only the following are directly transformed by the local normalization step:

    full

The transformation is:

    root-center
    +
    divide by sequence body scale

Global representations are additionally normalized as follows:

    root_positions_normalized
        =
        root_displacement / body_scale

    root_displacement_normalized
        =
        root_displacement / body_scale

    root_velocity_normalized
        =
        root_velocity / body_scale

---

# 58. What Is Preserved Without Normalization?

The following remain in their original representation:

    root_positions

and the Stage 03 derived tensors:

    body_core
    body_contact
    hands
    face

The original root trajectory is therefore available in its original dataset coordinate system.

---

# 59. What Is Removed From `full`?

The per-frame global root translation is removed from `full`.

This happens through:

    joints - root_positions

The root-centered local configuration remains.

The global root trajectory is not discarded because it is separately stored.

---

# 60. Reconstruction Contract

The fundamental reconstruction equation is:

    original =
        full * body_scale
        + root_positions

within floating-point precision.

This relationship is one of the key invariants of Stage 04.

---

# 61. Important Invariants

## Invariant 1 — Canonical joint count

    127 joints

must remain in `full`.

---

## Invariant 2 — Temporal length

    input T == output T

---

## Invariant 3 — Root-centered local representation

The root of `full` should be:

    approximately [0,0,0]

for every frame.

---

## Invariant 4 — Global root preservation

    root_positions

must remain available.

---

## Invariant 5 — Sequence-level body scale

There is exactly one:

    body_scale

per sequence.

---

## Invariant 6 — Reconstruction

    original ≈
        full * body_scale
        + root_positions

---

## Invariant 7 — Global normalized trajectory

The normalized trajectory is based on:

    root_displacement / body_scale

not directly on the original absolute root positions.

---

## Invariant 8 — Root velocity convention

    root_velocity

means:

    frame-to-frame displacement

not:

    meters/second

---

## Invariant 9 — Stage 03 derived representations

When present, these are preserved without Stage 04 normalization:

    body_core
    body_contact
    hands
    face

---

# 62. What Stage 04 Does NOT Do

This script does not:

    reduce 127 joints
    retarget motion
    change skeleton topology
    resample time
    interpolate frames
    crop motion
    reorder frames
    classify actions
    train a model
    create latent embeddings
    perform inverse kinematics
    predict future motion
    estimate physical velocity from FPS
    render animations

Its job is deterministic normalization and preservation of global root motion.

---

# 63. Why the Separation Matters

The output intentionally separates:

    Local body configuration

from:

    Global root trajectory

This allows downstream stages to use:

    full

when they need canonical local body motion,

or:

    full
    +
    root motion features

when global locomotion is also important.

---

# 64. Conceptual Representation

The complete Stage 04 representation can be summarized as:

    Original SMPL-X 127 Motion
                |
                +------------------------------+
                |                              |
                v                              v
        Root-centered body              Root trajectory
                |                              |
                v                              |
        Sequence body scale                   |
                |                              |
                v                              |
        Normalized `full`                     |
                |                              |
                |              +---------------+---------------+
                |              |               |               |
                |              v               v               v
                |        displacement      velocity       normalized
                |              |               |           trajectory
                |              |               |
                +--------------+---------------+----------------
                               |
                               v
                       Normalized NPZ

---

# 65. Key Difference Between Local and Global

`full` answers:

    What is the body doing relative to its root?

`root_positions` answers:

    Where is the root in the original coordinate system?

`root_displacement` answers:

    How far has the root moved from the starting position?

`root_positions_normalized` answers:

    How far has the root moved from the starting position after body-scale normalization?

`root_velocity` answers:

    How much did the root move between consecutive frames?

`root_velocity_normalized` answers:

    How much did the root move per frame after body-scale normalization?

Together these provide both local and global motion information.

---

# 66. Example Tensor Inventory

For a sequence with:

    T = 360

the main output tensors are:

    full
        (360,127,3)

    root_positions
        (360,3)

    root_positions_normalized
        (360,3)

    root_displacement
        (360,3)

    root_displacement_normalized
        (360,3)

    root_velocity
        (360,3)

    root_velocity_normalized
        (360,3)

and:

    body_scale
        scalar

If the input contains the Stage 03 derived representations, they are also copied into the output.

---

# 67. Numerical Precision

The implementation converts the main normalized and root-motion tensors to:

    float32

The reconstruction error is evaluated using:

    float64

to make the error calculation more reliable.

Small reconstruction errors are therefore expected because the stored motion representation uses float32 values.

---

# 68. Safety Philosophy

Stage 04 does not assume that a successful NumPy operation automatically means the output is correct.

It explicitly validates:

    input shape
    finite values
    body scale
    reconstruction error

This makes the preprocessing stage more robust for later large-scale processing.

---

# 69. Stage 04 in One Formula

The complete local transformation is:

    full =
        (joints - joints[:,0:1,:])
        /
        max(
            norm(
                joints - joints[:,0:1,:]
            )
        )

where the maximum is taken across the complete sequence and all joints.

The global trajectory is:

    root_displacement =
        joints[:,0,:] - joints[0,0,:]

and:

    root_positions_normalized =
        root_displacement / body_scale

The root frame displacement is:

    root_velocity[0] = 0

    root_velocity[t] =
        root_positions[t] - root_positions[t-1]

and:

    root_velocity_normalized =
        root_velocity / body_scale

---

# 70. Final Stage Philosophy

The core philosophy is:

    Normalize local body motion
    +
    Preserve global root motion
    +
    Keep the canonical 127-joint representation
    +
    Verify reconstruction

The normalization does not replace the complete motion.

It creates a structured representation in which local and global components are explicitly available.

---

# 71. Final Stage Result

Stage 04 produces:

    Canonical local motion
        ->
        full [T,127,3]

plus:

    Original global root motion
        ->
        root_positions

plus:

    Offset-independent global motion
        ->
        root_displacement

plus:

    Scale-normalized global trajectory
        ->
        root_positions_normalized
        root_displacement_normalized

plus:

    Frame-to-frame global motion
        ->
        root_velocity

plus:

    Scale-normalized frame-to-frame motion
        ->
        root_velocity_normalized

plus:

    Sequence normalization scale
        ->
        body_scale

plus:

    Stage 03 representations
        ->
        body_core
        body_contact
        hands
        face

plus:

    Traceability and validation metadata.

---

# 72. Final Status

Stage 04 — Human Motion Normalization

    STATUS:
        COMPLETED

    SCRIPT:
        04_normalize_motion.py

    CANONICAL KEY:
        full

    CANONICAL REPRESENTATION:
        SMPL-X 127

    CANONICAL SHAPE:
        [T,127,3]

    ROOT JOINT:
        index 0

    LOCAL NORMALIZATION:
        root-centered
        +
        sequence-level body scale

    GLOBAL MOTION:
        preserved

    GLOBAL NORMALIZATION:
        root displacement from first frame
        +
        sequence body scale

    ROOT VELOCITY:
        frame-to-frame displacement

    ROOT VELOCITY UNIT:
        dataset_units_per_frame

    CANONICAL INFORMATION REDUCED:
        False

    RECONSTRUCTION CHECK:
        Enabled

    RECONSTRUCTION THRESHOLD:
        max_abs_error <= 1e-4

---

# 73. Quick Reference

    INPUT
        data/processed/joints/**/*.npz

    OUTPUT
        data/processed/normalized/**/*.npz

    CANONICAL INPUT
        full
        [T,127,3]

    CANONICAL OUTPUT
        full
        [T,127,3]

    ROOT
        joint index 0

    LOCAL NORMALIZATION
        centered = joints - root_position
        full = centered / body_scale

    BODY SCALE
        max norm of centered joints
        across the complete sequence

    GLOBAL ORIGINAL
        root_positions

    GLOBAL DISPLACEMENT
        root_displacement

    GLOBAL NORMALIZED TRAJECTORY
        root_positions_normalized

    GLOBAL NORMALIZED DISPLACEMENT
        root_displacement_normalized

    GLOBAL FRAME DISPLACEMENT
        root_velocity

    GLOBAL NORMALIZED FRAME DISPLACEMENT
        root_velocity_normalized

    SCALE
        body_scale

    PRESERVED DERIVED DATA
        body_core
        body_contact
        hands
        face

    METADATA
        source
        representation
        normalization
        root_joint_index
        global_motion
        root_velocity_unit

    RECONSTRUCTION METRICS
        reconstruction_max_abs_error
        reconstruction_mean_abs_error
        reconstruction_rmse

    SUMMARY
        _normalization_summary.json

    RECONSTRUCTION
        original ≈
        full * body_scale + root_positions

    STATUS
        COMPLETED

---

# 74. Video Reference

Execution / demonstration video:

https://youtu.be/Gka6i7_VcUs

The video is associated with Stage 04 and documents the execution/demonstration of this stage.

---

# 75. One-Sentence Definition

Stage 04 deterministically converts SMPL-X 127-joint motion into a root-centered, sequence-body-scale-normalized local representation while preserving the original root trajectory, displacement, frame-to-frame root motion, normalized global motion features, Stage 03 derived representations, and enough information to reconstruct the original motion within a `1e-4` maximum absolute-error threshold.