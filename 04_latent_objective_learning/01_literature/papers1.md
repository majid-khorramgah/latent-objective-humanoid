## Paper 11 — Ng & Russell (2000)

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





## Paper 12 — Ziebart et al. (2008)

**Citation**  
Ziebart, B. D., Maas, A. L., Bagnell, J. A., & Dey, A. K. (2008). *Maximum Entropy Inverse Reinforcement Learning*. Proceedings of the AAAI Conference on Artificial Intelligence.

**Literature Category**  
Inverse Reinforcement Learning (IRL) / Maximum Entropy IRL / Human Behavior Modeling

---

### 1. Research Problem

Classical Inverse Reinforcement Learning (IRL) attempts to infer a reward function from observed demonstrations.

The basic idea is:

    Observed Behavior
            ↓
           IRL
            ↓
      Reward Function

However, human behavior is not always perfectly optimal or deterministic.

If a person has several reasonable ways to perform a task, they may choose different behaviors on different occasions.

For example:

    Person wants to reach a target

    Possible trajectories:
    
    A → very fast
    B → smooth and comfortable
    C → energy efficient

A human may choose B most of the time, but sometimes choose A or C.

Therefore, the paper asks:

> How can we infer a reward function when demonstrations are not assumed to be generated by one single deterministic optimal trajectory?

---

### 2. Input

The input consists of demonstrations of behavior.

Conceptually:

    Demonstrations
          ↓
    Trajectories
          ↓
    Maximum Entropy IRL
          ↓
    Reward Function

The demonstrations may contain different trajectories that are all reasonably consistent with the underlying objective.

This is particularly relevant to human demonstrations because different people, and even the same person at different times, may perform a task differently.

---

### 3. Method

The paper introduces a **Maximum Entropy formulation of Inverse Reinforcement Learning**.

The key idea is:

> Do not assume that the demonstrated trajectory is the only possible optimal behavior.

Instead, assign probabilities to possible trajectories.

Conceptually:

    Higher reward
         ↓
    Higher probability

and:

    Lower reward
         ↓
    Lower probability

Therefore, the model does not simply ask:

    "Which trajectory is optimal?"

It asks:

    "Which trajectories are more likely under the inferred reward?"

This makes the model better suited to situations where behavior contains variability.

---

### 4. Simple Example

Suppose a human wants to walk from point A to point B.

There are three possible walking behaviors:

    Path A → fast but energetically expensive

    Path B → moderate speed and moderate effort

    Path C → slow but very energy efficient

Suppose we observe:

    Path A → 10% of demonstrations
    Path B → 80% of demonstrations
    Path C → 10% of demonstrations

A deterministic interpretation might say:

    Path B = optimal
    Path A/C = wrong

Maximum Entropy IRL instead allows:

    Path B → high probability
    Path A → lower probability
    Path C → lower probability

The inferred reward explains why B is preferred without assuming that humans must always select B.

---

### 5. Objective / Reward

The reward is represented using features of the behavior.

Conceptually:

    Reward =
        w1 * Feature1
        +
        w2 * Feature2
        +
        ...

The learning process estimates a reward function whose induced trajectory distribution is consistent with the demonstrations.

The important difference from a purely deterministic formulation is that the reward defines a **distribution over possible behaviors**, rather than selecting only one behavior.

Conceptually:

    Objective
        ↓
    Probability distribution
        ↓
    Different possible trajectories

This is important for modeling human behavior.

---

### 6. Why "Maximum Entropy"?

The word "entropy" is important because many different trajectory distributions could potentially explain the demonstrations.

The Maximum Entropy principle chooses the least-committed distribution consistent with the available evidence.

In simple terms:

> Do not assume additional information about human behavior that is not supported by the demonstrations.

Therefore, if the demonstrations show that several trajectories are possible, the method does not artificially force all probability onto one trajectory.

This is useful because human behavior naturally contains variability.

---

### 7. Main Finding

The paper demonstrates that a maximum-entropy formulation provides a principled way to perform IRL when demonstrations can contain multiple possible behaviors.

The important conceptual result is:

    One objective
          ↓
    Multiple possible behaviors

rather than:

    One objective
          ↓
    One deterministic trajectory

This is a better conceptual model for many real-world behavior learning problems.

---

### 8. Relation to Human Behavior

Humans do not necessarily execute the exact same trajectory every time.

For example:

    Human 1 → slightly different gait

    Human 2 → different foot placement

    Human 3 → different joint motion

Even if all three humans are trying to accomplish the same task.

Therefore:

    Similar objective
          ↓
    Different trajectories

is possible.

Maximum Entropy IRL provides a framework that can represent this variability.

This is one of the main reasons the paper is relevant to our project.

---

### 9. Difference from Ng & Russell (2000)

Ng & Russell establish the fundamental IRL problem:

    Demonstration
         ↓
        IRL
         ↓
       Reward

The key difficulty is that multiple reward functions can explain the same behavior.

Ziebart et al. extend this idea by modeling behavior probabilistically.

Conceptually:

    Ng & Russell:

    Reward
       ↓
    Optimal behavior


    Ziebart:

    Reward
       ↓
    Probability distribution
       ↓
    Multiple possible behaviors

Therefore, Ziebart is particularly relevant when demonstrations contain behavioral variability.

---

### 10. Important Limitation

Maximum Entropy IRL does **not** solve the fundamental problem of uniquely recovering the "true" human objective.

Different reward functions may still explain the observed behavior.

Therefore:

    Learned reward
          ≠
    Guaranteed true human objective

The method gives us a principled probabilistic explanation of behavior, but it does not prove that the inferred reward is the exact cognitive objective used by the human.

This distinction is critical for our project.

---

### 11. Representation Limitation

The reward is still constructed using a feature representation.

Conceptually:

    Reward = weighted combination of features

Therefore, the method does not automatically discover an unrestricted latent representation of human objectives from raw demonstrations.

This distinction is important:

    Learning reward parameters
            ≠
    Discovering the complete objective representation

Our project should keep this distinction explicit.

---

### 12. Human Locomotion Limitation

The paper is not specifically about human locomotion.

It does not determine whether human walking is driven by:

- energy minimization,
- stability,
- smoothness,
- speed,
- comfort,
- robustness,
- task success,
- or a combination of these.

Therefore, we cannot use this paper as evidence for a particular human locomotion objective.

Those remain hypotheses that must be supported by the human locomotion literature.

---

### 13. No Humanoid Transfer

The paper does not investigate transferring an inferred human reward to a robot with different morphology and dynamics.

It does not solve:

    Human
      ↓
    Learned objective
      ↓
    Different humanoid
      ↓
    New motion

Therefore, the human-to-H1 transfer problem remains open.

---

### 14. No MPC Integration

The paper focuses on reward inference.

It does not demonstrate the complete pipeline:

    Human Demonstrations
            ↓
    Learned Objective
            ↓
       H1 Dynamics
            +
       H1 Constraints
            ↓
           MPC
            ↓
       H1 Behavior

Therefore, it does not directly solve the model-based control part of our project.

---

### 15. Relevance to Our Project

**Relevance: High**

The paper provides an important conceptual foundation for learning objectives from human demonstrations when human behavior is variable.

Our project should not assume:

    One human objective
            ↓
    One exact trajectory

Instead, it is reasonable to consider:

    Underlying objective
            ↓
    Distribution of reasonable behaviors
            ↓
    Different human trajectories

This is especially relevant because our goal is not trajectory imitation.

We want to infer an objective that can later be optimized by the H1 under its own dynamics and constraints.

---

### 16. Research Gap Contribution

This paper establishes that:

> Human-like behavioral variability can be incorporated into IRL by modeling a probability distribution over trajectories rather than assuming one deterministic optimal trajectory.

Therefore, the following is **not a sufficient novelty claim** for our project:

> "We use probabilistic IRL to learn a reward from human demonstrations."

That idea is already established.

The potentially important question for our project is different:

> Can an objective inferred from variable human demonstrations remain useful when it is optimized by a robot with different morphology, dynamics, and physical constraints?

This question is **NOT ESTABLISHED YET**.

It must be evaluated against the remaining locomotion, MPC, and humanoid literature.

---

### 17. Direct Implication for Our Project

This paper gives us an important design principle:

**Do not require all human demonstrations to have the same trajectory.**

For example:

    Human Demonstrations

    Demo 1 → gait A
    Demo 2 → gait B
    Demo 3 → gait A'
    Demo 4 → gait C
    Demo 5 → gait B'

These trajectories may still be consistent with a common underlying objective.

Therefore, our future objective-learning method should ideally distinguish:

    What is common across demonstrations
                    from
    What is individual trajectory variation

This is potentially important for learning a **generalizable objective**.

However, how exactly to represent and learn this common objective is **Unknown** at the current stage.

---

### 18. Position in Our Literature Review

| Question | Ziebart et al. (2008) |
|---|---|
| Demonstrations used? | Yes |
| Reward/objective inferred? | Yes |
| IRL used? | Yes |
| Probabilistic behavior model? | Yes |
| Maximum Entropy formulation? | Yes |
| Behavioral variability addressed? | Yes |
| Human motion? | Not specifically |
| Human locomotion? | No |
| Latent objective representation learned from scratch? | No |
| Unique true human objective recovered? | No |
| Robot morphology transfer? | No |
| Different dynamics transfer? | No |
| Humanoid control? | No |
| MPC integration? | No |
| H1-specific constraints? | No |
| Generalizable human objective? | Not established |

---

### 19. Role in Our Project

**Overall Role:**

**Foundational probabilistic IRL paper for modeling variability in human demonstrations**

The main lesson for our project is:

    Human Demonstrations
            ↓
    Variable behaviors
            ↓
    Probabilistic objective inference

rather than:

    Human Demonstrations
            ↓
    One exact trajectory
            ↓
    Imitation

This supports the broader motivation of our project:

> We should try to learn what is common in human behavior at the objective level rather than requiring the robot to reproduce every detail of human trajectories.

---

### 20. Final Takeaway

The most important idea to retain from this paper is:

> Humans may pursue similar objectives while producing different trajectories.

Therefore:

    Similar Objective
            ↓
    Different Valid Behaviors

Maximum Entropy IRL provides a mathematical framework for representing this idea.

For our project, this is useful because the desired learned objective should ideally capture the **common structure behind human demonstrations**, rather than memorizing one particular human trajectory.

**Status: Required**

**Reason:**  
This paper is essential for understanding probabilistic IRL and behavioral variability. It does not provide the final solution to our problem, but it establishes an important foundation for reasoning about human demonstrations.
