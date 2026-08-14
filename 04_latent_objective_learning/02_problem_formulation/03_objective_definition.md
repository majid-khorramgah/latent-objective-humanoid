# Objective Definition

## 1. Purpose

The purpose of this stage is to define what we mean by a
"human objective" in the context of this project.

The objective should describe the properties of human motion that
are inferred from demonstrations and can later be optimized under
the dynamics and physical constraints of the Unitree H1.

The objective representation is NOT fixed yet.

It will be treated as a research variable that must be evaluated
experimentally.

---

## 2. Core Principle

We do not want to directly reproduce the human trajectory.

Instead:

    Human Demonstration
            ↓
    Infer Human Objective
            ↓
    H1 Dynamics + Constraints
            ↓
           MPC
            ↓
       H1-generated Motion

Therefore, the objective should capture properties of the behavior
that can remain meaningful when the morphology and dynamics change.

---

## 3. What Is a Human Objective?

For this project, a human objective is defined as:

> A function that assigns a cost to a candidate movement according
> to how well that movement satisfies the behavioral preferences
> expressed by the human demonstration.

Conceptually:

    Motion + Context
          ↓
    Objective / Cost
          ↓
       Scalar Cost

A lower cost corresponds to a movement that better satisfies the
inferred objective.

The objective is therefore different from the trajectory itself.

Trajectory:

    "Move the left foot to this exact position at this exact time."

Objective:

    "Achieve the intended walking behavior while satisfying the
     relevant movement preferences."

This distinction is essential for transfer to a different robot.

---

## 4. Candidate Objective Representation

Based on the literature, human locomotion may involve multiple
movement criteria rather than a single universal criterion.

Candidate objective features may include:

### Task / Goal

- Desired walking speed
- Target achievement
- Foot placement
- Task completion

### Stability / Balance

- Center-of-mass behavior
- Postural stability
- Balance-related quantities

### Efficiency

- Mechanical effort
- Energy-related quantities
- Cost of transport

### Motion Quality

- Smoothness
- Joint acceleration
- Kinematic regularity

### Contact / Physical Behavior

- Foot-ground interaction
- Impact-related quantities
- Contact consistency

These are candidate hypotheses, not established components of the
final human objective.

---

## 5. Initial Mathematical Representation

A simple initial representation is:

    J_human(τ, c)
        = Σ_i w_i φ_i(τ, c)

where:

- τ = human motion trajectory
- c = task or context
- φ_i = candidate objective feature
- w_i = importance of the corresponding feature

For example:

    J =
        w_task       φ_task
      + w_balance    φ_balance
      + w_effort     φ_effort
      + w_smoothness φ_smoothness
      + ...

The weights determine how strongly each criterion contributes to
the overall objective.

---

## 6. Important Research Constraint

We must NOT assume that:

    J = Energy + Stability + Smoothness + Robustness

is the true human objective.

These components are only hypotheses.

The literature provides evidence that multiple criteria can explain
human movement, but it does not establish one universal objective
for all human locomotion.

For example, previous work has shown that combined cost functions
can improve prediction of healthy gait, while recent work has shown
that humans may prioritize different movement goals during walking.

Therefore:

    Candidate Features
            ↓
       Learn / Infer
            ↓
    Evaluate Experimentally
            ↓
    Keep / Remove / Modify

---

## 7. Context Dependence

Human movement objectives may depend on the task and context.

For example, consider walking on two surfaces.

### Normal walking

A person may prioritize:

    Comfortable walking
    +
    Efficient movement
    +
    Desired speed

### Slippery surface

The person may place greater importance on:

    Balance
    +
    Safe foot placement

Therefore, the objective may depend on context:

    J_human(τ | c)

rather than being a single fixed function:

    J_human(τ)

This possibility will be investigated experimentally rather than
assumed as a fact.

---

## 8. Individual Differences

Different humans may perform the same task differently.

For example:

    Person A
        → prioritizes efficiency

    Person B
        → prioritizes stability

while both successfully complete the same walking task.

Therefore, the formulation should allow the possibility that:

    J_human^person_A ≠ J_human^person_B

However, the initial experiments should remain small and controlled.

We should first determine whether a shared objective representation
can explain the demonstrations before introducing a personalized
objective model.

---

## 9. Objective Representation vs. Objective Parameters

An important distinction is made between:

### Objective Representation

The structure of the objective:

    J = Σ_i w_i φ_i

and:

### Objective Parameters

The learned values:

    w_1, w_2, ..., w_n

Learning only the weights of predefined features is parameter
estimation.

It does not necessarily mean that the underlying objective
representation itself has been discovered.

This distinction will be preserved throughout the project.

---

## 10. Why Start With a Structured Representation?

A structured representation provides several advantages:

- Interpretability
- Easier comparison with existing literature
- Easier ablation studies
- Easier synthetic validation
- Easier integration with MPC
- Lower computational complexity
- Easier identification of failure cases

It also prevents the project from immediately becoming a large
black-box representation-learning problem.

A more expressive latent representation can be investigated later
only if the structured formulation is insufficient.

---

## 11. Relationship to Previous Literature

Previous research provides evidence supporting several aspects of
this formulation.

Berret et al. demonstrated that human movement can be better
explained using a composite cost rather than a single criterion.

Maroger et al. applied inverse optimal control to human locomotion
and inferred a cost function that reproduced characteristics of
human locomotion.

Veerkamp et al. showed that different optimization criteria explain
different aspects of healthy gait and that a weighted combined cost
can improve gait prediction.

Recent work by Feldman et al. further indicates that people can
prioritize multiple movement goals during walking and that these
priorities can differ across individuals and task conditions.

These findings motivate a multi-criteria objective representation,
but they do not establish the final objective for our project.

---

## 12. Initial Objective Hypothesis

The initial hypothesis is therefore:

> Human locomotion can be represented by a structured objective
> composed of multiple candidate movement criteria whose relative
> importance can be inferred from demonstrations.

Formally:

    Human Demonstrations
            ↓
    Candidate Objective Features
            ↓
    Infer Objective Parameters
            ↓
       J_human

This hypothesis must be tested.

---

## 13. Transfer Requirement

The objective representation must ultimately be compatible with
optimization on the Unitree H1.

Therefore, we distinguish between:

### Human-specific quantities

Quantities that depend directly on human morphology and dynamics.

and:

### Transferable behavioral quantities

Quantities that can be expressed using the state, task, and physical
properties of the robot.

The final objective should preferably allow:

    Human Objective
          ↓
    Robot-compatible formulation
          ↓
    H1 optimization

without directly copying human joint trajectories.

---

## 14. Objective Transfer

The intended transfer is:

    Human
    -----

    Demonstration
         ↓
    Infer Objective
         ↓
    Human Objective


    Robot
    ------

    Human Objective
         ↓
    Express using H1 state / dynamics
         ↓
    Add H1 constraints
         ↓
    MPC
         ↓
    H1 Motion

The H1 is therefore allowed to generate a trajectory that is
different from the human trajectory.

The important requirement is that it satisfies the relevant
behavioral objective.

---

## 15. What We Do Not Assume

At this stage we do NOT assume:

- A universal human objective
- Energy is always the dominant criterion
- Stability is always the dominant criterion
- Smoothness is always necessary
- Robustness is necessarily an explicit human objective
- A VAE is required
- A Transformer is required
- A deep latent representation is required
- The objective must be linear
- The same objective applies to every task
- The same objective applies to every person

These remain research questions.

---

## 16. Initial Research Decision

For the first experimental formulation, we will use a small,
interpretable candidate objective representation.

The initial form is:

    J_human(τ, c) = Σ_i w_i φ_i(τ, c)

The objective components and their weights will be determined through
the subsequent problem formulation and validation experiments.

If experiments demonstrate that this representation cannot explain
the demonstrations or does not transfer to H1, a more expressive
representation may then be investigated.

This keeps the project small, rigorous, and experimentally testable.

---

## 17. Next Step

The next step is to define the exact candidate features:

    φ_1, φ_2, ..., φ_n

and determine:

1. Which features can be computed reliably from AMASS.
2. Which features are meaningful for locomotion.
3. Which features can be transferred to H1.
4. Which parameters can be inferred from demonstrations.
5. Which objective representations can be validated synthetically.

This will be specified in the subsequent problem formulation and
experimental design.

---

## Status

Objective definition:

**Preliminary formulation**

Final objective representation:

**Not established yet**

Candidate objective components:

**Hypotheses**

Next step:

**Define the exact mathematical problem and inference procedure.**
