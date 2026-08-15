# Motion Segmentation

## 1. Purpose

The purpose of this stage is to divide continuous human motion sequences
into meaningful and comparable motion segments.

AMASS sequences may contain long periods of motion and may include
different movement phases.

For objective analysis, comparing complete recordings directly may hide
important behavioral differences.

Therefore:

    Continuous Human Motion
            ↓
       Motion Segmentation
            ↓
      Comparable Segments
            ↓
      Feature Analysis
            ↓
      Objective Inference

The purpose of segmentation is data organization and comparison.

It does NOT determine the human objective.

---

## 2. Input

The segmentation stage uses the processed motion representation and
features generated in the previous stages.

Inputs include:

- 3D joint positions
- Joint velocities
- Joint accelerations
- Root motion
- Foot contact information
- Temporal information
- Extracted locomotion features

Example:

    positions
    velocity
    acceleration
    root_motion
    contacts
    fps

---

## 3. Why Segmentation Is Necessary

A complete motion sequence may contain:

    Preparation
        ↓
    Locomotion
        ↓
    Turning
        ↓
    Stopping
        ↓
    Other movement

Treating the entire sequence as one sample can mix different behaviors.

Segmentation allows us to compare more consistent movement units.

The goal is therefore:

    Long Motion Sequence
            ↓
    Behaviorally Consistent Segments

---

## 4. Initial Segmentation Target

The initial research focuses primarily on human locomotion.

Therefore, the first segmentation target is a walking segment that contains
a sufficiently consistent locomotion pattern.

For example:

    Start Walking
         ↓
    Stable Locomotion
         ↓
    End Walking

The exact segmentation criteria will be determined from observable motion
signals rather than assumed human intentions.

---

## 5. Available Signals

Segmentation can use measurable signals already extracted from the data.

Potential signals include:

### Root Motion

- Root velocity
- Root displacement
- Root orientation

### Foot Motion

- Foot velocity
- Foot height
- Foot contact state

### Temporal Motion

- Velocity changes
- Acceleration changes
- Motion discontinuities

These signals provide observable evidence for identifying changes in
movement phase.

---

## 6. Contact-Based Segmentation

Foot contact information can provide a useful temporal structure for
locomotion.

A simplified representation is:

    Foot Contact

    1 ────────┐      ┌────────
              │      │
    0         └──────┘

where:

    1 = foot in contact
    0 = foot not in contact

Contact transitions can help identify:

- Stance phases
- Swing phases
- Step boundaries
- Locomotion cycles

However, contact detection should not be interpreted as discovering a
human objective.

It is only a measurable property of the motion.

---

## 7. Step-Level Segmentation

Where reliable foot contacts are available, the motion can be divided
into step or gait-cycle segments.

Conceptually:

    Contact Event
         ↓
    Step
         ↓
    Contact Event
         ↓
    Next Step

A segment may therefore contain:

    t_start → t_end

with associated:

    Motion Features
    Contact Events
    Root Motion
    Joint Motion

This allows different steps and gait cycles to be compared.

---

## 8. Window-Based Segmentation

When reliable contact events are unavailable, fixed or overlapping
temporal windows may be used.

For example:

    Sequence
    ─────────────────────────────

    [ Window 1 ]
          [ Window 2 ]
                [ Window 3 ]

Window size and overlap should be configurable.

Window-based segmentation should be treated as a fallback rather than
automatically assuming that every fixed window represents a meaningful
behavioral unit.

---

## 9. Change-Based Segmentation

Changes in motion signals may also be used to identify boundaries.

Potential indicators include:

- Sudden changes in root velocity
- Changes in movement direction
- Large acceleration changes
- Foot contact transitions
- Motion pauses

Conceptually:

    Stable Motion
         ↓
    Change Detected
         ↓
    Segment Boundary

This approach may be useful for sequences containing transitions between
different movement phases.

---

## 10. Initial Segmentation Strategy

The initial implementation should use a simple and interpretable
procedure.

Priority:

    1. Contact-based segmentation when reliable
    2. Motion-based boundaries when necessary
    3. Temporal windows as fallback

The first implementation should avoid a complex learned segmentation
model.

The objective is to establish a reliable dataset before introducing
additional learning components.

---

## 11. Segment Quality Requirements

A valid segment should satisfy basic quality requirements.

### Temporal validity

- Minimum duration
- Correct frame ordering
- No missing frames

### Motion validity

- Sufficient motion content
- No severe reconstruction artifacts
- No unexpected discontinuities

### Locomotion validity

Where the segment is intended to represent walking:

- Appropriate root movement
- Meaningful foot motion
- Reasonable contact structure

Segments that fail these checks should be marked invalid or excluded.

---

## 12. Segment Metadata

Each segment should store metadata describing how it was generated.

Example:

```text
segment_id
dataset
sequence_id
start_frame
end_frame
duration
fps
segmentation_method
