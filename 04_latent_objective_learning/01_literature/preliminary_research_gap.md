# Preliminary Research Gap

## Learning Latent Human Objectives for Generalizable Humanoid Intelligence

### Executive Summary

The project has progressed through three foundational milestones:

**Milestone 1 — Isaac Lab / H1 Setup:**  
Established the NVIDIA Isaac Lab simulation environment and validated the Unitree H1 humanoid in simulation.

**Milestone 2 — H1 Locomotion Baseline:**  
Trained a PPO-based H1 locomotion policy and established a stable walking baseline. This also showed an important limitation: the policy learns a predefined robot reward rather than the underlying objectives expressed in human motion.

**Milestone 3 — Human Motion Representation:**  
Built an AMASS + SMPL-X pipeline that converts human motion capture data into structured 3D joint trajectories and temporal motion features suitable for objective inference.

These milestones establish the **robot, locomotion baseline, and human demonstration pipeline**. The research question therefore becomes meaningful at the next stage:

> **Can we infer an underlying objective from human locomotion demonstrations and optimize that objective on the H1 using its own dynamics and physical constraints, rather than directly imitating human trajectories?**

The next step is **04_02 Problem Formulation**, where this question will be converted into a specific, experimentally testable problem.

---

## 1. Why the Project Reaches Phase 4

The first three milestones were not intended to be the final research contribution. They establish the necessary experimental infrastructure.

The progression is:

    Milestone 1
    Isaac Lab + Unitree H1
            ↓
    Robot simulation foundation


    Milestone 2
    H1 locomotion baseline
            ↓
    Known robot control baseline


    Milestone 3
    AMASS + SMPL-X
            ↓
    Human motion demonstrations
            ↓
    Structured motion representation


    Phase 4
    Human motion
            ↓
    Infer underlying objective
            ↓
    H1 dynamics + constraints
            ↓
    Model-Based MPC
            ↓
    H1 behavior

Therefore, Phase 4 is the point where the project moves from **infrastructure and representation** to the actual research question.

---

## 2. Milestone 1 — Isaac Lab and H1 Setup

Milestone 1 established the simulation foundation using:

- NVIDIA Isaac Sim
- NVIDIA Isaac Lab
- Unitree H1
- GPU-accelerated simulation
- RSL-RL
- PPO

The H1 was successfully loaded and simulated in Isaac Lab.

### Research role

This milestone answers:

> **Can we reliably conduct the planned humanoid experiments in simulation?**

Result:

**Yes.**

The H1 simulation environment is operational and can be used for subsequent control experiments.

---

## 3. Milestone 2 — H1 Locomotion Baseline

Milestone 2 trained the Unitree H1 using PPO in:

    Isaac-Velocity-Flat-H1-v0

The policy was trained for approximately:

    5000 iterations
    450M+ simulation steps

The resulting policy achieved stable locomotion and velocity tracking.

### Research role

This milestone establishes a baseline for robot locomotion.

More importantly, it reveals the limitation motivating the research:

> The H1 can learn to walk using a predefined robot reward, but this reward does not necessarily represent the underlying objectives expressed by human locomotion.

For example, the robot can learn:

    "maximize the predefined locomotion reward"

without learning:

    "what makes human locomotion efficient,
     stable, natural, or adaptable?"

Therefore:

    PPO baseline
          ↓
    Robot learns a predefined objective

but our research asks:

    Human demonstrations
          ↓
    Infer the underlying objective

This distinction motivates Phase 4.

---

## 4. Milestone 3 — Human Motion Representation

Milestone 3 established the human-data pipeline using:

    AMASS
      ↓
    SMPL-X
      ↓
    3D Joint Motion
      ↓
    Position / Velocity / Acceleration

The pipeline converts human motion capture sequences into structured representations suitable for analysis and future learning.

### Research role

This milestone answers:

> **Can human demonstrations be converted into a representation from which an objective could potentially be inferred?**

Result:

**Yes, as a starting point.**

However, Milestone 3 does NOT yet infer the human objective.

It provides the input to Phase 4:

    Human Demonstration
          ↓
    Structured Motion
          ↓
    Objective Inference       ← CURRENT RESEARCH PROBLEM

---

## 5. What We Reviewed

We reviewed approximately 20 relevant papers across five main areas:

1. Inverse Optimal Control (IOC)
2. Inverse Reinforcement Learning (IRL)
3. Human Motion / Locomotion Objectives
4. Model-Based Control / MPC
5. Humanoid / RoMeLa-related work

### Literature Review

- [Papers 1–10](./papers.md)
- [Papers 11–20](./papers1.md)
- [Literature Matrix 1–10](./literature_matrix.md)
- [Literature Matrix 11–20](./literature_matrix1.md)

---

## 6. What the Literature Already Provides

The literature already provides important components of the proposed framework.

### IOC / IRL

Human demonstrations can be used to infer objectives or rewards:

    Observed Motion
          ↓
    Objective / Reward

However, many approaches rely on predefined features, cost structures, or reward representations.

### Human Motion / Locomotion

Human movement can be explained using multiple movement criteria or goals.

Therefore, we should NOT assume in advance that the human objective is:

    Energy + Stability + Smoothness + Robustness

These remain candidate hypotheses.

### Model-Based MPC

MPC can generate robot motion while explicitly considering:

- Robot dynamics
- Contacts
- Actuation limits
- Physical constraints

Therefore, MPC itself is not the proposed novelty.

### Humanoid Locomotion

Humanoid locomotion, RL, MPC, and dynamics-aware control are already established research areas.

Therefore, the contribution should not be claimed from using any of these components individually.

---

## 7. What the Literature Suggests

The existing literature largely covers the following two directions separately:

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

This suggests a potential connection:

    Human Demonstrations
            ↓
    Infer Human Objective
            ↓
    Different Robot Dynamics
            ↓
          MPC
            ↓
    Robot Behavior

The important question is whether an objective inferred from human locomotion remains useful when optimized by a robot with different morphology, dynamics, actuation, and physical constraints.

---

## 8. Preliminary Research Gap

The current preliminary research gap is:

> **Can an objective inferred from human locomotion demonstrations remain meaningful when it is re-optimized under the dynamics and physical constraints of a different humanoid robot?**

The key distinction from direct imitation is:

    Human Trajectory
          ↓
    Direct Imitation
          ↓
    Robot Motion

versus:

    Human Trajectory
          ↓
    Infer Underlying Objective
          ↓
    H1 Dynamics + Constraints
          ↓
          MPC
          ↓
    H1 Generates Its Own Motion

The goal is therefore not to make the H1 move like a human joint-by-joint.

The goal is to determine whether the H1 can pursue a **human-derived objective** while producing motion that is physically appropriate for the H1.

---

## 9. Why This Could Matter for Generalization

A trajectory is strongly tied to the body that produced it.

For example:

    Human body
        ↓
    Human trajectory

If the robot has different:

- limb lengths
- mass distribution
- joint limits
- actuator capabilities
- contact dynamics

then directly copying the trajectory may not be physically appropriate.

An objective may be more transferable than the trajectory itself.

Conceptually:

    Human
    Motion
      ↓
    Objective
      ↓
    ┌───────────────┐
    │               │
    H1             Other
    dynamics       humanoid
    │               │
    ↓               ↓
    Own motion     Own motion

This is the hypothesis that motivates the generalization experiments.

However:

> **Whether an inferred human objective is actually more transferable than a trajectory remains unknown and must be experimentally tested.**

---

## 10. What Is NOT Established as Novelty

The following are NOT established as novel contributions by themselves:

- IOC
- IRL
- Learning rewards from demonstrations
- Composite human movement objectives
- Human locomotion objective inference
- Humanoid MPC
- Humanoid RL
- Robot dynamics-aware control
- AMASS-based human motion processing

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

> **This remains a preliminary research gap, not a confirmed novelty claim.**

The literature review does not yet justify claiming that this exact formulation has never been attempted.

---

## 11. Current Project Scope

The initial target system is:

    Robot:
    Unitree H1

    Simulation:
    NVIDIA Isaac Sim / Isaac Lab

    Human Data:
    AMASS / SMPL-X

    Control:
    Model-Based MPC

The initial validation will be entirely simulation-based.

A physical H1 is NOT required for the initial research validation.

The purpose of the simulation study is to determine whether the proposed objective-transfer concept is experimentally supported before considering real-robot deployment.

---

## 12. Human Data Direction

AMASS provides a suitable starting point for human locomotion demonstrations.

The existing pipeline produces:

    AMASS
      ↓
    SMPL-X
      ↓
    3D Joint Motion
      ↓
    Position
    Velocity
    Acceleration

This data can therefore serve as input to the objective-inference stage.

However, we will NOT assume that a:

- VAE
- Transformer
- large neural latent representation
- or predefined objective structure

is necessary.

The appropriate objective representation remains an open research question.

This will be determined during `04_02_problem_formulation`.

---

## 13. Next Step — 04_02 Problem Formulation

The next stage is not yet large-scale implementation.

We will first define a specific and testable formulation.

We need to determine:

1. What constitutes a human locomotion demonstration.
2. Which information is extracted from it.
3. What "objective" means mathematically.
4. Whether the objective is parameterized or latent.
5. How the objective is inferred.
6. What assumptions are made about the objective.
7. How the objective is transferred to H1.
8. How H1 dynamics enter the optimization.
9. How physical constraints are enforced.
10. What MPC actually solves.
11. What constitutes successful transfer.
12. What "generalization" means experimentally.
13. Which baselines are required.
14. Which metrics will distinguish objective transfer from trajectory imitation.

The output of this stage should be a:

> **specific, experimentally testable research problem.**

---

## 14. Current Status

    Milestone 1
    Isaac Lab + H1
          ↓
       Complete

    Milestone 2
    H1 Locomotion Baseline
          ↓
       Complete

    Milestone 3
    Human Motion Representation
          ↓
       Complete

    Phase 4.1
    Literature Review
          ↓
       Complete
          ↓
    Preliminary Research Gap
          ↓
       Identified
          ↓
    Phase 4.2
    Problem Formulation
          ↓
        NEXT

### Status Summary

**Milestone 1 — Isaac Lab / H1 Setup:** Complete

**Milestone 2 — H1 Locomotion Baseline:** Complete

**Milestone 3 — Human Motion Representation:** Complete

**04_01 Literature:** Complete for the current review scope

**20 relevant papers reviewed:** Yes

**Preliminary Research Gap:** Identified, but not yet confirmed as a novel contribution

**Final Research Question:** Not locked yet

**04_02 Problem Formulation:** Next
