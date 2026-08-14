# Preliminary Research Gap

## Learning Latent Human Objectives for Generalizable Humanoid Intelligence

### Executive Summary

The project has progressed through three foundational milestones:

**Milestone 1 — Isaac Lab / H1 Setup:**  
Established the NVIDIA Isaac Lab simulation environment and validated the Unitree H1 humanoid in simulation.

**Milestone 2 — H1 Locomotion Baseline:**  
Trained a PPO-based H1 locomotion policy and established a stable walking baseline. This showed an important limitation: the policy learns a predefined robot reward rather than the underlying objectives expressed in human motion.

**Milestone 3 — Human Motion Representation:**  
Built an AMASS + SMPL-X pipeline that converts human motion capture data into structured 3D joint trajectories and temporal motion features suitable for objective inference.

The project now moves to the main research question:

> **Can an underlying objective inferred from human locomotion demonstrations be re-optimized by the Unitree H1 using its own dynamics and physical constraints, rather than directly imitating human trajectories?**

---

## 1. Literature Review

We reviewed 20 relevant papers across five areas:

1. Inverse Optimal Control (IOC)
2. Inverse Reinforcement Learning (IRL)
3. Human Motion / Locomotion Objectives
4. Model-Based Control / MPC
5. Humanoid / RoMeLa-related work

The literature provides the main components separately:

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

The literature also shows that human locomotion may involve multiple movement criteria or goals.

Therefore, we will NOT assume in advance that the objective is:

    Energy + Stability + Smoothness + Robustness

These remain candidate hypotheses.

Detailed reviews:

- [Papers 1–10](./papers.md)
- [Papers 11–20](./papers1.md)
- [Literature Matrix 1–10](./literature_matrix.md)
- [Literature Matrix 11–20](./literature_matrix1.md)

---

## 2. Preliminary Research Gap

The existing literature establishes objective/reward inference from demonstrations and model-based humanoid control as important research directions.

The preliminary gap we want to investigate is the connection between them:

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

The key distinction is:

    Direct Trajectory Transfer
            ✗

    Objective Transfer
            ✓

Instead of forcing H1 to reproduce human trajectories, we investigate whether H1 can use a human-derived objective to generate its own physically feasible motion.

> **This is a preliminary research gap, not yet a confirmed novelty claim.**

---

## 3. Current Scope

The initial validation will be simulation-based using:

- NVIDIA Isaac Lab
- Unitree H1
- AMASS / SMPL-X human motion
- Model-based MPC

A physical H1 is not required for the initial research validation.

The objective representation and inference method remain open questions and will be determined during problem formulation.

---

## 4. Next Step — 04_02 Problem Formulation

The next step is to convert the preliminary research direction into a specific, experimentally testable problem.

We will define:

1. The human demonstration representation.
2. The objective representation.
3. The objective inference method.
4. The transfer mechanism to H1.
5. The H1 dynamics and constraints.
6. The MPC formulation.
7. The generalization setting.
8. The baselines and evaluation metrics.

### Current Status

**Milestone 1 — Isaac Lab / H1 Setup:** Complete

**Milestone 2 — H1 Locomotion Baseline:** Complete

**Milestone 3 — Human Motion Representation:** Complete

**04_01 Literature:** Complete for the current review scope

**20 relevant papers reviewed:** Yes

**Preliminary Research Gap:** Identified, not yet confirmed as a novel contribution

**04_02 Problem Formulation:** Next

**Final Research Question:** Not yet locked
