# Preliminary Research Gap

## Learning Latent Human Objectives for Generalizable Humanoid Intelligence

### Executive Summary

We reviewed prior work across IOC, IRL, human locomotion objectives, model-based MPC, and humanoid control.

The literature shows that **objective inference from human demonstrations** and **dynamics-aware humanoid MPC** have largely been studied separately.

Our preliminary research direction is to connect them: **infer an underlying human locomotion objective from demonstrations, then optimize that objective under the Unitree H1's own dynamics and physical constraints using MPC, rather than directly imitating human trajectories.**

The next step is to formulate this idea as a **specific, experimentally testable problem** in `04_02_problem_formulation`.

---

## 1. What We Found

Previous work provides the main components separately:

    Human Demonstrations
            ↓
        IOC / IRL
            ↓
      Human Objective


    Objective
        +
    Robot Dynamics
        +
    Physical Constraints
        ↓
       MPC
        ↓
    Humanoid Motion

However, the key question for our project is:

> Can an objective inferred from human locomotion remain useful when optimized by a humanoid robot with different morphology, dynamics, and constraints?

This is a **preliminary research gap**, not yet a confirmed novelty claim.

---

## 2. Important Lessons from the Literature

- IOC/IRL can infer objectives or rewards from demonstrations.
- Human locomotion may involve multiple competing movement criteria.
- We should not assume the human objective in advance (e.g., energy + stability + smoothness).
- Whole-body MPC can generate motion while respecting robot dynamics and constraints.
- Direct human-to-humanoid trajectory imitation is not the target of this project.

Therefore, the central distinction is:

    Trajectory Transfer
            ✗

    Objective Transfer
            ✓

---

## 3. Proposed Research Direction

    Human Demonstrations
            ↓
    Infer Human Objective
            ↓
    Unitree H1
    + Dynamics
    + Constraints
            ↓
           MPC
            ↓
       H1 Behavior
            ↓
      Unseen Conditions

The H1 should generate its **own motion** rather than reproduce the human trajectory.

---

## 4. Current Data Foundation

AMASS provides a suitable source of human demonstrations.

An existing preprocessing pipeline provides:

    AMASS
      ↓
    SMPL-X
      ↓
    3D Joints
      ↓
    Position / Velocity / Acceleration

This can be used as the starting point for `04_03 Human Data`.

Large neural latent representations (VAE/Transformer) are **not assumed necessary yet**.

---

## 5. Current Status

**04_01 Literature:** Complete for the current review scope

**Preliminary Research Gap:** Identified, not yet fully established

**Final Research Question:** Not locked yet

**Next Step:** `04_02 Problem Formulation`

The next stage will define the demonstration, objective, objective representation, inference method, H1 transfer mechanism, MPC formulation, and generalization evaluation.
