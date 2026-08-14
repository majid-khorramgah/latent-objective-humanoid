# Preliminary Research Gap

## Learning Latent Human Objectives for Generalizable Humanoid Intelligence

## 1. Literature Review

Following the suggested research direction, we reviewed 20 relevant papers across five areas:

1. Inverse Optimal Control (IOC)
2. Inverse Reinforcement Learning (IRL)
3. Human Motion / Locomotion Objectives
4. Model-Based Control / MPC
5. Humanoid / RoMeLa-related work

The literature shows that the main components of the proposed idea already exist as separate research directions.

### IOC / IRL

Human demonstrations can be used to infer objectives or rewards:

    Human Demonstrations
            ↓
      Objective / Reward

However, existing approaches often rely on predefined features, cost structures, or reward representations.

### Human Motion / Locomotion

Human locomotion can involve multiple movement criteria or goals.

Therefore, we should NOT assume in advance that the objective is:

    Energy + Stability + Smoothness + Robustness

These remain candidate hypotheses.

### Model-Based MPC

MPC can generate robot motion while explicitly considering:

- Robot dynamics
- Contacts
- Actuation limits
- Physical constraints

Therefore, MPC itself is not the proposed novelty.

### Humanoid / RoMeLa Work

Humanoid locomotion, RL, MPC, and dynamics-aware control are already established research areas.

Therefore, using these components individually is not sufficient as a novelty claim.

### Detailed Literature

- [Papers 1–10](./papers.md)
- [Papers 11–20](./papers1.md)
- [Literature Matrix 1–10](./literature_matrix.md)
- [Literature Matrix 11–20](./literature_matrix1.md)

---

## 2. What the Literature Tells Us

The literature provides two important building blocks:

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

This suggests a possible connection between human objective inference and model-based humanoid control.

The key distinction is:

    Direct Trajectory Transfer
            ✗

    Objective Transfer
            ✓

Instead of forcing the H1 to reproduce a human trajectory, we want to investigate whether the H1 can optimize a human-derived objective using its own dynamics and constraints.

---

## 3. Preliminary Research Gap

The current preliminary research question is:

> **Can an objective inferred from human locomotion demonstrations remain meaningful when it is re-optimized under the dynamics and physical constraints of a different humanoid robot?**

Conceptually:

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

This is a **preliminary research gap, not yet a confirmed novelty claim**.

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

Whether this represents a genuine research gap must be established through the subsequent formulation and experiments.

---

## 4. Why We Are Now at Phase 4

The first three milestones established the necessary experimental foundation.

**Milestone 1 — Isaac Lab / H1 Setup**

Established the NVIDIA Isaac Lab simulation environment and validated the Unitree H1 humanoid in simulation.

**Milestone 2 — H1 Locomotion Baseline**

Trained a PPO-based H1 locomotion policy and established a stable walking baseline.

This also revealed an important limitation:

> The policy learns a predefined robot reward rather than the underlying objectives expressed in human motion.

**Milestone 3 — Human Motion Representation**

Built an AMASS + SMPL-X pipeline that converts human motion capture data into structured 3D joint trajectories and temporal motion features suitable for objective inference.

Therefore:

    Robot + Simulation
            ↓
    H1 Locomotion Baseline
            ↓
    Human Demonstration Pipeline
            ↓
    Objective Inference
            ↑
          NOW

Phase 4 is therefore the point where the project moves from infrastructure and data preparation to the main research question.

---

## 5. Current Scope

The initial research will be simulation-based using:

- NVIDIA Isaac Lab
- Unitree H1
- AMASS / SMPL-X human motion
- Model-based MPC

A physical H1 is NOT required for the initial research validation.

The objective representation and inference method remain open questions and will be determined during problem formulation.

---

## 6. Next Step — 04_02 Problem Formulation

The next step is to convert the preliminary research direction into a specific, experimentally testable problem.

We will define:

1. What constitutes a human demonstration.
2. What information is extracted from the demonstration.
3. What "objective" means mathematically.
4. How the objective is represented.
5. How the objective is inferred.
6. How the objective is transferred to H1.
7. How H1 dynamics and constraints enter the optimization.
8. What the MPC solves.
9. What "generalization" means experimentally.
10. What baselines and evaluation metrics are required.

The goal is:

> **To formulate a small, rigorous, experimentally testable research problem.**

---

## 7. Current Status

**Milestone 1 — Isaac Lab / H1 Setup:** Complete

**Milestone 2 — H1 Locomotion Baseline:** Complete

**Milestone 3 — Human Motion Representation:** Complete

**04_01 Literature:** Complete for the current review scope

**20 relevant papers reviewed:** Yes

**Preliminary Research Gap:** Identified, not yet confirmed as a novel contribution

**04_02 Problem Formulation:** Next

**Final Research Question:** Not yet locked
