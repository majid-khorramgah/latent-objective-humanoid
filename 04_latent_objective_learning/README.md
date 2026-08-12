# Phase 4 — Latent Human Objective / Cost Learning

## Status

**Current Phase:** Phase 4
**Status:** In Progress
**Research Stage:** Literature → Problem Formulation → Objective Learning → Validation

---

# 1. Purpose

The purpose of Phase 4 is to investigate whether human motion demonstrations can be used to infer the underlying objectives or cost functions that explain human behavior.

The central idea is:

> Do not directly imitate human motion trajectories. Instead, infer the physical or task-related objectives that may have generated those trajectories.

This phase is the core research bridge between:

* Human Motion Understanding
* Inverse Optimal Control / Inverse Reinforcement Learning
* Latent Objective Learning
* Model-Based Robot Control

The output of this phase should be a validated objective or cost representation that can later be used by model-based planning and control.

---

# 2. Core Research Question

## Main Question

**Can underlying human objectives or cost functions be inferred from human motion demonstrations in a form that can later guide physically feasible humanoid control?**

A more specific version of the question will be formulated after reviewing the relevant literature.

The final formulation must be:

* specific
* mathematically defined
* experimentally testable
* falsifiable
* relevant to humanoid locomotion
* compatible with later model-based control

---

# 3. Important Research Principle

This project must NOT assume that the correct human objectives are already known.

For example, the following should initially be treated as hypotheses rather than ground truth:

* stability
* energy efficiency
* robustness
* task success
* smoothness
* effort minimization
* balance

The purpose of this phase is to investigate whether such objectives:

1. explain human demonstrations,
2. can be identified from data,
3. are distinguishable from one another,
4. generalize to unseen demonstrations,
5. and can eventually be used for robot control.

---

# 4. Research Context

The research direction was motivated by feedback from Dr. Dennis Hong at UCLA RoMeLa.

The proposed connection is:

```text
Human Demonstrations
        ↓
Learn Underlying Objectives / Cost Functions
        ↓
Model-Based Planning / MPC
        ↓
Robot Dynamics + Physical Constraints
        ↓
Humanoid Motion
```

The important distinction from conventional imitation learning is:

```text
Trajectory Imitation:

Human trajectory
        ↓
Robot reproduces trajectory


Objective-Based Learning:

Human trajectory
        ↓
Infer underlying objective
        ↓
Robot optimizes objective
        ↓
Robot generates its own feasible motion
```

The robot is therefore not required to reproduce the exact human trajectory.

---

# 5. Relationship to Later Phases

Phase 4 is not the final controller.

The intended research pipeline is:

```text
Human Motion
      ↓
Phase 4
Latent Objective / Cost Learning
      ↓
Phase 5
Model-Based Planning / MPC
      ↓
Phase 6
Humanoid Control
      ↓
Phase 7
Generalization
      ↓
Phase 8
Ablation + Comparison
```

Phase 4 must therefore produce an objective representation that is meaningful for downstream optimization and control.

---

# 6. Phase 4 Sub-Objectives

Phase 4 is divided into the following research tasks.

## 4.1 Literature Review

Investigate prior work in:

### A. Inverse Optimal Control

Study methods that infer a cost function from observed behavior.

Questions:

* What assumptions are made about the expert?
* What is observable?
* What is latent?
* How is the cost parameterized?
* Is the solution unique?
* What ambiguity exists?
* How are demonstrations used?

---

### B. Inverse Reinforcement Learning

Study how reward functions or objectives can be inferred from demonstrations.

Questions:

* How is the reward represented?
* How is reward ambiguity handled?
* How does IRL differ from inverse optimal control?
* Can the learned reward be interpreted physically?
* Can it transfer across agents with different dynamics?

---

### C. Human Motion Objective Learning

Investigate literature on human locomotion and motion generation.

Potential objectives include:

* energetic efficiency
* stability
* smoothness
* effort
* task completion
* balance
* robustness
* contact-related objectives
* biomechanical plausibility

The goal is not to automatically adopt these objectives.

The goal is to determine:

> Which objectives are supported by previous evidence, and which remain open research questions?

---

### D. Optimal Control and MPC

Study how learned objectives can be used by:

* trajectory optimization
* optimal control
* model predictive control
* constrained optimization

This establishes the connection between Phase 4 and Phase 5.

---

### E. RoMeLa Model-Based Control

Study relevant RoMeLa work involving:

* model-based humanoid control
* DCM-based locomotion
* MPC
* whole-body control
* optimization-based control
* QP-based control
* physical constraints
* dynamic locomotion

The purpose is not to copy an existing controller.

The purpose is to understand how a learned human objective could eventually connect to a model-based humanoid control stack.

---

# 7. Human Demonstration Representation

Human demonstrations must be converted into a representation suitable for objective inference.

The representation may include:

### Kinematic information

* joint positions
* joint velocities
* joint accelerations
* root position
* root orientation
* center of mass
* center of mass velocity

### Contact information

* foot contacts
* contact timing
* contact locations
* support phases

### Dynamic / physical information

Where available:

* estimated forces
* estimated torques
* momentum
* angular momentum
* mechanical work
* energy-related quantities

### Task information

Where available:

* desired velocity
* target position
* terrain condition
* obstacle information
* task goal

The final feature set must be justified by literature and experiments.

---

# 8. Objective Representation

The objective should eventually be represented mathematically.

A generic form is:

```text
J(τ; θ)
```

where:

* `τ` = observed motion trajectory
* `θ` = parameters describing the underlying objective

A possible structured representation is:

```text
J(τ; θ) =
    θ₁ f₁(τ)
  + θ₂ f₂(τ)
  + ...
  + θₙ fₙ(τ)
```

where each `fᵢ` represents a measurable physical or task-related feature.

However:

**The final objective structure must NOT be fixed before literature review and experimental analysis.**

The project should determine which representation is scientifically justified.

---

# 9. Latent Objective Learning

The central learning problem is:

```text
Human Demonstrations
        ↓
Observed trajectories
        ↓
Feature / physical representation
        ↓
Objective inference
        ↓
θ / latent objective
```

The learned objective should explain why the observed behavior is plausible under the assumed model.

The research must investigate:

* identifiability
* ambiguity
* parameter sensitivity
* demonstration diversity
* robustness to noise
* generalization
* physical interpretability

---

# 10. Do Not Confuse Latent Representation with Latent Objective

A neural network embedding is not automatically a meaningful objective.

For example:

```text
trajectory
    ↓
encoder
    ↓
128-dimensional vector
```

does not by itself prove that the vector represents a human objective.

A valid objective representation should have a meaningful relationship with:

* observed behavior
* optimization
* physical quantities
* task performance
* downstream robot control

The research must therefore distinguish:

```text
Latent representation
        ≠
Latent objective
```

---

# 11. Objective Identifiability

A major research issue is whether multiple objectives can explain the same demonstration.

For example:

```text
Human trajectory
      ↓
Could be explained by:
      ↓
Energy minimization
Stability optimization
Smoothness
Task success
Combination of objectives
```

Therefore Phase 4 must investigate whether the inferred objective is:

* identifiable
* partially identifiable
* ambiguous
* dependent on assumptions

If the objective is not uniquely identifiable, the project should explicitly model or analyze that ambiguity rather than hiding it.

---

# 12. Demonstration Dataset

The initial dataset should be kept small and controlled.

The first experiments should focus on a simple task such as:

**Human walking / locomotion**

Potential variations:

* walking speed
* stride length
* terrain
* direction
* perturbation
* task condition

The initial objective is not to solve all human motion.

The initial objective is to establish whether the proposed objective-learning methodology works on a controlled locomotion problem.

---

# 13. Experimental Strategy

Phase 4 should proceed incrementally.

## Experiment 1 — Baseline Objective Model

Test whether a simple predefined objective can reproduce or explain demonstrations.

Purpose:

* establish a baseline
* verify the mathematical formulation
* verify data processing

---

## Experiment 2 — Objective Parameter Identification

Estimate objective parameters from demonstrations.

Measure:

* fitting quality
* prediction error
* parameter stability
* sensitivity to demonstration selection

---

## Experiment 3 — Held-Out Demonstrations

Train/infer using one subset of demonstrations and evaluate on unseen demonstrations.

Purpose:

> Determine whether the learned objective captures a reusable principle rather than memorizing individual trajectories.

---

## Experiment 4 — Cross-Condition Evaluation

If data permits:

```text
Train:
normal walking

Test:
different walking speed
different condition
```

The objective should ideally remain meaningful under changed conditions.

---

## Experiment 5 — Synthetic Validation

Before relying entirely on human data, create a controlled synthetic environment where the ground-truth objective is known.

Example:

```text
Known objective
      ↓
Generate demonstrations
      ↓
Hide objective
      ↓
Run objective-learning method
      ↓
Compare learned objective
with ground truth
```

This is important because it tests whether the inference algorithm itself works.

---

# 14. Metrics

Phase 4 should evaluate more than trajectory reconstruction.

Potential metrics:

### Objective recovery

Can the method recover the known objective in synthetic experiments?

### Demonstration explanation

How well does the learned objective explain observed demonstrations?

### Prediction

Can the learned objective predict behavior under new conditions?

### Generalization

Does the learned objective remain useful outside the training demonstrations?

### Interpretability

Can the learned objective be related to meaningful physical quantities?

### Stability of inference

Does the inferred objective change drastically when demonstrations or noise change?

---

# 15. Comparison Baselines

Possible baselines include:

### Baseline A — Direct trajectory imitation

```text
Human trajectory
        ↓
Robot trajectory
```

### Baseline B — Hand-designed objective

```text
Manually designed cost
        ↓
Optimization
```

### Baseline C — Learned objective

```text
Human demonstrations
        ↓
Learned objective
        ↓
Optimization
```

The comparison should determine whether learning the objective provides a meaningful advantage.

---

# 16. Important Constraint

Phase 4 must not become an uncontrolled deep-learning project.

Do not introduce:

* large foundation models
* unnecessary neural architectures
* huge datasets
* complicated latent spaces
* multiple RL algorithms

unless they are justified by the research question.

The goal is:

> **Understand and validate the objective-learning problem first.**

---

# 17. Relationship to Reinforcement Learning

Reinforcement learning is not the primary research question of Phase 4.

RL may be used as a tool where appropriate.

However, the central question is:

```text
What objective explains human behavior?
```

not:

```text
Can PPO reproduce human motion?
```

The learned objective should eventually be usable by model-based optimization/control.

Therefore:

```text
Learning
   ↓
Objective
   ↓
Model-Based Optimization
```

is the primary direction.

RL remains an optional tool rather than the central architecture.

---

# 18. Expected Output of Phase 4

Phase 4 is considered complete only when the project has:

### 1. Literature map

A structured review covering:

* inverse optimal control
* inverse reinforcement learning
* human motion objective learning
* optimal control
* MPC
* relevant RoMeLa model-based control

### 2. Clearly defined research gap

A statement explaining:

> What existing methods already solve and what remains unresolved.

### 3. Specific research question

A question that can be experimentally tested.

### 4. Mathematical formulation

A precise definition of:

* demonstrations
* state
* trajectory
* objective
* cost
* parameters
* assumptions

### 5. Objective-learning method

A reproducible method for inferring the objective.

### 6. Synthetic validation

Evidence that the method can recover a known objective.

### 7. Human-data validation

Evidence that the method can explain or predict human behavior.

### 8. Downstream compatibility

Evidence that the learned objective can be expressed in a form suitable for model-based optimization / MPC.

---

# 19. Exit Criteria

**DO NOT move to Phase 5 simply because the neural network trains successfully.**

Phase 4 is complete only when:

```text
[ ] Relevant literature reviewed
[ ] Research gap identified
[ ] Research question finalized
[ ] Assumptions documented
[ ] Human motion representation defined
[ ] Objective representation defined
[ ] Objective-learning method implemented
[ ] Synthetic validation completed
[ ] Human demonstration experiment completed
[ ] Held-out evaluation completed
[ ] Objective interpretability evaluated
[ ] Limitations documented
[ ] Learned objective expressed in a form usable by optimization/MPC
```

Only after these criteria are satisfied should Phase 5 begin.

---

# 20. Research Decision Gate

Before entering Phase 5, answer:

> **If this learned objective is given to a model-based controller, can the controller optimize it under the robot's own dynamics and physical constraints?**

If the answer is **no**, remain in Phase 4.

If the answer is **yes**, proceed to Phase 5.

---

# 21. Phase 4 Final Pipeline

The target pipeline is:

```text
Human Demonstrations
        ↓
Motion / Physical Representation
        ↓
Candidate Objective Space
        ↓
Inverse Objective / Cost Learning
        ↓
Latent Human Objective
        ↓
Objective Validation
        ↓
Held-Out Demonstrations
        ↓
Generalization / Interpretability Check
        ↓
Optimization-Compatible Cost
        ↓
PHASE 5: Model-Based Planning / MPC
```

---

# 22. Current Position

Current project position:

```text
Phase 1  — Isaac Lab + H1
    ↓
Phase 2  — H1 Locomotion Baseline
    ↓
Phase 3  — Human Motion
    ↓
Phase 4  — Latent Human Objective / Cost Learning  ← CURRENT
    ↓
Phase 5  — Model-Based Planning / MPC
    ↓
Phase 6  — H1 Whole-Body / Low-Level Control
    ↓
Phase 7  — Generalization
    ↓
Phase 8  — Ablation + Comparison
```

**Current task:**

> Do not jump to MPC yet.

The immediate task is to determine, through literature and controlled experiments, what can legitimately be called a latent human objective and how it can be inferred from demonstrations.

---

# 23. Research Log

Every major decision should be recorded here.

Example:

```text
Date:
Decision:
Why:
Evidence:
Paper / experiment:
Effect on project:
```

This section should be updated throughout Phase 4.

---

# 24. Non-Negotiable Research Rules

1. Do not assume the human objective in advance.
2. Do not equate a neural latent vector with an objective.
3. Do not optimize for trajectory similarity alone.
4. Do not move to MPC before the objective is validated.
5. Do not claim generalization without held-out experiments.
6. Record assumptions explicitly.
7. Distinguish hypothesis from experimentally supported conclusions.
8. Prefer simple models before complex neural models.
9. Every major architectural choice must be justified by literature or experiment.
10. The final objective must be usable by downstream model-based control.

---

# 25. Phase 4 Research Goal

The ultimate goal of Phase 4 is to establish:

> **A scientifically justified method for inferring meaningful human objectives or cost functions from demonstrations, in a representation that can later be optimized by a model-based humanoid controller.**

The project should not attempt to reproduce human motion exactly.

The target is:

```text
Understand the objective
        ↓
Represent the objective
        ↓
Validate the objective
        ↓
Give the objective to the robot
        ↓
Let the robot generate its own feasible motion
```

This is the conceptual bridge from:

**Human Motion Understanding**

to:

**Generalizable Humanoid Control.**
