# Phase 4.1 — Literature Review

## Purpose

The purpose of this stage is to understand what has already been done in the area of learning human objectives or cost functions from motion demonstrations, and to identify a clear research gap for this project.

The main research direction is:

Human Motion Demonstrations
→ Objective / Cost Inference
→ Model-Based Optimization
→ Humanoid Control

This stage is focused on understanding the literature before implementing the objective-learning method.

---

## Main Research Question

Can the underlying objectives or cost functions that generate human motion be inferred from human demonstrations in a form that can later be used by model-based humanoid control?

---

## Literature Areas

The review focuses on five main areas:

1. Inverse Optimal Control (IOC)
2. Inverse Reinforcement Learning (IRL)
3. Human Motion and Locomotion Objectives
4. Optimal Control and Model Predictive Control (MPC)
5. RoMeLa / Dennis Hong model-based humanoid control

---

## What We Need to Understand

For each area, investigate:

- What problem is being solved?
- What information is observed?
- What is learned?
- How is the objective or cost represented?
- What assumptions are required?
- How is the method validated?
- Does it generalize to unseen demonstrations or conditions?
- Can the learned objective be used for robot control?
- What are the main limitations?

---

## Important Research Principle

The project must not assume that the true human objectives are already known.

Possible objectives such as:

- stability
- energy efficiency
- smoothness
- robustness
- effort
- task completion

should initially be treated as candidate hypotheses rather than established ground truth.

The literature review should determine how previous research has addressed these objectives and what remains unresolved.

---

## Key Distinction

This project is not primarily about reproducing human trajectories.

Trajectory imitation:

Human trajectory
→ Robot reproduces trajectory

Objective learning:

Human trajectory
→ Infer underlying objective
→ Robot optimizes objective
→ Robot generates its own feasible motion

The distinction between trajectory imitation and objective learning must remain central throughout the project.

---

## Literature Comparison

Each important paper should be recorded in `papers.md`.

The following information should be collected:

- Paper
- Year
- Problem
- Input / Demonstrations
- Method
- Objective / Cost Representation
- Human Motion
- Robot Control
- Main Result
- Main Limitation
- Relevance to This Project

---

## Literature Matrix

The file `literature_matrix.md` should provide a concise comparison between the most relevant papers.

The main questions are:

- Does the work use human demonstrations?
- Does it infer an objective or cost?
- Does it use IOC or IRL?
- Is the objective physically interpretable?
- Is the objective transferable?
- Is model-based control used?
- Is MPC used?
- Is humanoid control involved?
- What limitation remains?

---

## Research Gap

The most important output of this stage is a clearly defined research gap.

The goal is to identify:

Previous Work
→ What has already been solved
→ What remains unresolved
→ Proposed Research Direction

The research gap must be supported by the reviewed literature.

It should not be based only on intuition.

---

## Relation to RoMeLa

The literature review should specifically examine relevant work from Dennis Hong and RoMeLa on:

- humanoid locomotion
- model-based control
- DCM
- MPC
- trajectory optimization
- whole-body control
- optimization-based control
- physical constraints

The purpose is to understand how a learned human objective could eventually connect to a model-based humanoid control framework.

The goal is not to reproduce an existing RoMeLa controller.

---

## Completion Criteria

Phase 4.1 is complete when:

- The main relevant literature areas have been reviewed.
- Important papers have been recorded in `papers.md`.
- The main approaches have been compared in `literature_matrix.md`.
- The strengths and limitations of existing methods are understood.
- Relevant RoMeLa work has been reviewed.
- A preliminary research gap has been identified.
- The findings provide enough evidence to formulate the specific problem in Phase 4.2.

---

## Current Status

Status: In Progress

Current task:

Literature review and research-gap identification.

Next step:

Phase 4.2 — Problem Formulation
