# Stage 04 — Human Motion Normalization

**Project:** Latent Objective Humanoid  
**Pipeline:** Human Data Processing  
**Stage:** 04 — Motion Normalization  
**Canonical Representation:** SMPL-X 127 Joints  
**Status:** Completed  
**Video:** https://youtu.be/Gka6i7_VcUs

---

# 1. Purpose of This Document

This document permanently records the complete design, motivation, implementation, data structure, normalization strategy, validation method, and output format of Stage 04 of the Latent Objective Humanoid project.

The goal is that, even much later, this document can be opened independently and still provide a complete understanding of:

- What this stage is
- Why this stage exists
- What problem it solves
- What the input data looks like
- What the output data looks like
- What normalization means in this project
- Why root-centered motion is used
- Why global root motion must be preserved separately
- What information is stored inside every output NPZ
- How the original motion can be reconstructed
- What validation was performed
- What was deliberately preserved
- What was deliberately transformed
- How this representation will be used by later stages

This stage is therefore not simply a coordinate preprocessing step.

It establishes the motion representation that later learning stages can rely on.

---

# 2. Stage Overview

The input to this stage is the processed human-motion joint dataset produced by the previous human-data processing stage.

Each input NPZ contains a canonical SMPL-X representation.

The canonical representation is:

    SMPL-X 127 joints
    Shape: [T, 127, 3]

where:

- `T` = number of frames
- `127` = number of canonical SMPL-X joints
- `3` = XYZ coordinates

The central design decision of this stage is:

> Local body motion and global root motion are represented separately, rather than destroying global motion during root-centering.

The resulting representation contains both:

1. Local normalized body motion
2. Global root motion information

This distinction is fundamental.

---

# 3. Why Normalization Is Necessary

Raw human motion sequences can differ in several ways:

- Different global positions
- Different initial locations
- Different body scales
- Different recording locations
- Different distances from the coordinate origin
- Different global trajectories

If raw coordinates are directly passed to a learning model, the model may spend capacity learning irrelevant variations such as:

- "Where was the person standing in the recording space?"
- "How far from the origin was the person?"
- "What was the initial translation of this sequence?"

Those variations are often not the actual body-motion objective.

For example, two people can perform the same squat:

    Person A:
        starts at X = 0

    Person B:
        starts at X = 10

The local body motion can be essentially identical even though the absolute coordinates are completely different.

Therefore, the body motion should have a canonical local representation.

However, simply removing the root position is also problematic because global locomotion is meaningful.

For example:

    Walking forward
    Walking backward
    Running
    Jumping while translating
    Changing global position
    Moving along a trajectory

must not be accidentally discarded.

Therefore, the solution used in this stage is:

    Normalize local body motion
    +
    Preserve global root motion separately

---

# 4. Core Representation Strategy

The complete conceptual representation is:

    Original SMPL-X Motion
              |
              |
              +-----------------------------+
              |                             |
              v                             v
        Local Body Motion             Global Root Motion
              |                             |
              v                             v
        Root Centering               Root Position
              |                       Root Displacement
              v                       Root Velocity
        Body Scale                    Normalized Trajectory
        Normalization
              |
              v
        `full`
        [T,127,3]

The important point is that `full` is intentionally a LOCAL representation after normalization.

It is not intended to contain the absolute global position of the person.

Global information is stored separately.

---

# 5. Input Dataset Structure

The input root is:

    data/processed/joints/

The dataset hierarchy is preserved.

For example:

    data/
        processed/
            joints/
                ACCAD/
                    Female1General_c3d/
                        A1 - Stand_poses.npz
                        A10 - lie to crouch_poses.npz
                        A11 - crawl forward_poses.npz
                        ...

The Stage 04 script recursively searches for:

    *.npz

inside the input root.

The corresponding normalized output hierarchy is preserved under:

    data/processed/normalized/

For example:

    joints/
        ACCAD/
            Female1General_c3d/
                A1 - Stand_poses.npz

becomes:

    normalized/
        ACCAD/
            Female1General_c3d/
                A1 - Stand_poses.npz

This makes it possible to map every normalized file back to its original source.

---

# 6. Input NPZ Structure

The canonical input file contains:

    full
    body_core
    body_contact
    hands
    face

For example:

    full            -> [T, 127, 3]
    body_core       -> [T, 22, 3]
    body_contact    -> [T, 6, 3]
    hands           -> [T, 40, 3]
    face            -> [T, 59, 3]

The most important tensor is:

    full

because it is the canonical SMPL-X 127-joint representation.

The other representations are derived subsets.

---

# 7. Canonical Representation

The canonical tensor is explicitly defined as:

    CANONICAL_KEY = "full"

and:

    CANONICAL_JOINT_COUNT = 127

and:

    COORD_DIM = 3

Therefore the expected canonical tensor shape is:

    [T,127,3]

The normalization stage does NOT reduce the canonical joint representation.

It does NOT convert:

    127 joints -> 22 joints

or:

    127 joints -> another reduced skeleton

Instead:

    127 joints remain 127 joints

throughout the normalization stage.

This is an intentional design decision.

---

# 8. Validation of the Canonical Tensor

Before normalization, the input `full` tensor is validated.

The following conditions must hold:

1. The tensor must be a NumPy array.
2. It must have exactly 3 dimensions.
3. The second dimension must contain exactly 127 joints.
4. The third dimension must contain exactly 3 coordinates.
5. The sequence must contain at least one frame.
6. The tensor must not contain NaN values.
7. The tensor must not contain Inf values.

The required shape is therefore:

    [T,127,3]

If the canonical tensor does not satisfy these requirements, the file is marked as failed.

---

# 9. The First Important Problem We Encountered

The first version of the normalization script attempted to automatically find a joint tensor inside the NPZ.

However, the input files contained:

    ['full', 'body_core', 'body_contact', 'hands', 'face']

The script could not safely infer which representation was canonical.

The actual structure was then inspected directly.

For example:

    full            (360, 127, 3) float32
    body_core       (360, 22, 3) float32
    body_contact    (360, 6, 3) float32
    hands           (360, 40, 3) float32
    face            (360, 59, 3) float32

This confirmed that:

    full

is the canonical representation.

The script was therefore changed to explicitly use:

    CANONICAL_KEY = "full"

This is safer and more reproducible than trying to guess the canonical tensor.

---

# 10. Root-Centered Local Motion

The main local normalization operation is root-centering.

The root joint is:

    joint 0

which represents the pelvis/root of the canonical representation.

For every frame:

    root_position[t] = joints[t,0]

The root position has shape:

    [T,3]

The local body representation is computed as:

    centered[t,j] = joints[t,j] - root_position[t]

In vectorized form:

    root_position = joints[:, 0:1, :]

    centered = joints - root_position

The resulting tensor remains:

    [T,127,3]

---

# 11. What Root-Centering Means

Suppose a person walks forward.

In the original global representation:

    Frame 0:
        person at X = 0

    Frame 1:
        person at X = 0.1

    Frame 2:
        person at X = 0.2

    Frame 3:
        person at X = 0.3

The whole body is translating through space.

After root-centering, the root is placed at the origin for every frame.

Therefore:

    Frame 0:
        root = [0,0,0]

    Frame 1:
        root = [0,0,0]

    Frame 2:
        root = [0,0,0]

    Frame 3:
        root = [0,0,0]

The body configuration relative to the root remains.

But the absolute translation of the root is no longer inside `full`.

This is intentional.

---

# 12. Why Walking Can Look Different After Normalization

This explains an important visual observation made during validation.

In the original motion, a person may visibly:

    take a step
    move forward
    move backward
    translate across the scene

After root-centering, the same motion may appear to happen in place.

For example:

    ORIGINAL

    Person
       |
       |-------> global translation


    ROOT-CENTERED

    Person
       |
       |
       O
      /|\
      / \

    The body motion remains,
    but the global root translation is no longer inside `full`.

This does NOT mean that the global motion was destroyed.

The global motion is stored separately.

---

# 13. Local Motion vs Global Motion

This distinction is one of the most important concepts in this stage.

## Local motion

Local motion answers:

> How are the body joints moving relative to the person's root?

Examples:

- Arm movement
- Leg movement
- Joint configuration
- Crouching
- Standing
- Crawling
- Limb articulation
- Body deformation relative to the pelvis

This is stored primarily in:

    full

after root-centering and body-scale normalization.

---

## Global motion

Global motion answers:

> Where is the person's root moving in the environment?

Examples:

- Walking forward
- Walking backward
- Moving sideways
- Running through the scene
- Translating through space
- Global trajectory
- Root velocity

This is represented by:

    root_positions
    root_positions_normalized
    root_displacement
    root_velocity

The two representations are complementary.

---

# 14. Sequence-Level Body Scale

After root-centering, the sequence is normalized by a single body scale.

The scale is computed across the entire sequence.

First:

    distances = norm(centered_joints)

Then:

    scale = max(distances)

The important point is that there is:

    ONE scale per sequence

not:

    ONE scale per frame

This is critical.

---

# 15. Why Scale Is Sequence-Level

If each frame were independently normalized, the body could artificially change size over time.

For example:

    Frame 1 -> scale = 1.0
    Frame 2 -> scale = 1.1
    Frame 3 -> scale = 0.9
    Frame 4 -> scale = 1.2

This could introduce unwanted temporal distortions.

Instead, this pipeline computes:

    scale = one scalar for the entire sequence

and uses that same scalar for every frame.

Therefore the temporal geometry of the motion is preserved.

---

# 16. Local Normalized Representation

The final normalized local motion is:

    normalized = centered / body_scale

or mathematically:

    normalized[t,j] =
        (original[t,j] - root_position[t])
        / body_scale

The resulting shape remains:

    [T,127,3]

and is stored as:

    full

The tensor is stored as:

    float32

---

# 17. Global Root Position

The original root trajectory is preserved.

For every frame:

    root_positions[t] = original[t,0]

Shape:

    [T,3]

This represents the root position in the original dataset coordinate system.

This information is important because it contains global translation.

---

# 18. Root Displacement

The root displacement is measured relative to the initial frame.

The formula is:

    root_displacement[t] =
        root_positions[t] - root_positions[0]

Shape:

    [T,3]

Therefore:

    root_displacement[0] = [0,0,0]

This representation removes the arbitrary initial location while preserving the actual movement during the sequence.

For example:

    Frame 0 -> [0.0, 0.0, 0.0]
    Frame 1 -> [0.1, 0.0, 0.0]
    Frame 2 -> [0.2, 0.0, 0.0]
    Frame 3 -> [0.3, 0.0, 0.0]

This clearly represents forward movement.

---

# 19. Normalized Global Trajectory

A second global representation is:

    root_positions_normalized

This removes the initial global offset and normalizes the trajectory using the same sequence body scale.

Conceptually:

    root_positions_normalized =
        (root_positions - root_positions[0])
        / body_scale

This means the global trajectory is:

1. Independent of the arbitrary initial position.
2. Consistent with the body-scale normalization.
3. Still able to represent forward/backward/sideways translation.

This gives a normalized global coordinate representation without putting global translation back into `full`.

---

# 20. Root Velocity

The root velocity is represented as the frame-to-frame change in root position.

Conceptually:

    root_velocity[t] =
        root_positions[t] - root_positions[t-1]

with the first frame handled consistently by the implementation.

Shape:

    [T,3]

The current convention is:

    dataset units per frame

This is an important metadata convention.

It means this tensor is not currently expressed in physical units such as meters/second unless the upstream dataset itself is calibrated that way.

The current representation is:

    displacement per frame

in the coordinate units of the source dataset.

---

# 21. Why Root Velocity Is Useful

Root velocity can help later models distinguish:

    Standing
    Walking
    Running
    Moving forward
    Moving backward
    Stopping
    Accelerating
    Changing trajectory

For example:

    root_velocity ≈ 0

suggests little global translation.

While:

    root_velocity > 0

along the relevant direction indicates translation.

Therefore root velocity provides a compact description of global locomotion dynamics.

---

# 22. What Happens to Jumping?

A visual question during validation was whether a jump appears different after normalization.

This is expected.

A jump can contain two different components:

1. Local body configuration changes
2. Global root translation

The local body configuration remains inside:

    full

The global movement of the root remains inside:

    root_positions
    root_positions_normalized
    root_displacement
    root_velocity

Therefore a jump should not be evaluated using only the normalized `full` tensor.

The complete motion representation is:

    Local body motion
    +
    Global root motion

Both are needed to understand the complete physical trajectory.

---

# 23. Reconstruction Principle

A major requirement of this stage is that normalization should not irreversibly destroy information.

The local normalized representation is:

    full =
        (original - root_position) / body_scale

Therefore the original coordinates can be reconstructed as:

    original =
        full * body_scale
        + root_position

This is the fundamental reconstruction relationship.

---

# 24. Reconstruction Check

The implementation performs a reconstruction consistency check.

Conceptually:

    reconstructed =
        normalized * body_scale
        + root_positions

Then:

    reconstruction_error =
        max(abs(reconstructed - original))

The purpose is to verify that the normalization transformation is mathematically consistent.

---

# 25. Reconstruction Results

The test runs showed reconstruction errors such as:

    5.9604644775e-08

and:

    1.1920928955e-07

These values are extremely small and are consistent with normal floating-point precision for float32 operations.

Therefore the normalization pipeline successfully preserved the original coordinate information required for reconstruction.

The important conclusion is:

> Root-centering did not destroy the original global translation because the root trajectory was explicitly preserved.

---

# 26. Output NPZ Structure

Every normalized motion sequence is stored as one NPZ file.

For example:

    normalized/
        ACCAD/
            Female1General_c3d/
                A1 - Stand_poses.npz

The output file contains the following major groups of information.

---

# 27. `full`

Key:

    full

Shape:

    [T,127,3]

Meaning:

    Canonical SMPL-X 127-joint local motion.

Transformation:

    root-centered
    +
    sequence-level body-scale normalized

This is the primary local motion tensor.

It retains all 127 canonical joints.

---

# 28. `root_positions`

Key:

    root_positions

Shape:

    [T,3]

Meaning:

    Original global root/pelvis position for every frame.

This preserves the original global trajectory.

It is not root-centered.

It is stored in the original dataset coordinate system.

---

# 29. `root_positions_normalized`

Key:

    root_positions_normalized

Shape:

    [T,3]

Meaning:

    Global root trajectory after:

    1. Removing the initial offset.
    2. Applying sequence body-scale normalization.

This provides a normalized global trajectory.

---

# 30. `root_displacement`

Key:

    root_displacement

Shape:

    [T,3]

Meaning:

    Root movement relative to the first frame.

Formula:

    root_displacement[t] =
        root_positions[t] - root_positions[0]

The first frame is therefore:

    [0,0,0]

This representation is particularly useful for describing how far the person has moved during the sequence.

---

# 31. `root_velocity`

Key:

    root_velocity

Shape:

    [T,3]

Meaning:

    Frame-to-frame root translation.

Current convention:

    dataset units per frame

This represents global locomotion dynamics.

---

# 32. `body_scale`

Key:

    body_scale

Shape:

    scalar

Meaning:

    The single sequence-level scale factor used to normalize the local body motion.

There is one value for the entire sequence.

It is not recomputed independently for every frame.

---

# 33. `body_core`

Key:

    body_core

Typical shape:

    [T,22,3]

Meaning:

    Previously extracted body-core representation.

It is preserved in the normalized output so downstream stages can access it without repeating extraction.

---

# 34. `body_contact`

Key:

    body_contact

Typical shape:

    [T,6,3]

Meaning:

    Contact-related body joints.

It is preserved as part of the original processed representation.

---

# 35. `hands`

Key:

    hands

Typical shape:

    [T,40,3]

Meaning:

    Hand-related joints.

This representation is preserved so that downstream stages can use hand information without recomputing it.

---

# 36. `face`

Key:

    face

Typical shape:

    [T,59,3]

Meaning:

    Face-related joints.

This representation is also preserved unchanged.

---

# 37. `source`

Key:

    source

Meaning:

    Original input file path.

This provides traceability between the normalized output and the original dataset file.

For example:

    data/processed/joints/ACCAD/...
    
This makes debugging and dataset auditing easier.

---

# 38. `representation`

Key:

    representation

Value:

    smplx_127

Meaning:

    The canonical representation used by the file is SMPL-X 127 joints.

This is explicit metadata rather than something that must be inferred later.

---

# 39. `normalization`

Key:

    normalization

Value:

    root_centered_sequence_body_scale

Meaning:

    The local body representation was:

    1. Root-centered
    2. Normalized using sequence-level body scale

This records the transformation convention used to create the file.

---

# 40. Complete NPZ Inventory

Therefore, conceptually, every normalized NPZ contains:

    full
    root_positions
    root_positions_normalized
    root_displacement
    root_velocity
    body_scale
    body_core
    body_contact
    hands
    face
    source
    representation
    normalization

The exact tensor shapes depend on `T`, the number of frames in the sequence, but the semantic structure remains the same.

---

# 41. Example of One Output File

For a sequence with:

    T = 360

the main tensors are:

    full
        (360, 127, 3)

    root_positions
        (360, 3)

    root_positions_normalized
        (360, 3)

    root_displacement
        (360, 3)

    root_velocity
        (360, 3)

and:

    body_scale
        scalar

The preserved derived representations are:

    body_core
        (360, 22, 3)

    body_contact
        (360, 6, 3)

    hands
        (360, 40, 3)

    face
        (360, 59, 3)

---

# 42. Important Design Decision: Do Not Reduce `full`

The canonical representation remains:

    [T,127,3]

This is intentional.

Although a reduced body representation such as:

    [T,22,3]

could be easier for some models, reducing the canonical data at this stage would permanently discard information.

The project therefore keeps:

    full = 127 joints

and provides reduced/derived representations separately.

This keeps the normalized dataset flexible for future experiments.

---

# 43. Why We Preserve the Derived Representations

The input already contains:

    body_core
    body_contact
    hands
    face

Instead of throwing these away, Stage 04 preserves them.

This gives downstream stages access to:

    Full canonical representation
    +
    Body subset
    +
    Contact subset
    +
    Hand subset
    +
    Face subset

without requiring the extraction stage to be repeated.

---

# 44. Data Flow

The complete Stage 04 data flow is:

    Input NPZ
        |
        v
    Load `full`
        |
        v
    Validate [T,127,3]
        |
        v
    Extract root position
        |
        +--------------------------+
        |                          |
        v                          v
    Root-center               Preserve root
        |                          |
        v                          v
    Compute sequence          root_positions
    body scale
        |
        v
    Normalize local body
        |
        v
    `full`
        |
        +--------------------------+
        |                          |
        v                          v
    Save local motion       Save global motion
                               |
                               +--> root_positions
                               |
                               +--> root_positions_normalized
                               |
                               +--> root_displacement
                               |
                               +--> root_velocity
                               |
                               +--> body_scale
        |
        v
    Preserve derived data
        |
        +--> body_core
        +--> body_contact
        +--> hands
        +--> face
        |
        v
    Reconstruction Check
        |
        v
    Save normalized NPZ

---

# 45. What Is Normalized?

The following is normalized:

    Local body coordinates

Specifically:

    full

using:

    root-centering
    +
    sequence-level body scale

The normalized global trajectory is also available as:

    root_positions_normalized

---

# 46. What Is Preserved in Original Coordinates?

The original global root trajectory is preserved as:

    root_positions

This is important because it provides access to the original global coordinate system.

Therefore we have both:

    Original global root trajectory

and:

    Normalized global root trajectory

---

# 47. What Is Not Removed?

The normalization stage does NOT remove:

    Joint identity
    Joint count
    Temporal ordering
    Frame count
    Local body motion
    Global root trajectory
    Root displacement
    Root velocity
    Hand information
    Face information
    Contact information

The canonical 127-joint structure remains intact.

---

# 48. What Is Removed from `full`?

The following is intentionally removed from `full`:

    Per-frame global root translation

Because `full` is converted into a root-relative representation.

This is not considered information loss because the root trajectory is stored separately.

---

# 49. Why This Representation Is Better for Learning

The representation separates two fundamentally different sources of variation.

## Body configuration

Stored in:

    full

This captures:

    pose
    articulation
    local body dynamics

## Global locomotion

Stored in:

    root_positions_normalized
    root_displacement
    root_velocity

This captures:

    translation
    trajectory
    global locomotion

A future model can therefore choose whether it needs:

    local motion only

or:

    local motion + global trajectory

without requiring a different dataset representation.

---

# 50. Example: Walking Forward

Suppose a person walks forward.

Original:

    Root:
        X = 0.0
        X = 0.1
        X = 0.2
        X = 0.3

Local normalized body:

    full

contains the changing leg and body configuration.

Global information:

    root_displacement:
        0.0
        0.1
        0.2
        0.3

Therefore:

    `full`
        tells us how the body is moving

while:

    `root_displacement`
        tells us where the body is moving

Together they describe the complete motion.

---

# 51. Example: Same Walk at a Different Starting Position

Consider two sequences.

Sequence A:

    starts at X = 0

Sequence B:

    starts at X = 100

If the person performs the same local walking motion, the root-centered representation can be very similar.

This is desirable because the model should not need to learn:

    "X = 100 means a different walking motion."

Instead:

    Local motion -> `full`

and:

    Global trajectory -> root information

are treated separately.

---

# 52. Example: Walking Backward

If the person walks backward, the local body motion may look similar to another sequence, but the global root trajectory has the opposite direction.

This information is preserved through:

    root_displacement
    root_velocity
    root_positions_normalized

Therefore backward motion is not confused with stationary motion simply because the body is root-centered.

---

# 53. Example: Standing Still

For a standing sequence:

    root_velocity ≈ 0

and:

    root_displacement ≈ constant / near zero

while:

    full

still contains the body configuration.

This gives the future model a clean distinction between:

    body pose

and:

    global movement.

---

# 54. Example: Crawling

For crawling, the body may undergo large local configuration changes.

The normalized:

    full

captures these body-relative changes.

The global root trajectory captures whether the person is:

    crawling forward
    crawling backward
    remaining approximately stationary

This is particularly useful because crawling can involve substantial changes in body configuration while also producing meaningful translation.

---

# 55. Example: Jumping

A jump can be decomposed into:

    Local:
        body configuration changes

    Global:
        root trajectory / vertical movement

Therefore both components are retained.

The normalized visualization of `full` should not be interpreted as the complete global motion by itself.

The complete motion is:

    full
    +
    root motion

---

# 56. Why We Do Not Normalize Each Frame Independently

Per-frame normalization would be problematic.

For example, if each frame were independently scaled, the same body could appear to change scale during the sequence.

This could create artificial temporal effects.

Instead:

    one body scale
    per sequence

is computed.

Therefore temporal consistency is preserved.

---

# 57. Why We Do Not Simply Normalize Everything to the Origin

Another possible approach would be to force the complete motion sequence into a fixed global coordinate system and discard the original root trajectory.

That would make visualization simpler but would destroy useful locomotion information.

The current method is better because:

    Local body motion
        ->
        canonicalized

while:

    Global root motion
        ->
        explicitly preserved

This is a deliberate separation rather than an accidental side effect.

---

# 58. Validation Strategy

Stage 04 uses two complementary validation methods.

## Visual validation

The normalized sequences were visually inspected.

The expected behavior is:

    Body remains anatomically and temporally coherent.

The global translation may disappear from `full` because `full` is root-centered.

This is expected.

## Numerical validation

The original motion is reconstructed from the normalized representation.

The maximum reconstruction error is measured.

This provides a much stronger validation than visual inspection alone.

---

# 59. Numerical Validation Result

The test run produced:

    reconstruction max error:
        ~5.96e-08
        ~1.19e-07

These errors are effectively zero for the float32 representation used.

Therefore the transformation is numerically consistent.

---

# 60. Test Run

The pipeline was tested on five files.

The test included:

    A1 - Stand_poses.npz
    A10 - lie to crouch_poses.npz
    A11 - crawl forward_poses.npz
    A12 - crawl backwards_poses.npz
    A14 - stand to skip_poses.npz

The result was:

    Processed : 5
    Failed    : 0

This confirmed that the corrected canonical-key handling and normalization pipeline worked successfully on the test subset.

---

# 61. Example Test Shapes

The test sequences included different temporal lengths.

Examples:

    A1:
        [360,127,3]

    A10:
        [524,127,3]

    A11:
        [2399,127,3]

    A12:
        [2647,127,3]

    A14:
        [618,127,3]

The normalization pipeline preserves the frame count.

For example:

    [2399,127,3]
        ->
    [2399,127,3]

No temporal downsampling or frame removal is performed in this stage.

---

# 62. Important Property: Temporal Information Is Preserved

The normalization stage does not:

    resample
    crop
    downsample
    reorder
    interpolate
    remove frames

The temporal dimension remains:

    T -> T

Therefore:

    [T,127,3]

becomes:

    [T,127,3]

---

# 63. Output Directory

The default output directory is:

    data/processed/normalized/

The directory hierarchy from the input dataset is preserved.

A summary file is also created:

    _normalization_summary.json

inside the normalized root.

---

# 64. Normalization Summary

The summary JSON records information about the processing run.

It includes:

    script
    project_root
    input_root
    output_root
    canonical_key
    canonical_representation
    canonical_shape
    normalization
    canonical_information_reduced
    processed
    failed
    files_found
    failed_files
    results

This provides a machine-readable record of the preprocessing stage.

---

# 65. Error Handling

Each NPZ file is processed independently.

If a file fails:

    The error is reported.
    The file is added to the failed list.
    Processing continues with the next file.

Therefore one corrupted or incompatible file does not necessarily stop the entire dataset preprocessing run.

---

# 66. `--limit`

The script supports:

    --limit N

For example:

    python 04_normalize_motion.py --limit 5

processes only the first five discovered NPZ files.

This is useful for:

    debugging
    validation
    visual inspection
    testing

before processing the entire dataset.

Once the pipeline is verified, the complete dataset can be processed without the limit.

---

# 67. Recommended Full-Dataset Run

After validation, the intended full-dataset execution is:

    python 04_normalize_motion.py

This processes all NPZ files under:

    data/processed/joints/

and writes the corresponding normalized files under:

    data/processed/normalized/

---

# 68. Important File-Level Contract

Every normalized NPZ should be considered a self-contained motion sample.

The file contains:

    Canonical local body motion
    +
    Global root motion
    +
    Normalization metadata
    +
    Derived representations

This makes each NPZ independently interpretable by downstream stages.

---

# 69. Recommended Interpretation of Each Tensor

For future development, the following interpretation should be treated as the canonical contract.

    full
        = normalized local body motion

    root_positions
        = original global root trajectory

    root_positions_normalized
        = normalized global root trajectory

    root_displacement
        = global displacement relative to initial position

    root_velocity
        = global root motion between frames

    body_scale
        = sequence normalization scale

    body_core
        = reduced body representation

    body_contact
        = contact-related representation

    hands
        = hand representation

    face
        = face representation

---

# 70. Local + Global Is the Core Design

The most important conceptual decision of this stage is:

    LOCAL ≠ GLOBAL

They should not be forced into a single representation.

Instead:

    Local body motion
        ->
        `full`

and:

    Global motion
        ->
        root motion tensors

This gives the project flexibility for later representation learning.

---

# 71. Future Model Usage

A future model may use only:

    full

if the objective is local body-motion learning.

Or it may use:

    full
    +
    root_positions_normalized

if global trajectory is relevant.

Or:

    full
    +
    root_velocity

if locomotion dynamics are important.

Or all available motion features can be combined.

The dataset therefore does not lock the project into one particular model architecture.

---

# 72. Potential Future Representation

A later learning stage can conceptually use:

    Pose Encoder
        |
        |---- full
        |
        v
    Local Motion Latent


    Root Encoder
        |
        |---- root_positions_normalized
        |---- root_velocity
        |
        v
    Global Motion Latent


    Local Latent + Global Latent
                |
                v
          Motion Representation

This separation can be useful for latent objective learning because local body configuration and global locomotion are related but distinct sources of information.

---

# 73. Reconstruction Contract

The normalized file should be considered valid if the following relationship approximately holds:

    original ≈ full * body_scale + root_positions

The small difference comes from numerical floating-point precision.

This reconstruction property should be preserved in future modifications of the normalization stage.

If a future modification produces a large reconstruction error, the normalization pipeline should be considered potentially broken until investigated.

---

# 74. Important Invariant #1 — Joint Count

The canonical joint count must remain:

    127

Never silently change:

    full

to a reduced representation.

---

# 75. Important Invariant #2 — Temporal Length

For every input sequence:

    input T == output T

No frame should be removed by this normalization stage.

---

# 76. Important Invariant #3 — Local Motion

The normalized `full` representation must remain:

    root-centered

The root joint in `full` should therefore be approximately:

    [0,0,0]

for every frame.

---

# 77. Important Invariant #4 — Global Motion

Global root movement must not be discarded.

At minimum:

    root_positions

must remain available.

---

# 78. Important Invariant #5 — Sequence-Level Scale

The local body scale must be one scalar per sequence.

It must not vary independently from frame to frame.

---

# 79. Important Invariant #6 — Reconstruction

The original motion should remain reconstructible:

    original ≈ full * body_scale + root_positions

within floating-point precision.

---

# 80. Important Invariant #7 — Derived Data Preservation

The following derived representations should remain available when present in the input:

    body_core
    body_contact
    hands
    face

---

# 81. Important Invariant #8 — Dataset Traceability

Each output file should preserve its relationship with the source file.

The `source` metadata is therefore retained.

---

# 82. What This Stage Does NOT Do

Stage 04 does NOT:

    perform motion retargeting
    change the skeleton topology
    reduce 127 joints to a smaller canonical skeleton
    perform temporal resampling
    perform motion interpolation
    perform motion segmentation
    classify actions
    learn a neural representation
    train a model
    generate latent embeddings
    perform inverse kinematics
    perform trajectory prediction

This stage is specifically a deterministic motion representation and normalization stage.

---

# 83. Deterministic Nature

The normalization is deterministic.

Given the same input NPZ and the same implementation:

    the same normalized representation
    and
    the same normalization scale

should be produced.

No learned model is involved in this stage.

---

# 84. Why This Stage Comes Before Learning

The purpose of preprocessing is to provide a consistent coordinate representation before learning.

Without this step, a future model may learn undesirable correlations related to:

    initial position
    body scale
    global coordinate offset

Instead, the model can focus on meaningful motion structure.

The normalization therefore acts as a representation standardization layer between raw processed motion and learned motion representations.

---

# 85. Conceptual Summary

The entire transformation can be summarized as:

    RAW HUMAN MOTION
            |
            v
    SMPL-X 127
            |
            +-----------------------------+
            |                             |
            v                             v
    ROOT-CENTERED BODY              ORIGINAL ROOT
            |                             |
            v                             v
    SEQUENCE BODY SCALE          GLOBAL TRAJECTORY
            |                             |
            v                             +--> displacement
    NORMALIZED LOCAL BODY              |
            |                          +--> velocity
            v                          |
          `full`                       +--> normalized trajectory
            |
            +-----------------------------+
                          |
                          v
                 NORMALIZED NPZ

---

# 86. Final Dataset Philosophy

The normalized dataset follows one central philosophy:

> Canonicalize what should be canonicalized, but preserve information that represents meaningful motion.

Therefore:

    Initial global position
        can be removed from the local body representation.

But:

    Global movement
        must be preserved.

Similarly:

    Body scale differences
        can be normalized.

But:

    Temporal body dynamics
        must be preserved.

This balance is the main purpose of Stage 04.

---

# 87. Final Stage Result

Stage 04 successfully establishes a dual representation for human motion:

## Local representation

    `full`

    Shape:
        [T,127,3]

    Contains:
        Root-centered,
        sequence-level body-scale normalized
        SMPL-X motion.

## Global representation

    `root_positions`
    `root_positions_normalized`
    `root_displacement`
    `root_velocity`

    Contains:
        Global root trajectory and motion.

Together they provide:

    Local Body Motion
        +
    Global Motion

without sacrificing the canonical 127-joint representation.

---

# 88. Final Status

Stage 04 — Human Motion Normalization:

    STATUS: COMPLETED

Validation:

    Canonical SMPL-X 127:
        PASS

    Root-centering:
        PASS

    Sequence-level body scaling:
        PASS

    Global root preservation:
        PASS

    Root displacement:
        PASS

    Root velocity:
        PASS

    Reconstruction check:
        PASS

    Derived representation preservation:
        PASS

    Test subset:
        5 files

    Processed:
        5

    Failed:
        0

Observed reconstruction errors:

    approximately 1e-7

which is consistent with float32 numerical precision.

---

# 89. One-Sentence Definition of Stage 04

If this entire stage needs to be remembered in one sentence:

> Stage 04 converts SMPL-X 127 human motion into a canonical root-centered, sequence-scale-normalized local representation while explicitly preserving the global root trajectory, displacement, and velocity so that the complete original motion remains reconstructible.

---

# 90. Quick Reference

    INPUT
        data/processed/joints/**/*.npz

    CANONICAL INPUT
        full
        [T,127,3]

    LOCAL OUTPUT
        full
        [T,127,3]

    GLOBAL OUTPUT
        root_positions
        root_positions_normalized
        root_displacement
        root_velocity

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

    SUMMARY
        _normalization_summary.json

    LOCAL NORMALIZATION
        root-centered
        +
        sequence-level body scale

    GLOBAL MOTION
        preserved separately

    RECONSTRUCTION
        original ≈ full * body_scale + root_positions

    VALIDATION
        reconstruction error ≈ 1e-7

    CANONICAL REPRESENTATION
        SMPL-X 127

    STATUS
        COMPLETED

---

# 91. Video Reference

The execution and visual validation of this stage are documented in the project video:

https://youtu.be/Gka6i7_VcUs

Video title:

    Human Motion Normalization | SMPL-X 127 Joint Dataset | Local + Global Motion Pipeline

---

# 92. End of Stage 04 Documentation

Stage 04 establishes the normalized human-motion data representation used as the foundation for subsequent stages of the Latent Objective Humanoid project.

The key principle to carry forward is:

    LOCAL BODY MOTION
        +
    GLOBAL ROOT MOTION

rather than treating root-centered normalization as a complete replacement for global motion.

The canonical SMPL-X 127 representation remains intact, local body motion is normalized, global root motion is preserved, and reconstruction has been numerically verified.