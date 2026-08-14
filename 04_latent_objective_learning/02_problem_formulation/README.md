# 04_02 Problem Formulation

## Learning Latent Human Objectives for Generalizable Humanoid Intelligence

### Purpose

This stage converts the preliminary research gap identified in the literature review into a specific and experimentally testable research problem.

The central idea is:

    Human Demonstrations
            ↓
    Infer Human Objective
            ↓
    H1 Dynamics + Constraints
            ↓
          MPC
            ↓
       H1 Behavior
            ↓
      Generalization

The goal is NOT to directly imitate human trajectories.

Instead, the objective underlying human locomotion will be investigated and then optimized using the dynamics and physical constraints of the Unitree H1.

---

## Starting Point

The literature review established that:

- IOC and IRL can infer objectives or rewards from demonstrations.
- Human locomotion may reflect multiple movement criteria or goals.
- Model-based MPC can optimize objectives under robot dynamics and physical constraints.
- Humanoid locomotion and robot-specific control are already established research areas.

The preliminary research gap is therefore:

> Can an objective inferred from human locomotion demonstrations remain meaningful when it is re-optimized under the dynamics and physical constraints of a different humanoid robot?

This question is not yet considered a confirmed novelty claim.

---

## Problem Formulation Tasks

This stage will determine:

1. What constitutes a human demonstration.
2. Which human motion data are used.
3. What is meant by the underlying human objective.
4. How the objective is represented.
5. How the objective is inferred from demonstrations.
6. How the inferred objective is transferred to H1.
7. How H1 dynamics and physical constraints are incorporated.
8. What optimization problem the MPC solves.
9. What constitutes successful objective transfer.
10. How generalization will be experimentally evaluated.

---

## Important Constraints

We will not assume in advance that the human objective is:

    Energy
    + Stability
    + Smoothness
    + Robustness

These are candidate hypotheses only.

The objective representation and inference method must be justified by the literature and the experimental problem.

We will also avoid introducing unnecessary model complexity before the core problem is clearly defined.

---

## Experimental Setting

The initial validation will be simulation-based.

Target robot:

    Unitree H1

Simulation environment:

    NVIDIA Isaac Lab

Human motion source:

    AMASS / SMPL-X

Control direction:

    Model-Based MPC

A physical H1 robot is not required for the initial research validation.

---

## Expected Output

The output of this stage will be a precise problem formulation defining:

    Input
      ↓
    Objective Inference
      ↓
    Objective Representation
      ↓
    H1 Optimization
      ↓
    Evaluation

The formulation should be sufficiently precise that the proposed method can be implemented and experimentally compared against appropriate baselines.

---

## Current Status

**04_01 Literature:** Complete for the current review scope

**Preliminary Research Gap:** Identified

**04_02 Problem Formulation:** In Progress

**Final Research Question:** Not yet locked

**Objective Representation:** Unknown

**Inference Method:** Unknown

**MPC Formulation:** To be defined

**Generalization Protocol:** To be defined
