# Preliminary Research Gap

## Learning Latent Human Objectives for Generalizable Humanoid Intelligence

### Executive Summary

We reviewed 20 relevant papers across Inverse Optimal Control (IOC), Inverse Reinforcement Learning (IRL), human locomotion objectives, model-based MPC, and humanoid locomotion/control.

The literature provides the main components separately: objectives can be inferred from human demonstrations, and humanoid robots can generate motion using their own dynamics and constraints with model-based control.

Our preliminary research direction is to connect these components: **infer an underlying objective from human locomotion demonstrations, then optimize that objective on the Unitree H1 using its own dynamics and physical constraints through MPC, rather than directly imitating human trajectories.**

The next step is to formulate this idea as a **specific, experimentally testable problem** in `04_02_problem_formulation`.

---

## 1. Literature Review

We reviewed 20 relevant papers across five areas:

1. Inverse Optimal Control (IOC)
2. Inverse Reinforcement Learning (IRL)
3. Human Motion / Locomotion Objectives
4. Model-Based Control / MPC
5. Humanoid / RoMeLa-related work

### Main conclusions

**IOC / IRL**

Human demonstrations can be used to infer objectives or rewards:

    Observed Motion
          ↓
    Objective / Reward

However, many existing approaches depend on predefined features, cost structures, or reward representations.

**Human Motion / Locomotion**

Human movement may reflect multiple competing criteria or goals.

Therefore, we should NOT assume in advance that the objective is:

    Energy + Stability + Smoothness + Robustness

These remain candidate hypotheses.

**Model-Based MPC**

MPC can generate robot motion while considering:

- Robot dynamics
- Contacts
- Actuation limits
- Physical constraints

Therefore, MPC itself is not the proposed novelty.

**Humanoid Locomotion**

Humanoid locomotion, RL, MPC, and dynamics-aware control are already established research areas.

Therefore, the contribution should not be claimed from using any of these components individually.

### Detailed Literature

- [Papers 1–10](./papers.md)
- [Papers 11–20](./papers1.md)
- [Literature Matrix 1–10](./literature_matrix.md)
- [Literature Matrix 11–20](./literature_matrix1.md)

---

## 2. What We Learned

The literature already provides the main building blocks separately:

    Human Demonstrations
            ↓
        IOC / IRL
            ↓
      Objective / Reward


    Objective
        +
    Robot Dynamics
        +
    Physical Constraints
        ↓
       MPC
        ↓
    Humanoid Motion

The remaining question is whether these components can be connected through a transferable human objective.

The key distinction is:

    Direct Trajectory Transfer
            ✗

    Objective Transfer
            ✓

We do not want the H1 to reproduce the human trajectory.

Instead:

    Human Motion
         ↓
    Infer Objective
         ↓
    H1 + its own Dynamics
         ↓
        MPC
         ↓
    H1 generates its own motion

---

## 3. Preliminary Research Gap

The current preliminary research question is:

> **Can an objective inferred from human locomotion demonstrations remain meaningful when it is re-optimized under the dynamics and physical constraints of a different humanoid robot?**

Conceptually:

    Human Demonstrations
            ↓
    Learned Human Objective
            ↓
    H1 Dynamics + Constraints
            ↓
          MPC
            ↓
       H1 Behavior
            ↓
      Unseen Conditions

This is a **preliminary research gap**, not yet a confirmed novelty claim.

The potentially interesting combination is:

    Human Objective Inference
            +
    Different Humanoid Dynamics
            +
    Physical Constraints
            +
    Model-Based MPC
            +
    Generalization

Whether this combination represents a genuine research gap must be further established during problem formulation and experimental design.

---

## 4. Current Project Scope

The target robot is the Unitree H1.

The initial research will be simulation-based using:

- NVIDIA Isaac Lab
- Unitree H1
- Human motion demonstrations
- Model-based control / MPC

A physical H1 is NOT required for the initial research validation.

The first objective is to establish whether the proposed approach works in simulation before considering real-robot validation.

---

## 5. Human Data Direction

AMASS is a suitable source of human motion demonstrations.

An existing preprocessing pipeline provides:

    AMASS
      ↓
    SMPL-X
      ↓
    3D Joint Motion
      ↓
    Position / Velocity / Acceleration

This provides a useful starting point for the human-data stage.

However, we will NOT assume that a VAE, Transformer, large neural latent representation, or a predefined objective is necessary.

The appropriate objective representation remains an open research question.

---

## 6. What Is NOT Established as Novelty

The following are established research directions and are not, by themselves, novelty claims:

- IOC
- IRL
- Learning rewards from demonstrations
- Composite human movement objectives
- Humanoid MPC
- Humanoid RL
- Robot dynamics-aware control

The research contribution, if supported by further investigation, would instead concern the relationship between:

    Human Objective
          ↓
    Different Robot Dynamics
          ↓
    Constraint-Aware MPC
          ↓
    Generalizable Humanoid Behavior

---

## 7. Next Step — 04_02 Problem Formulation

The next stage is NOT yet implementation.

We will formally define:

1. What constitutes a human demonstration.
2. What information is extracted from the demonstration.
3. What "objective" means in this project.
4. How the objective is represented.
5. How the objective is inferred.
6. How the learned objective is transferred to H1.
7. How H1 dynamics and constraints enter the optimization.
8. What the MPC solves.
9. What "generalization" means experimentally.
10. What baselines and evaluation metrics are required.

The goal is to convert the preliminary research direction into a:

> **specific, experimentally testable problem.**

---

## 8. Current Status

    Literature Review
          ↓
       Completed
          ↓
    Prior Work Synthesized
          ↓
    Preliminary Gap Identified
          ↓
    Problem Formulation
          ↓
       NEXT STEP

### Status

**04_01 Literature: Complete for the current review scope**

**20 papers reviewed: Yes**

**Research Gap: Preliminary / Not yet fully established**

**04_02 Problem Formulation: Next**

**Final Research Question: Not locked yet**
