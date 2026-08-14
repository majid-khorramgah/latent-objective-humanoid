# Preliminary Research Gap

## Learning Latent Human Objectives for Generalizable Humanoid Intelligence

### 1. Research Motivation

The original research idea is to move beyond direct human trajectory imitation.

Instead of asking:

    "How can the H1 reproduce the human trajectory?"

we ask:

    "What underlying objective explains the human motion,
     and can the H1 optimize that objective using its own
     dynamics and physical constraints?"

The intended framework is:

    Human Demonstrations
            ↓
    Infer Human Objective
            ↓
    H1 Dynamics + Constraints
            ↓
    Model-Based MPC
            ↓
    H1 Behavior
            ↓
    Generalization


---

## 2. What We Reviewed

We reviewed approximately 20 papers across five main areas:

### 1. Inverse Optimal Control (IOC)

IOC shows that an objective/cost can be inferred from observed behavior.

Key lesson:

    Observed Motion → Objective

However, many approaches rely on predefined objective features or assumptions about the cost representation.

---

### 2. Inverse Reinforcement Learning (IRL)

IRL provides more general frameworks for learning rewards from demonstrations, including probabilistic and deep reward representations.

Key lesson:

    Demonstrations → Learned Reward

However, reward learning alone does not solve the human-to-humanoid transfer problem.

---

### 3. Human Motion / Locomotion Objectives

Human movement studies show that locomotion can be explained using multiple movement criteria and potentially multiple movement goals.

Key lesson:

    Human locomotion ≠ necessarily one simple objective

Therefore, we should NOT assume in advance that the human objective is:

    Energy + Stability + Smoothness + Robustness

These remain candidate hypotheses.

---

### 4. Model-Based Control / MPC

Recent work demonstrates that whole-body MPC can generate humanoid/legged motion while explicitly considering:

- Robot dynamics
- Contacts
- Actuation limits
- Physical constraints

Key lesson:

    Objective
        +
    Robot Dynamics
        +
    Constraints
        ↓
       MPC
        ↓
    Robot Motion

Therefore, MPC itself is not the proposed novelty.

---

### 5. RoMeLa / Humanoid Locomotion

Recent humanoid work demonstrates successful model-based and learning-based locomotion on complex humanoid systems.

Key lesson:

Humanoid locomotion, robot-specific dynamics, MPC, and RL are already established research areas.

Therefore, the project should not claim novelty from using any of these components individually.


---

## 3. What We Learned

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
    Constraints
        ↓
       MPC
        ↓
    Humanoid Motion

The remaining question is whether these components can be connected through a transferable human objective.

---

## 4. Preliminary Research Gap

The current preliminary gap is:

> Can an objective inferred from human locomotion demonstrations remain meaningful when it is re-optimized under the dynamics and physical constraints of a different humanoid robot?

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

The important distinction is that we do NOT directly transfer the human trajectory.

Instead:

    Human trajectory
          ↓
    infer objective
          ↓
    H1 generates its own motion

This may allow the robot to satisfy the underlying behavioral objective without reproducing human morphology or dynamics.

---

## 5. What Is NOT Established Yet

The following are NOT established as novelty claims:

- IOC itself
- IRL itself
- Learning rewards from demonstrations
- Composite human movement objectives
- Humanoid MPC
- Humanoid RL
- Robot dynamics-aware control

The potentially interesting contribution is the combination:

    Human Objective Inference
            +
    Different Humanoid Dynamics
            +
    Physical Constraints
            +
    Model-Based MPC
            +
    Generalization

However:

> This is a preliminary research gap, NOT YET a confirmed novelty claim.

The remaining work must determine whether closely related human-objective-to-humanoid transfer methods already exist.

---

## 6. Current Project Scope

The target robot is the Unitree H1.

The initial research will be simulation-based using:

- NVIDIA Isaac Lab
- Unitree H1
- Human motion data
- Model-based control / MPC

A physical H1 is NOT required for the initial research validation.

The first goal is to establish whether the proposed idea works in simulation before considering real-robot validation.

---

## 7. Human Data Direction

AMASS is a suitable source of human motion demonstrations.

An existing preprocessing pipeline has already been developed:

    AMASS
      ↓
    SMPL-X
      ↓
    3D Joint Motion
      ↓
    Position / Velocity / Acceleration

This provides a useful starting point for the human-data stage.

However, we will NOT assume that a large neural latent representation, VAE, Transformer, or predefined objective is necessary.

The appropriate objective representation remains an open research question.

---

## 8. Next Step — 04_02 Problem Formulation

The next stage is NOT yet implementation.

We will formally define:

1. What constitutes a human demonstration.
2. What information is used from the demonstration.
3. What "objective" means in this project.
4. How the objective will be represented.
5. How the objective is inferred.
6. How the learned objective is transferred to H1.
7. How H1 dynamics and constraints enter the optimization.
8. What MPC solves.
9. What "generalization" means experimentally.
10. What baselines and evaluation metrics are required.

The goal is to convert the preliminary research idea into a:

> **specific, experimentally testable problem.**

---

## 9. Current Status

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

**Research Gap: Preliminary / Not yet fully established**

**04_02 Problem Formulation: Next**

**Final Research Question: Not locked yet**
