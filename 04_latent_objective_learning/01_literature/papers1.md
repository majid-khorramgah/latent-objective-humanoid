## Paper 10 — Ng & Russell (2000)

**Citation**  
Ng, A. Y., & Russell, S. J. (2000). *Algorithms for Inverse Reinforcement Learning*. Proceedings of the 17th International Conference on Machine Learning (ICML).

**Literature Category**  
Inverse Reinforcement Learning (IRL) / Reward Inference / Objective Learning

---

### 1. Research Problem

The paper studies **Inverse Reinforcement Learning (IRL)**.

In ordinary Reinforcement Learning (RL), the reward function is known and the agent learns how to behave.

The direction is:

    Reward / Objective
            ↓
        RL Algorithm
            ↓
          Behavior

In Inverse Reinforcement Learning, the direction is reversed.

We observe an agent's behavior and try to infer a reward function that could have produced that behavior:

    Observed Behavior
            ↓
          IRL
            ↓
    Reward / Objective

The central problem is therefore:

> Given observed behavior, can we recover the underlying reward function that explains that behavior?

This is directly relevant to our project because we also want to infer an underlying objective from human demonstrations rather than directly copying human trajectories.

---

### 2. Input

The input to the IRL problem consists of:

- an environment/model,
- observed behavior or demonstrations,
- and information about the dynamics or transition structure.

The demonstrations represent behavior that is assumed to be approximately optimal with respect to some unknown reward function.

Conceptually:

    Environment / Dynamics
            +
    Demonstration
            ↓
           IRL
            ↓
      Reward Function

For our project, the analogous input would be:

    Human locomotion demonstrations
            +
    Human motion / dynamics information
            ↓
           IRL / IOC
            ↓
    Candidate Human Objective

---

### 3. Method

Ng & Russell formulate IRL as the problem of finding a reward function for which the observed behavior is optimal, or approximately optimal.

The important idea is that we do not directly learn the trajectory.

Instead, we search for a reward function that explains why the demonstrated behavior would be preferred.

Suppose a robot can reach a target using several possible trajectories.

If the human consistently chooses one particular trajectory, IRL asks:

> What reward function would make this trajectory optimal?

For example, imagine two possible paths:

    Path A: short but high effort

    Path B: longer but low effort

If the human consistently chooses Path B, IRL might infer that minimizing effort is important.

However, this does not prove that effort is the true human objective.

Another reward function could potentially explain the same behavior.

This leads to one of the most important concepts in this paper:

**Reward ambiguity.**

---

### 4. Objective / Cost

The paper represents the reward using features of the state and/or behavior.

Conceptually:

    Reward = combination of features

For example:

    Reward =
        w1 * Feature1
        +
        w2 * Feature2
        +
        ...

The features might describe properties such as:

- distance to a goal,
- state properties,
- actions,
- or other characteristics of the behavior.

The IRL algorithm attempts to find reward functions under which the demonstrated behavior is better than alternative behaviors.

An important point is that the method does not guarantee recovery of the unique "true" reward function.

---

### 5. Simple Example

Imagine a person walking from point A to point B.

We observe:

    Human
      ↓
    chooses a short path
      ↓
    reaches B

We might infer:

    Objective = minimize distance

But another explanation could be:

    Objective = minimize time

or:

    Objective = minimize distance + minimize effort

or:

    Objective = avoid uncomfortable regions

All of these could potentially produce similar behavior.

Therefore:

    One observed behavior
            ↓
    Multiple possible objectives

This is the fundamental ambiguity of IRL.

---

### 6. Important Concept: Reward Ambiguity

One of the most important lessons from Ng & Russell is that the mapping

    Behavior → Reward

is generally not unique.

This is extremely important for our research.

Suppose we observe:

    Human walking demonstration

and infer:

    J = energy + smoothness

We cannot immediately claim:

> "We discovered the true human objective."

A safer statement is:

> "We found an objective that explains the observed behavior."

This distinction should remain explicit throughout our project.

---

### 7. Validation

The paper develops algorithms for solving the IRL problem and evaluates whether the inferred reward functions can explain or reproduce the demonstrated behavior.

The important validation concept is not simply:

    Does the learned reward look mathematically reasonable?

Instead:

    Does optimizing the learned reward produce behavior
    consistent with the demonstration?

This idea is highly relevant to our future validation stages.

For our project, we should eventually ask:

    Learned Human Objective
            ↓
       Optimization
            ↓
       Generated Motion

and compare the resulting behavior with held-out human demonstrations.

---

### 8. Main Finding

The main contribution is the formalization and algorithmic treatment of the Inverse Reinforcement Learning problem.

The paper establishes that:

> It is possible to infer reward functions from observed behavior, but the inferred reward is generally not uniquely determined by the behavior.

This is a fundamental result for objective learning.

The paper therefore provides both:

1. a foundation for learning objectives from demonstrations, and
2. an important warning about objective identifiability.

---

### 9. Limitations

#### 9.1 Reward ambiguity

The biggest limitation is that multiple reward functions can explain the same behavior.

Therefore:

    Demonstration
        ↓
    Unique true reward

cannot generally be assumed.

This is directly relevant to our project.

---

#### 9.2 Dependence on representation

The reward is generally expressed using a feature representation.

Therefore, the quality of the inferred reward depends partly on the features available to the algorithm.

This creates an important distinction:

    Learning reward parameters
            ≠
    Discovering an unrestricted objective representation

This distinction is important for our "latent objective" idea.

---

#### 9.3 Assumption about approximately optimal behavior

IRL generally relies on the assumption that the observed demonstrations are informative about an approximately optimal policy or behavior.

Human behavior does not necessarily satisfy this assumption perfectly.

Humans may:

- make mistakes,
- behave inconsistently,
- explore,
- react to uncertainty,
- or optimize multiple objectives.

Therefore, applying classical IRL directly to human locomotion requires care.

---

#### 9.4 Environment and dynamics knowledge

The classical formulation assumes that the environment or transition dynamics are sufficiently known.

This is easier in a controlled simulation than in real human locomotion.

For our project, this distinction matters because:

    Human dynamics
          ≠
    H1 dynamics

The human demonstration is used to infer an objective, while the final motion must be generated using H1's own dynamics.

---

#### 9.5 No humanoid transfer

The paper does not investigate:

    Human
      ↓
    learned objective
      ↓
    different humanoid morphology
      ↓
    robot behavior

Therefore, it does not solve the human-to-H1 transfer problem.

---

#### 9.6 No MPC integration

The paper is about reward inference rather than using a learned human reward as the central objective of a whole-body humanoid MPC.

Therefore it does not establish:

    Learned Human Objective
            +
       H1 Dynamics
            +
       H1 Constraints
            ↓
           MPC

---

### 10. Relevance to Our Project

**Relevance: High**

This paper is important because it provides the conceptual foundation for the IRL side of our literature review.

Our project asks:

    Human Demonstrations
            ↓
    Underlying Objective
            ↓
    H1 Motion

IRL provides a formal framework for the first step:

    Human Demonstrations
            ↓
           IRL
            ↓
       Objective / Reward

However, we should not assume that classical IRL automatically solves our problem.

Our problem adds several additional requirements:

- human locomotion,
- generalizable objective,
- different robot morphology,
- different robot dynamics,
- physical constraints,
- and model-based MPC.

---

### 11. Research Gap Contribution

This paper establishes that:

> Reward/objective inference from demonstrations is a valid and formal research problem.

Therefore, the following is NOT a sufficient novelty claim:

> "We learn a reward from demonstrations."

That has been established by the IRL literature for decades.

More importantly, the paper introduces a fundamental issue:

> The inferred reward may not be uniquely identifiable from observed behavior.

This creates an important question for our project:

> If multiple objectives can explain the same human locomotion, what properties should an objective have in order to be useful when transferred to a humanoid robot with different dynamics and constraints?

This question is highly relevant to our research direction.

However:

> Whether this can constitute a novel research contribution is NOT ESTABLISHED YET.

The remaining IRL, locomotion, and model-based control literature must be reviewed first.

---

### 12. Difference Between This Paper and Our Project

The conceptual difference can be summarized as:

Ng & Russell:

    Demonstration
         ↓
        IRL
         ↓
    Reward function

Our target:

    Human Locomotion Demonstrations
                 ↓
        Human Objective Inference
                 ↓
       Generalizable Objective
                 ↓
          H1 Dynamics
                 +
          H1 Constraints
                 ↓
                MPC
                 ↓
          H1 Locomotion

Therefore, our project is not simply:

> "Apply IRL to human motion."

The difficult part is potentially the transfer and use of the inferred objective under a different robot's physical dynamics and constraints.

---

### 13. Important Lesson for Phase 4

This paper gives us an important rule:

**Do not equate behavioral explanation with recovery of the true objective.**

If an objective reproduces the demonstrations, that does not automatically mean it is the true human objective.

Therefore, later experiments should evaluate more than training reconstruction.

We will eventually need:

- held-out demonstrations,
- different locomotion conditions,
- objective perturbation tests,
- and potentially transfer tests on different dynamics.

This connects directly to our planned:

    04_08 Held-out Evaluation

and:

    04_09 Analysis

stages.

---

### 14. Position in Our Literature Review

| Question | Ng & Russell (2000) |
|---|---|
| Demonstrations used? | Yes |
| Objective/reward inferred? | Yes |
| IRL used? | Yes |
| IOC used? | No |
| Human motion? | No |
| Human locomotion? | No |
| Composite human objective? | Not specifically |
| Latent objective representation? | No |
| Reward ambiguity addressed? | Yes |
| Generalization across humans? | No |
| Robot morphology transfer? | No |
| Different dynamics transfer? | No |
| Humanoid control? | No |
| MPC integration? | No |
| H1-specific constraints? | No |

---

### 15. Role in Our Project

**Overall role:**

**Foundational IRL paper + fundamental reward ambiguity/identifiability warning**

The paper tells us:

    Demonstration
        ↓
       IRL
        ↓
    Objective

is possible.

But it also tells us:

    Demonstration
        ↓
    Multiple possible objectives

may also occur.

Therefore, our project should not simply ask:

> "Can we find a reward that reproduces human motion?"

Instead, we should eventually ask:

> "Can we infer an objective from human locomotion that remains useful and meaningful when optimized under the dynamics and physical constraints of a different humanoid robot?"

This distinction is central to the research direction.

---

### 16. Status for Our Literature Review

**Status: Required**

**Reason:**

This paper is foundational for understanding IRL and the objective-identifiability problem.

It is not a direct solution to our project.

It establishes an important constraint on how we should formulate and interpret our future objective-learning experiments.
