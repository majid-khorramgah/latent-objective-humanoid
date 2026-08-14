# 02 — Problem Definition

## Learning Latent Human Objectives for Generalizable Humanoid Intelligence

**Date:** 14 August 2026

---

## 1. Problem Overview

The goal of this project is to investigate whether the underlying objective of human locomotion can be inferred from human demonstrations and subsequently optimized by a different humanoid robot using its own dynamics and physical constraints.

The problem is intentionally different from direct trajectory imitation.

### Direct imitation

    Human Trajectory
          ↓
    Trajectory Reproduction
          ↓
        H1 Motion

### Proposed direction

    Human Demonstration
          ↓
    Infer Human Objective
          ↓
    H1 Dynamics + Constraints
          ↓
          MPC
          ↓
       H1 Motion

The central question is whether the second approach can produce useful and generalizable humanoid behavior without requiring the H1 to reproduce the human trajectory.

---

## 2. Human Demonstration

Let a human locomotion demonstration be represented by a time-varying motion trajectory:

    τ_H = {x_H(t), u_H(t)} from t = 0 ... T

where:

- `x_H(t)` represents the human state or motion representation.
- `u_H(t)` represents available motion or dynamic information when available.
- `T` is the duration of the demonstration.

Depending on the available dataset, the human state may contain:

- Joint positions
- Joint velocities
- Root position and orientation
- Root velocity
- Joint accelerations
- Other physically meaningful motion features

The initial human data source is AMASS processed through SMPL-X.

---

## 3. Important Distinction: Trajectory vs Objective

The human demonstration is an observation of behavior.

It is NOT assumed that the observed trajectory itself is the objective.

Conceptually:

    Human Objective
          ↓
    Human Decision / Control
          ↓
    Human Motion
          ↓
    Observed Demonstration

Our inference problem attempts to reason in the reverse direction:

    Observed Human Motion
          ↓
    Infer Objective
          ↓
    Objective Representation

Therefore:

> The trajectory is evidence about the objective, not the objective itself.

---

## 4. Human Objective

Let the underlying human objective be represented by a cost function:

    J_H(τ; θ)

where:

- `τ` is a motion trajectory.
- `θ` represents unknown objective parameters.

The exact structure of `J_H` is intentionally left unspecified at this stage.

For example, it may eventually depend on features such as:

- energetic effort,
- smoothness,
- stability,
- task-related behavior,
- or other motion criteria.

However, these are hypotheses rather than assumptions.

We therefore do NOT define the objective in advance as:

    J_H =
        w1 Energy
      + w2 Stability
      + w3 Smoothness
      + w4 Robustness

The appropriate representation must be determined through the subsequent formulation and experiments.

---

## 5. Objective Inference Problem

Given a set of human demonstrations:

    D_H = {τ_H^1, τ_H^2, ..., τ_H^N}

the objective inference problem is to estimate an objective:

    J_hat_H

such that the inferred objective is consistent with the observed human behavior.

Conceptually:

    Human Demonstrations
            ↓
    Objective Inference
            ↓
       J_hat_H

The exact inference method is not fixed yet.

Possible methodological families include:

- Inverse Optimal Control (IOC)
- Inverse Reinforcement Learning (IRL)
- Other objective-learning approaches

The method will be selected after the mathematical problem and experimental requirements are fully defined.

---

## 6. Robot Problem

The target robot is the Unitree H1.

The robot has its own state:

    x_R

control input:

    u_R

and dynamics:

    x_dot_R = f_R(x_R, u_R)

where `f_R` represents the H1 dynamics.

The H1 also has physical and operational constraints.

These may include:

- Joint position limits
- Joint velocity limits
- Joint torque limits
- Contact constraints
- Kinematic constraints
- Balance-related constraints
- Actuator limitations
- Collision constraints

The exact constraint set will be specified according to the H1 model and the selected MPC formulation.

---

## 7. Objective Transfer

The central transfer problem is:

    Human
      ↓
    J_hat_H
      ↓
    H1

The objective inferred from human demonstrations should be expressed in a form that can be evaluated on the H1.

This does NOT mean transferring the human state trajectory directly.

Instead:

    Human Objective
          ↓
    Evaluate / interpret using H1 state
          ↓
    Optimize under H1 dynamics
          ↓
    H1-generated trajectory

This distinction is fundamental.

---

## 8. H1 Optimization Problem

Given the inferred objective `J_hat_H`, the H1 should generate a trajectory that minimizes the transferred objective while satisfying its own dynamics and constraints.

Conceptually:

    τ_R* =
        argmin J_hat_H(τ_R)

subject to:

    H1 Dynamics
    +
    H1 Physical Constraints

The exact mathematical form will be defined after determining how the objective is represented.

---

## 9. Role of MPC

MPC provides the model-based optimization mechanism for solving the robot-side problem.

At each control step, MPC uses:

- the current H1 state,
- the H1 dynamics model,
- physical constraints,
- and the inferred objective.

Conceptually:

    Current H1 State
           +
    Human-Derived Objective
           +
    H1 Dynamics
           +
    H1 Constraints
           ↓
          MPC
           ↓
    Feasible H1 Motion

The role of MPC is therefore to test whether the inferred human objective can actually be optimized by a different physical system.

MPC is not itself claimed as the research novelty.

---

## 10. Core Research Problem

The complete problem can therefore be summarized as:

### Given

A dataset of human locomotion demonstrations:

    D_H = {τ_H^1, ..., τ_H^N}

### Infer

A human-derived objective:

    J_hat_H

### Then solve

For the Unitree H1:

    τ_R* = argmin J_hat_H(τ_R)

subject to:

    x_dot_R = f_R(x_R, u_R)

and:

    x_R ∈ X_R
    u_R ∈ U_R
    contact / physical constraints

### Finally evaluate

Whether the resulting H1 behavior:

- is physically feasible,
- captures the intended behavioral characteristics,
- differs appropriately from the human trajectory,
- and generalizes to held-out conditions.

---

## 11. What Makes This Different from Trajectory Imitation?

Trajectory imitation attempts to minimize a difference such as:

    J_imitation =
        Distance(τ_R, τ_H)

The robot is therefore encouraged to reproduce the human trajectory.

Our proposed problem instead asks:

    Human Trajectory
          ↓
    Infer Objective
          ↓
    J_hat_H
          ↓
    Optimize for H1
          ↓
    τ_R

The resulting H1 trajectory does not need to equal the human trajectory.

The desired result is:

    Human Motion ≠ H1 Motion

but:

    Human Objective
          ≈
    H1 Objective

under different physical dynamics.

---

## 12. Generalization Problem

The final goal is not simply to reproduce the training demonstrations.

The objective should be evaluated under conditions that were not used during objective inference.

For example:

    Training Human Demonstrations
              ↓
        Infer Objective
              ↓
             H1
              ↓
      Held-Out Conditions

Possible held-out conditions may include:

- Unseen walking speeds
- Different locomotion conditions
- Different task parameters
- Other controlled environmental changes

The exact generalization protocol will be defined in:

    04_transfer_and_generalization.md

---

## 13. Success Criterion

The proposed approach is successful only if the experiments provide evidence that the inferred objective is useful beyond the demonstrations from which it was learned.

Success should therefore not be defined simply as:

> "The H1 can walk."

Instead, the key question is:

> **Does the human-derived objective provide a meaningful and generalizable criterion for generating H1 behavior under H1-specific dynamics and constraints?**

This distinction will guide the evaluation protocol.

---

## 14. Current Unknowns

The following elements are intentionally not fixed yet:

### Objective Representation

Unknown.

We do not yet know whether the objective should be:

- Hand-designed feature-based
- Parameterized cost
- Latent representation
- Neural objective
- Or another representation

### Inference Method

Unknown.

IOC, IRL, or another method may be appropriate.

### Objective Transfer Mechanism

Unknown.

The objective must be represented in a way that can be meaningfully evaluated on the H1.

### MPC Formulation

Partially defined conceptually, but the exact formulation is still open.

### Generalization Protocol

Not yet finalized.

These decisions will be made based on scientific justification and experimental feasibility.

---

## 15. Scope Control

The following are outside the immediate scope unless later evidence shows they are necessary:

- Real-robot H1 experiments
- Large-scale foundation models
- Unnecessary neural architectures
- Human motion generation
- Direct human trajectory imitation as the main method
- Universal transfer to all humanoid morphologies
- Solving arbitrary human tasks

The initial study should remain:

    Human Locomotion
          +
    Human Objective Inference
          +
    Unitree H1
          +
    Model-Based MPC
          +
    Controlled Generalization

---

## 16. Problem Statement

The current formal problem statement is:

> **Given human locomotion demonstrations, infer an objective that captures behaviorally meaningful properties of the demonstrated motion, and investigate whether that objective can be re-optimized by the Unitree H1 under its own dynamics and physical constraints to produce feasible and generalizable locomotion without directly reproducing the human trajectory.**

This is the problem that the following formulation stages will refine.

---

## 17. Next Step

The next step is to define precisely what is meant by:

> **Human Objective**

This requires determining what properties of human locomotion the objective is expected to capture and how those properties can be represented mathematically.

The next file is:

    03_objective_definition.md
