# Problem Definition

## Learning a Transferable Human Objective from Motion Demonstrations

### 1. Purpose

The purpose of this stage is to convert the preliminary research gap into
a precise computational problem.

The central question is:

> Can a behavioral objective inferred from human locomotion demonstrations
> be transferred to a humanoid robot with different morphology, dynamics,
> and physical constraints?

The project therefore does NOT aim to reproduce human trajectories directly.

Instead, the goal is:

    Human Demonstrations
            ↓
    Motion Representation
            ↓
    Objective Inference
            ↓
    Human Objective
            ↓
    H1 Dynamics + Constraints
            ↓
           MPC
            ↓
       H1-generated Motion


---

# 2. Problem Statement

Let a set of human locomotion demonstrations be:

    D_H = {τ_1, τ_2, ..., τ_N}

where each trajectory τ represents a human movement sequence.

Each demonstration contains observable motion information such as:

- Joint positions
- Root motion
- Joint velocities
- Joint accelerations
- Foot trajectories
- Temporal structure
- Walking speed
- Step timing
- Other kinematic and dynamic descriptors

The objective is to infer a function:

    J_H(τ, c; θ)

that captures behavioral preferences expressed by the demonstrations.

Here:

- τ = candidate motion trajectory
- c = task/context
- θ = parameters of the objective representation

The inferred objective should explain the observed demonstrations
without requiring direct trajectory reproduction.


---

# 3. What AMASS Provides

AMASS is used as the source of human demonstrations.

The existing AMASS + SMPL-X pipeline provides:

    AMASS
      ↓
    SMPL-X
      ↓
    3D Human Joints
      ↓
    Temporal Motion Data

The current preprocessing pipeline already provides:

- 3D joint positions
- Velocity
- Acceleration
- Motion energy
- Frame rate
- Full temporal sequences

These outputs are useful, but they are NOT themselves the learned
human objective.

The distinction is:

    AMASS data
        ↓
    Observable motion descriptors
        ↓
    Objective inference
        ↓
    Human objective


---

# 4. What We Are NOT Trying to Do

The project does NOT simply learn:

    Energy
    +
    Smoothness
    +
    Stability

and call this the human objective.

These quantities have already been extensively investigated in
human movement and locomotion research.

They may still be used as candidate measurable descriptors when
necessary, but they are not assumed to constitute the final objective.

Similarly, the project does NOT assume that:

- Energy is the dominant human preference.
- Stability is the dominant human preference.
- Smoothness is the dominant human preference.
- Humans share one universal locomotion objective.
- A VAE is required.
- A Transformer is required.
- A deep neural reward is required.
- The objective must be linear.
- The objective must be identical across tasks or people.


---

# 5. The Key Distinction

There are three different concepts in this project.

## 5.1 Motion Data

What the human actually did.

Example:

    Joint trajectories
    Foot trajectories
    Walking speed
    Step timing


## 5.2 Motion Descriptors

Quantities computed from the demonstrations.

Examples:

    Velocity
    Acceleration
    Step length
    Cadence
    Foot placement
    COM-related quantities
    Temporal coordination


## 5.3 Objective

A function that explains why one behavior is preferred over
another.

Conceptually:

    Motion Descriptors
            ↓
    Behavioral Preference
            ↓
         Objective


This distinction is fundamental.

We are not trying to turn every measured quantity into an objective.


---

# 6. Human Demonstrations

The initial demonstration set will focus on human locomotion.

A demonstration may contain:

    τ_i =
    {q(t), q_dot(t), q_ddot(t), root(t), feet(t), ...}

where:

- q(t) = human joint configuration
- q_dot(t) = joint velocity
- q_ddot(t) = joint acceleration
- root(t) = root/body motion
- feet(t) = foot trajectories

The demonstrations should preferably contain locomotion under
different conditions or with meaningful variation.

This variation is important because objective inference requires
more information than observing one nearly identical trajectory.


---

# 7. What Should Be Extracted from AMASS?

The existing AMASS pipeline should be extended from simple motion
processing toward objective-relevant descriptors.

The first stage should extract measurable quantities such as:

## Kinematic descriptors

- Joint positions
- Joint velocities
- Joint accelerations
- Root position
- Root orientation
- Body segment orientations


## Locomotion descriptors

- Walking speed
- Step length
- Step duration
- Cadence
- Stride timing
- Foot trajectories
- Foot placement


## Whole-body descriptors

- Center-of-mass-related quantities
- Body posture
- Whole-body coordination
- Relative motion between body segments


## Temporal descriptors

- Phase relationships
- Periodicity
- Motion timing
- Inter-joint coordination


These descriptors form the observation space from which objective
inference can be performed.


---

# 8. Why These Features?

The purpose of extracting these quantities is not to manually define
the human objective.

Instead, they provide measurable evidence about the behavior.

For example:

    Human A
        ↓
    faster walking
    shorter step duration

    Human B
        ↓
    slower walking
    different foot placement

If the task is the same, these differences may contain information
about different behavioral preferences.

Therefore, demonstrations with behavioral variation are important.


---

# 9. Objective Inference

The central computational problem is to infer an objective that
explains the demonstrations.

Conceptually:

    Demonstrations
          +
    Motion Descriptors
          ↓
    Objective Inference
          ↓
    J_H


A simple initial formulation may be:

    J_H(τ, c; θ)
        = Σ_i θ_i φ_i(τ, c)

where:

- φ_i = measurable motion descriptors
- θ_i = learned parameters

However, this linear formulation is an initial experimental model,
not a final assumption.

If it cannot adequately explain the demonstrations, more expressive
representations can be investigated later.


---

# 10. Why Demonstrations Alone Are Not Enough

A major issue in objective inference is that a single trajectory
usually does not uniquely determine the objective.

Many different objectives can produce similar behavior.

Therefore, the project should use:

    Multiple Demonstrations
            +
    Behavioral Variation
            +
    Controlled Context
            ↓
    Objective Identification


This is important for avoiding an objective that simply memorizes
the observed trajectory.


---

# 11. Objective Identifiability

The project must explicitly consider objective identifiability.

Suppose two objectives produce nearly identical behavior:

    J_1 → τ

    J_2 → τ

Then the demonstrations may not contain enough information to
distinguish between J_1 and J_2.

Therefore, objective inference should be evaluated not only by
whether the learned objective fits the demonstrations, but also by
whether it can distinguish meaningful behavioral alternatives.


---

# 12. Human-to-Robot Transfer

After an objective is inferred from human demonstrations, it must
be expressed in a form that can be evaluated for the H1.

The intended transfer is:

    Human Demonstrations
            ↓
    Human Objective
            ↓
    Robot-compatible Objective
            ↓
    H1 Dynamics
            ↓
    Physical Constraints
            ↓
           MPC
            ↓
        H1 Motion


The H1 is NOT required to reproduce the human joint trajectory.

Instead, it should generate its own feasible motion that optimizes
the transferred objective.


---

# 13. Human Morphology vs. Behavioral Objective

A critical requirement is to separate human-specific quantities
from behavioral quantities.

For example:

Human-specific:

    Exact human joint angles
    Human limb lengths
    Human joint torques

Potentially transferable:

    Walking speed
    Step timing
    Foot placement behavior
    Body stability characteristics
    Task achievement
    Temporal coordination


This distinction is essential for the proposed research direction.


---

# 14. Robot-Specific Optimization

Once the objective is transferred, the H1 uses its own dynamics.

Let the H1 state be:

    x_t

and control input be:

    u_t

with dynamics:

    x_{t+1} = f_H1(x_t, u_t)

The robot must satisfy constraints such as:

    x_t ∈ X

    u_t ∈ U

    contact constraints

    actuator limits

    balance / feasibility constraints


The optimization problem becomes conceptually:

    minimize
        J_H1(x_0:T, u_0:T)

    subject to

        x_{t+1} = f_H1(x_t, u_t)

        x_t ∈ X

        u_t ∈ U

        contact constraints


This is where MPC enters the framework.


---

# 15. Role of MPC

MPC is not responsible for discovering the human objective.

Its role is to optimize the inferred objective while respecting
the physical properties of the H1.

Therefore:

    Objective Learning
            ↓
        defines WHAT
        is preferred

    MPC
            ↓
        determines HOW
        H1 can achieve it


This separation is central to the project.


---

# 16. Generalization

Generalization is defined as the ability of the inferred objective
to remain useful when conditions change.

Possible sources of variation include:

### Robot variation

    Human
      ↓
    H1

and potentially later:

    H1
    ↓
    Other humanoid morphology


### Motion variation

    Different walking speeds
    Different trajectories
    Different initial states


### Environmental variation

    Different terrain
    Different constraints
    External disturbances


The first experiments should remain controlled.

We should not attempt to demonstrate all forms of generalization
simultaneously.


---

# 17. Initial Experimental Strategy

The first experiment should be deliberately small.

### Step 1

Select a controlled subset of AMASS locomotion demonstrations.

### Step 2

Convert demonstrations into a common representation.

### Step 3

Extract objective-relevant motion descriptors.

### Step 4

Define a small candidate objective representation.

### Step 5

Infer objective parameters from demonstrations.

### Step 6

Validate whether the inferred objective explains held-out
human demonstrations.

### Step 7

Transfer the objective to the H1.

### Step 8

Optimize it using H1 dynamics and constraints.

### Step 9

Compare the resulting H1 behavior against appropriate baselines.


---

# 18. Baselines

The problem should eventually be evaluated against at least:

## Baseline 1 — Standard RL

H1 learns locomotion using a conventional robot reward.

    H1
     ↓
    PPO
     ↓
    Walking


## Baseline 2 — Direct Motion Imitation

H1 attempts to reproduce human motion.

    Human Motion
         ↓
    Imitation
         ↓
    H1 Motion


## Proposed Approach

    Human Demonstrations
            ↓
    Objective Inference
            ↓
    H1 Dynamics
            ↓
           MPC
            ↓
        H1 Motion


The comparison should determine whether objective transfer provides
an advantage over direct trajectory imitation or robot-specific
reward learning.


---

# 19. Success Criteria

The initial problem will be considered successful only if the
inferred objective satisfies several requirements.

### Human explanation

The objective should explain or predict held-out human behavior
better than appropriate alternatives.

### Transferability

The objective should remain meaningful when evaluated on H1.

### Physical feasibility

The resulting H1 behavior must satisfy:

- Dynamics
- Contacts
- Actuation limits
- Physical constraints


### Generalization

The H1 behavior should remain useful under at least one previously
unseen condition.

### Non-triviality

The result should demonstrate something beyond simply reproducing
the human trajectory.


---

# 20. Core Research Problem

The complete problem can therefore be summarized as:

    Given:

        Human locomotion demonstrations D_H

    Infer:

        A behavioral objective J_H

    Such that:

        J_H explains the demonstrations

    and:

        J_H remains meaningful when evaluated
        under H1 dynamics and constraints.

    Then:

        Use MPC to generate feasible H1 behavior.


Formally:

    D_H
      ↓
    Infer J_H
      ↓
    Optimize J_H under f_H1
      ↓
    Generate τ_H1


The important requirement is:

    τ_H1 ≠ τ_H

in general.

The H1 is allowed to produce a different trajectory because its
morphology and dynamics are different.

The goal is to transfer the behavioral objective, not the human
trajectory.


---

# 21. Current Research Hypothesis

The initial hypothesis is:

> A sufficiently informative representation of human locomotion
> demonstrations may allow inference of behavioral preferences that
> remain meaningful when optimized under the dynamics and physical
> constraints of a humanoid robot.

This hypothesis remains to be experimentally tested.


---

# 22. Relation to the Existing AMASS Pipeline

The existing Milestone 3 pipeline is therefore retained.

Current:

    AMASS
      ↓
    SMPL-X
      ↓
    3D Joints
      ↓
    Position / Velocity / Acceleration


The next extension is:

    3D Joints
        ↓
    Locomotion Descriptors
        ↓
    Demonstration Dataset
        ↓
    Objective Inference


Therefore, the existing AMASS work is not discarded.

It becomes the data-processing layer of the objective-learning
problem.


---

# 23. What Is Still Open

The following questions remain open and will be resolved experimentally:

1. Which AMASS sequences should be selected?
2. Which motion descriptors contain useful information?
3. Which descriptors are transferable to H1?
4. How much behavioral variation is required?
5. What objective representation should be used?
6. Which IOC / IRL formulation is appropriate?
7. How should context be represented?
8. How should human objective terms be mapped to H1 quantities?
9. Which MPC formulation is computationally practical?
10. What level of generalization can be demonstrated?


---

# 24. Important Scope Constraint

The project will not attempt to solve all of these questions
simultaneously.

The initial goal is only to establish:

    Demonstrations
          ↓
    Objective inference
          ↓
    Objective validation


before attempting full humanoid transfer.

Only after objective inference is shown to be meaningful should
the H1 + MPC transfer experiment be expanded.


---

# 25. Current Status

Problem definition:

**Formulated at a preliminary experimental level**

Human data:

**AMASS + SMPL-X pipeline available**

Motion representation:

**3D joints + temporal features available**

Objective representation:

**Not yet finalized**

Objective inference method:

**Not yet finalized**

H1 transfer:

**Planned**

MPC formulation:

**Planned**

Generalization experiment:

**Not yet finalized**

---

# 26. Next Step

The next step is to define the exact objective representation and
the inference experiment.

Specifically:

    AMASS demonstrations
            ↓
    Select controlled locomotion subset
            ↓
    Extract candidate descriptors
            ↓
    Define objective hypothesis
            ↓
    Infer objective parameters
            ↓
    Validate on held-out demonstrations


Only after this step is validated will the project proceed to:

    Human Objective
          ↓
    H1-compatible Objective
          ↓
    MPC
          ↓
    Generalizable H1 Behavior


## Status

**02_problem_definition: Complete — preliminary formulation**

**Objective representation: Open research variable**

**Inference method: Open research variable**

**H1 transfer: Future stage**

**Next document: `03_objective_definition.md`**
