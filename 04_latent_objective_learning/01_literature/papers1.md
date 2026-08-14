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




## Paper 13 — Wulfmeier et al. (2015/2016)

**Citation**  
Wulfmeier, M., Ondruska, P., & Posner, I. (2015). *Deep Inverse Reinforcement Learning*. arXiv:1507.04888.

Published/extended version: *Maximum Entropy Deep Inverse Reinforcement Learning* (2016).

**Literature Category**  
Inverse Reinforcement Learning (IRL) / Maximum Entropy IRL / Deep Reward Learning / Nonlinear Cost Function Learning

---

### 1. Research Problem

Traditional Inverse Reinforcement Learning (IRL) attempts to infer the reward function that explains observed behavior.

A common formulation represents the reward as a weighted combination of manually designed features:

    Reward =
        w1 * Feature1
        +
        w2 * Feature2
        +
        ...

This creates an important limitation.

The researcher must decide beforehand which features are relevant.

For simple problems this may be sufficient, but realistic environments can contain large state spaces and complicated interactions between features.

The paper therefore asks:

> Can neural networks be used to learn complex and nonlinear reward functions from demonstrations?

The main idea is to combine:

    Maximum Entropy IRL
            +
    Deep Neural Networks
            ↓
    Nonlinear Reward Function

---

### 2. Input

The input consists of demonstrations of an agent's behavior together with a model of the environment.

Conceptually:

    Demonstrations
          +
    Environment Model
          ↓
    Deep IRL
          ↓
    Learned Reward Function

The paper is primarily demonstrated in navigation/path-planning style environments rather than human locomotion.

Therefore:

- Demonstrations: Yes
- IRL: Yes
- Human locomotion: No
- Humanoid robot: No
- H1: No

---

### 3. Method

The paper uses a neural network to approximate the reward function inside a Maximum Entropy IRL framework.

Instead of assuming:

    Reward = weighted sum of predefined features

the model learns a nonlinear mapping:

    State / Features
          ↓
    Neural Network
          ↓
    Reward

The neural network provides a much more expressive representation of the reward.

The Maximum Entropy formulation provides the probabilistic treatment of demonstrations.

Therefore, the overall idea is:

    Demonstrations
          ↓
    Maximum Entropy IRL
          +
    Neural Network
          ↓
    Nonlinear Reward

The authors show that deep networks can represent complex reward structures and can be trained efficiently in this IRL setting. :contentReference[oaicite:1]{index=1}

---

### 4. Simple Example

Imagine a human driving a car through a city.

Suppose the human avoids:

- obstacles,
- narrow roads,
- dangerous regions,
- sharp turns,
- and uncomfortable driving situations.

A traditional feature-based reward might be:

    Cost =
        w1 * obstacle_distance
        +
        w2 * road_curvature
        +
        w3 * distance
        +
        ...

The researcher has to manually decide these features.

But some important behavior may depend on interactions between several factors.

For example:

    narrow road
        +
    sharp turn
        +
    nearby obstacle

may produce a behavior that cannot easily be represented by a simple weighted sum.

The deep IRL approach allows a neural network to learn such nonlinear relationships.

Conceptually:

    Environment State
            ↓
       Neural Network
            ↓
      Learned Reward

---

### 5. Objective / Cost Representation

The major contribution of the paper is the use of a neural network as the reward-function approximator.

Instead of:

    Reward =
        w1 * Feature1
        +
        w2 * Feature2
        +
        ...

we have:

    Reward = NeuralNetwork(State / Features)

This allows the reward to contain nonlinear interactions between features.

The paper also investigates extending the architecture so that it can operate on raw input representations rather than depending entirely on manually precomputed spatial features. :contentReference[oaicite:2]{index=2}

---

### 6. Why This Is Important

This paper represents an important transition in the literature:

    Classical IRL
          ↓
    Hand-designed features
          ↓
    Learn feature weights

versus:

    Deep IRL
          ↓
    Neural representation
          ↓
    Learn complex nonlinear reward

This is highly relevant to our project because we do not yet know whether the human locomotion objective can be adequately described by a small number of manually selected terms.

---

### 7. Relation to Previous Papers

The progression is:

    Ng & Russell (2000)
            ↓
    Formal IRL problem

    Ziebart et al. (2008)
            ↓
    Probabilistic / Maximum Entropy IRL

    Wulfmeier et al. (2015/2016)
            ↓
    Deep / Nonlinear Maximum Entropy IRL

The conceptual progression is therefore:

    Demonstration
          ↓
    Infer Reward
          ↓
    Allow behavioral variability
          ↓
    Allow complex nonlinear reward representations

This progression is important for understanding the evolution of objective learning.

---

### 8. Validation

The paper evaluates the proposed approach on IRL benchmarks.

The authors report performance comparable to state-of-the-art methods on established benchmarks and improved performance on a benchmark with highly varying and complex reward structures. :contentReference[oaicite:3]{index=3}

The paper also considers larger neural architectures that reduce dependence on precomputed spatial features and allow learning from raw input representations. :contentReference[oaicite:4]{index=4}

The main validation therefore concerns:

    Can a deep reward model
    explain complex demonstration behavior?

The answer is demonstrated to be positive in the studied benchmark settings.

---

### 9. Main Finding

The main finding is:

> Neural networks can be used within Maximum Entropy IRL to represent complex, nonlinear reward functions that are difficult to express using manually designed linear feature combinations.

This significantly increases the representational capacity of IRL.

In simple terms:

    Old approach:

    Human designs features
            ↓
    IRL learns weights


    Deep IRL:

    Human provides demonstrations
            ↓
    Neural network represents reward
            ↓
    IRL learns the reward

The paper therefore shows that reward learning does not have to be restricted to a simple weighted sum of predefined features. :contentReference[oaicite:5]{index=5}

---

### 10. Important Limitation: Neural Reward Is Not Automatically a Human Objective

This is extremely important for our project.

A neural network can learn a function that explains demonstrations well.

But this does not automatically mean that the network has discovered the meaningful human objective.

For example:

    Human Motion
          ↓
    Neural Network
          ↓
    Reward

The network may learn a complicated function that predicts human behavior.

But we may still not know whether that function represents:

- energy,
- balance,
- smoothness,
- comfort,
- speed,
- robustness,
- task success,
- or interactions between these factors.

Therefore:

    Learned Neural Reward
            ≠
    Guaranteed Human Objective

This distinction must remain explicit in our project.

---

### 11. Representation Limitation

Although the neural network is much more expressive than a simple linear feature model, the input representation still matters.

The network learns a mapping from its available inputs to reward.

Therefore:

    Input Representation
            ↓
       Neural Network
            ↓
          Reward

If important information is absent from the input, the network cannot recover it.

This creates an important question for our project:

> What information about human motion should be provided to the objective-learning system?

This question belongs later in:

    04_03 Human Data

and:

    04_04 Objective Representation

It should not be decided at the literature stage.

---

### 12. No Human Locomotion

The paper does not study human walking or running as its central problem.

Therefore, it does not tell us:

> What objective humans use for locomotion.

It only tells us that:

> A complex nonlinear reward can be learned from demonstrations using deep IRL.

This distinction is important.

We cannot use this paper as evidence that human locomotion optimizes a particular set of objectives.

---

### 13. No Humanoid Transfer

The paper does not address the problem:

    Human
      ↓
    Learned Objective
      ↓
    Different Robot
      ↓
    New Robot Behavior

In particular, it does not study:

- human-to-humanoid transfer,
- morphology differences,
- robot-specific dynamics,
- contact constraints,
- actuator limits,
- whole-body balance,
- or H1 locomotion.

Therefore, the transfer problem remains open.

---

### 14. No Model-Based Humanoid MPC

The paper focuses on learning the reward/cost function.

It does not demonstrate the complete pipeline:

    Human Demonstrations
            ↓
    Learned Human Objective
            ↓
       H1 Dynamics
            +
       H1 Constraints
            ↓
           MPC
            ↓
       H1 Behavior

Therefore, it does not solve the final control problem of our project.

---

### 15. Generalization Limitation

The paper demonstrates that learned nonlinear reward functions can generalize within the studied problem settings.

However, it does not establish generalization across substantially different physical systems.

In particular, it does not demonstrate:

    Human Dynamics
          ↓
    Learned Objective
          ↓
    H1 Dynamics

Therefore, we cannot claim from this paper that a learned reward is automatically transferable across embodiments.

---

### 16. Relevance to Our Project

**Relevance: High**

This paper is highly relevant to our Phase 4 because it establishes an important possibility:

> The underlying reward/cost does not necessarily have to be represented as a simple weighted combination of manually designed features.

This is directly relevant to our current uncertainty about objective representation.

We currently do NOT know whether the human locomotion objective should be:

    Linear weighted sum

or:

    Nonlinear function

or:

    Latent representation

or:

    Another structure entirely.

Wulfmeier et al. show that nonlinear learned reward functions are technically possible.

They do not tell us that a neural reward is necessarily the correct representation for human locomotion.

---

### 17. Research Gap Contribution

This paper means that the following is NOT a sufficient novelty claim:

> "We use a neural network to learn the reward from human demonstrations."

Deep IRL has already established this direction.

Similarly, the following is not sufficient:

> "Our reward is nonlinear."

That is also established by the deep IRL literature.

Therefore, if our project uses a neural network, the novelty cannot simply be the neural network itself.

A potentially more important distinction is:

    Deep IRL:
        Learn a complex reward that explains demonstrations

versus our target:

    Human demonstrations
            ↓
    Objective with meaningful structure
            ↓
    Transfer across embodiment
            ↓
    H1 dynamics + constraints
            ↓
    MPC
            ↓
    Generalizable behavior

Whether this difference represents a genuine research gap is:

**NOT ESTABLISHED YET**

It must be checked against the human locomotion, humanoid, and model-based control literature.

---

### 18. Important Implication for Our Project

This paper gives us an important warning:

**Do not confuse model capacity with objective meaning.**

A sufficiently powerful neural network may be able to fit demonstrations very well.

But:

    Good demonstration fit
            ≠
    Meaningful human objective

Therefore, our future evaluation should not only ask:

> Can the learned objective reproduce the training demonstrations?

It should also ask:

> Does the learned objective produce useful behavior under new conditions?

and eventually:

> Does the learned objective remain useful when optimized using H1's own dynamics and constraints?

This connects directly to our planned:

    04_08 Held-out Evaluation

and:

    04_09 Analysis

---

### 19. Difference Between Wulfmeier et al. and Our Project

Wulfmeier et al.:

    Demonstrations
          ↓
    Deep IRL
          ↓
    Nonlinear Reward
          ↓
    Explain / reproduce behavior

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
       H1-generated behavior

The important additional requirements in our project are:

- human locomotion,
- meaningful objective representation,
- generalization,
- different embodiment,
- different dynamics,
- physical constraints,
- and model-based control.

---

### 20. Important Lesson for Phase 4

This paper gives us the following principle:

> The objective representation should not be assumed to be a simple linear combination of manually selected features.

However, it does NOT imply:

> We should automatically use a neural network.

Therefore, the correct decision at the current stage is:

    Candidate:
    Neural nonlinear objective

    Status:
    Possible

    Decision:
    Not yet established

The final objective representation should be selected only after the remaining literature and experiments.

---

### 21. Position in Our Literature Review

| Question | Wulfmeier et al. (2015/2016) |
|---|---|
| Demonstrations used? | Yes |
| IRL used? | Yes |
| Maximum Entropy IRL? | Yes |
| Neural network reward? | Yes |
| Nonlinear reward? | Yes |
| Complex reward structure? | Yes |
| Human demonstrations? | General demonstrations; not human locomotion |
| Human locomotion? | No |
| Latent human objective? | Not established |
| Interpretable human objective? | Not guaranteed |
| Objective representation learned from scratch? | Partially, via neural approximation |
| Robot morphology transfer? | No |
| Different dynamics transfer? | No |
| Humanoid robot? | No |
| MPC integration? | No |
| H1-specific constraints? | No |
| Generalizable objective across embodiments? | No |

---

### 22. Role in Our Project

**Overall Role:**

**Important bridge from classical feature-based IRL to nonlinear/deep objective learning.**

The paper shows:

    Classical IRL
          ↓
    Hand-designed features
          ↓
    Learn weights

can be extended to:

    Deep IRL
          ↓
    Neural reward representation
          ↓
    Learn complex nonlinear reward

For our project, this is important because we have not yet established that human locomotion objectives can be represented by a small set of manually selected costs.

However, this paper does not solve the key problem we ultimately care about:

    Human Objective
          ↓
    Different Humanoid
          ↓
    Robot Dynamics + Constraints
          ↓
    MPC
          ↓
    Generalizable Behavior

---

### 23. Final Takeaway

The most important lesson from Wulfmeier et al. is:

> A reward learned from demonstrations can be much more complex than a simple weighted sum of hand-designed features.

But the equally important warning is:

> A powerful neural reward model that fits demonstrations well is not automatically the true or meaningful human objective.

Therefore, for our project:

    Neural Reward
         ↓
    Candidate representation

not:

    Neural Reward
         ↓
    Assumed final solution

**Status: Required**

**Reason:**  
This paper is necessary for understanding how modern IRL can learn nonlinear reward functions and for preventing us from incorrectly claiming novelty for simply using a neural network to learn an objective.






## Paper 14 — Veerkamp et al. (2021)

**Citation**  
Veerkamp, K., Waterval, N. F. J., Geijtenbeek, T., Carty, C. P., Lloyd, D. G., Harlaar, J., & van der Krogt, M. M. (2021). *Evaluating Cost Function Criteria in Predicting Healthy Gait*. Journal of Biomechanics, 123, 110530. DOI: 10.1016/j.jbiomech.2021.110530.

**Literature Category**  
Human Motion / Human Locomotion Objectives / Computational Biomechanics / Predictive Simulation / Composite Cost Functions

---

### 1. Research Problem

The paper investigates a fundamental question in computational models of human walking:

> What objective or cost function can best explain healthy human gait?

Predictive simulations of human gait require an optimization objective. However, it is not known exactly which criteria humans optimize when walking.

The authors therefore investigate several physiologically motivated candidate criteria and ask:

> Which criteria, individually or in combination, can produce a gait that resembles experimentally observed healthy human walking?

This is directly relevant to our project because our project also needs to determine what objective may underlie human locomotion.

However, there is an important difference:

Veerkamp et al. test predefined candidate costs in a forward simulation.

Our project aims to infer an objective from human demonstrations and eventually use it on a different humanoid robot.

---

### 2. Input

The study uses:

- Experimental data describing healthy human gait
- A generic planar musculoskeletal model
- 18 Hill-type muscles
- A parameterized reflex-based controller
- Several candidate physiological cost functions

The candidate criteria include:

1. Cost of transport
2. Muscle activity
3. Head stability
4. Foot-ground impact
5. Knee ligament use / knee hyperextension

The simulation is then optimized using these criteria.

Therefore:

- Human locomotion: Yes
- Healthy gait: Yes
- Human experimental data: Yes
- Forward dynamic simulation: Yes
- Musculoskeletal model: Yes
- IOC: No
- IRL: No
- Humanoid robot: No
- H1: No
- MPC on a robot: No

---

### 3. Method

The paper follows a forward-optimization approach.

The basic procedure is:

    Candidate Cost
          ↓
    Optimize Human Model
          ↓
    Predicted Gait
          ↓
    Compare with Experimental Human Gait

First, each candidate criterion is optimized separately.

For example:

    Minimize Energy
          ↓
    Predicted gait

or:

    Minimize Muscle Activity
          ↓
    Predicted gait

or:

    Minimize Head Motion
          ↓
    Predicted gait

The predicted gait is then compared with experimentally observed healthy gait.

After evaluating the individual criteria, the authors construct a combined cost function with weighted criteria.

Conceptually:

    J =
        w1 * Cost_of_Transport
        +
        w2 * Muscle_Activity
        +
        w3 * Head_Stability
        +
        w4 * Foot_Ground_Impact
        +
        w5 * Knee_Extension

The weights are optimized to improve agreement between simulated and experimental gait.

---

### 4. Simple Interpretation

Imagine we want to understand why a human walks the way they do.

We propose several possible reasons:

    Human may want to:

    - use less energy
    - activate muscles less
    - keep the head stable
    - reduce impact when the foot hits the ground
    - avoid stressing the knee

Now suppose we tell a simulated human:

    "Only minimize energy."

It produces one walking pattern.

Then:

    "Only minimize muscle activity."

It produces another walking pattern.

Then:

    "Only minimize head movement."

It produces another walking pattern.

The question is:

> Which one looks most like real human walking?

The paper finds that no single criterion is sufficient to reproduce all aspects of healthy gait well.

A carefully weighted combination performs substantially better.

---

### 5. Objective / Cost

The paper evaluates five candidate criteria:

#### 5.1 Cost of Transport

This represents the energetic cost associated with moving the body over a distance.

Conceptually:

    Lower energy per distance
            ↓
       Better gait

---

#### 5.2 Muscle Activity

This criterion penalizes high muscle activation.

Conceptually:

    Less muscle activation
            ↓
       Lower cost

This can be interpreted as a possible strategy for reducing muscular effort or fatigue.

---

#### 5.3 Head Stability

This criterion penalizes excessive movement of the head.

Conceptually:

    More stable head
            ↓
       Lower cost

This is motivated by the sensory role of head motion during walking.

---

#### 5.4 Foot-Ground Impact

This criterion penalizes impact associated with the foot contacting the ground.

Conceptually:

    Smaller impact
            ↓
       Lower cost

This represents a possible preference to reduce mechanical loading during foot-ground contact.

---

#### 5.5 Knee Ligament Use / Knee Hyperextension

This criterion penalizes excessive knee extension/hyperextension and associated ligament loading.

Conceptually:

    Avoid extreme knee configuration
            ↓
       Lower cost

---

### 6. Individual Criteria vs. Combined Cost

A major result is that the individual criteria explain different aspects of human gait.

When each criterion is optimized independently, the agreement with experimental gait is limited.

The reported overall coefficients of determination for the individual criteria were approximately:

    R² = 0.37 – 0.56

with RMSE values of approximately:

    3.47 – 4.63 SD

The authors then construct an optimally weighted combined cost.

The combined objective achieves approximately:

    R² = 0.72

with:

    RMSE = 2.10 SD

The combined cost therefore provides substantially better agreement with experimental healthy gait within the studied simulation framework. The authors conclude that careful weighting of multiple criteria is important for predicting healthy gait. 

---

### 7. Main Finding

The central finding is:

> No single tested physiological criterion was sufficient to reproduce all characteristics of healthy human gait, while a carefully weighted combination of criteria produced substantially better agreement with experimental gait.

This provides evidence that human locomotion may be influenced by multiple competing or complementary objectives.

However, this should NOT be interpreted as proof that the human brain literally optimizes exactly these five criteria.

The paper demonstrates that this combination is useful for explaining/synthesizing gait within the chosen simulation framework.

---

### 8. Important Limitation: This Is Not IOC

This distinction is critical for our project.

Veerkamp et al. do NOT start with:

    Human Demonstration
          ↓
    Infer Objective

Instead, they start with:

    Candidate Objective
          ↓
    Forward Simulation
          ↓
    Generate Gait
          ↓
    Compare with Human Gait

Therefore:

    Forward Optimization:

    Objective → Motion

whereas our target direction is:

    Objective Inference:

    Motion → Objective

This is the fundamental difference between this work and our planned IOC/IRL approach.

---

### 9. Important Limitation: Candidate Objectives Are Predefined

The authors choose the candidate criteria beforehand.

They do not ask:

> Can an unknown objective representation be discovered directly from human demonstrations?

Instead, they ask:

> Which of these physiologically motivated criteria, and what combination of their weights, best predicts healthy gait?

Therefore:

    Learning weights
          ≠
    Discovering the objective representation

This distinction is important for our project.

---

### 10. What the Paper Tells Us About Candidate Human Objectives

This paper is especially useful because it provides locomotion-specific evidence for several candidate objective components.

Before this paper, we might have simply guessed:

    Energy
    Stability
    Smoothness
    Robustness
    Task success

After this paper, we have stronger literature support that several physiologically motivated criteria have actually been investigated in human gait modeling.

In particular:

- energetic cost,
- muscle activity,
- head stability,
- foot-ground impact,
- knee loading / hyperextension

have all been explicitly tested as possible contributors to healthy gait.

However:

> These should still be treated as candidate hypotheses, not established ground-truth components of the human objective.

---

### 11. Important Limitation: Healthy Gait Only

The study focuses on healthy gait.

It does not investigate whether the same objective remains valid under:

- perturbations,
- uneven terrain,
- obstacles,
- stairs,
- different walking speeds,
- running,
- carrying objects,
- external disturbances,
- or different tasks.

Therefore, the study does not establish that the identified weighted cost is a universal human locomotion objective.

---

### 12. Important Limitation: Human Model, Not Robot

The model is a generic planar musculoskeletal human model.

It does not represent:

- Unitree H1,
- humanoid robot actuators,
- robot torque limits,
- robot contact constraints,
- robot morphology,
- robot whole-body dynamics,
- robot control architecture.

Therefore, the paper does not address:

    Human Objective
          ↓
    Different Robot Dynamics
          ↓
    Robot Motion

This is a central part of our project.

---

### 13. No Human-to-Robot Transfer

The paper does not investigate whether the inferred/selected cost can be transferred from a human to a robot with different morphology.

There is no:

    Human
      ↓
    Objective
      ↓
    H1

transfer experiment.

Therefore, the embodiment-transfer question remains open in this paper.

---

### 14. No Learned Latent Objective

The combined cost is still constructed from explicitly defined candidate criteria.

Conceptually:

    Human-designed criteria
              ↓
       Optimize weights
              ↓
       Combined objective

Our desired direction is:

    Human demonstrations
              ↓
       Infer objective
              ↓
       Objective representation
              ↓
       Optimize on H1

Therefore, Veerkamp et al. provides evidence for the importance of composite objectives, but does not solve latent objective inference.

---

### 15. Relevance to Our Project

**Relevance: Very High**

This is one of the most directly relevant papers in the Human Motion / Locomotion Objectives category.

The reason is simple:

It directly studies:

    Human locomotion
          +
    Cost functions
          +
    Optimization
          +
    Healthy gait prediction

It therefore helps answer an important preliminary question:

> Are there scientifically motivated candidate objectives that can explain human locomotion?

The answer is clearly yes.

However, it does not answer our final question:

> Can the underlying objective be inferred from human demonstrations and then optimized by a humanoid with different dynamics and constraints?

---

### 16. Research Gap Contribution

This paper means that the following would NOT be a sufficient novelty claim:

> "We use a combination of multiple cost functions for human locomotion."

That has already been investigated.

Similarly, this is not sufficient:

> "Human locomotion can be explained better by a weighted combination of several objectives."

Veerkamp et al. provide direct evidence for this within their simulation framework.

Therefore, our novelty cannot simply be:

    Composite Human Locomotion Cost

A potentially more interesting distinction is:

    Existing work:

    Predefined locomotion costs
              ↓
       Optimize weights
              ↓
       Reproduce human gait


    Our target:

    Human demonstrations
              ↓
       Infer objective
              ↓
       Learn objective representation
              ↓
       Transfer to H1
              ↓
       H1 dynamics + constraints
              ↓
             MPC

Whether this constitutes a genuine research gap is:

**NOT ESTABLISHED YET**

It must be tested against the remaining IOC, IRL, humanoid, and model-based-control literature.

---

### 17. Implications for Our Objective Representation

This paper gives us an important design consideration for Phase 4.

There are at least two possible directions:

#### Direction A — Explicit composite objective

    J =
        w1 * Energy
        +
        w2 * Muscle Cost
        +
        w3 * Stability
        + ...

Advantages:

- interpretable
- physically meaningful
- easier to analyze
- easier to transfer into MPC

Disadvantage:

- requires us to choose the candidate components beforehand

---

#### Direction B — More general learned objective

    Human Motion
          ↓
    Learned Representation
          ↓
    Objective / Cost

Advantages:

- potentially captures nonlinear interactions
- does not require all objective components to be specified beforehand

Disadvantages:

- potentially less interpretable
- harder to verify
- may overfit demonstrations
- difficult to use safely inside MPC
- transfer behavior is uncertain

The literature review must help determine which direction is scientifically justified.

No final decision should be made yet.

---

### 18. Relation to Our Earlier Papers

This paper connects strongly to Berret et al. (2011).

Berret et al.:

    Human Arm Motion
          ↓
    IOC
          ↓
    Composite Cost
          ↓
    Infer weights of candidate costs

Veerkamp et al.:

    Human Locomotion
          ↓
    Candidate Costs
          ↓
    Forward Simulation
          ↓
    Optimize weights
          ↓
    Predict Human Gait

The difference is:

    Berret:
    Motion → Objective

    Veerkamp:
    Objective → Motion

This distinction should remain explicit in our literature matrix.

---

### 19. Relation to Our Final Pipeline

Veerkamp et al. address approximately:

    Candidate Human Costs
            ↓
       Human Dynamics
            ↓
      Forward Simulation
            ↓
       Human-like Gait

Our target pipeline is:

    Human Demonstrations
            ↓
     Latent Objective
            ↓
         H1 Model
            +
     H1 Constraints
            ↓
           MPC
            ↓
       H1 Behavior
            ↓
      Generalization

Therefore, the paper supports the motivation for the "objective" part of our project, but not the inference, transfer, or MPC parts.

---

### 20. Position in Our Literature Review

| Question | Veerkamp et al. (2021) |
|---|---|
| Human motion? | Yes |
| Human locomotion? | Yes |
| Healthy gait? | Yes |
| Cost functions? | Yes |
| Multiple candidate objectives? | Yes |
| Composite objective? | Yes |
| Weight optimization? | Yes |
| Forward simulation? | Yes |
| Experimental gait comparison? | Yes |
| IOC? | No |
| IRL? | No |
| Objective inferred from demonstrations? | No |
| Objective representation learned from scratch? | No |
| Neural objective? | No |
| Humanoid robot? | No |
| H1? | No |
| Human-to-robot transfer? | No |
| Different morphology? | No |
| Different dynamics? | No |
| MPC integration? | No |
| Generalization across embodiments? | No |

---

### 21. Role in Our Project

**Overall Role:**

**Core human-locomotion objective paper.**

This paper provides strong evidence that:

> Multiple physiologically motivated criteria may contribute to the generation of human gait, and their relative weighting can strongly affect the predicted walking pattern.

It also gives us a scientifically grounded list of candidate locomotion objectives rather than forcing us to invent them ourselves.

However:

> The paper does not demonstrate that these criteria constitute the true underlying neural objective of human locomotion.

And:

> It does not demonstrate that such an objective can be inferred from demonstrations and transferred to a different humanoid.

---

### 22. Final Takeaway

The most important lesson for our project is:

    Human locomotion
          ↓
    probably not explained well
    by one simple cost
          ↓
    multiple criteria can matter

But the next question is the one our project is interested in:

    Which objective actually explains
    the observed human demonstrations?

And then:

    Can that objective still be useful
    when optimized using H1's
    own dynamics and constraints?

Veerkamp et al. answer the first part only indirectly.

They show that carefully weighted combinations of candidate criteria can predict healthy gait well.

They do NOT perform:

    Human Motion
          ↓
    IOC / IRL
          ↓
    Learned Objective
          ↓
    H1
          ↓
    MPC

Therefore:

**Status: Required**

**Research-gap status: Not established yet**

**Key contribution to our literature review:**
This paper establishes that human locomotion objective design is a real and nontrivial problem, and that composite cost functions can substantially improve gait prediction. It also gives us experimentally grounded candidate objective components that can later be considered when designing and interpreting our latent objective representation.






## Paper 15 — Feldman et al. (2026)

**Citation**  
Feldman, J. N., Morales Loro, D., Chin, A., Erickson, S., Li, S., Bonbrest, E., & Slade, P. (2026). *Estimating and Interpreting How Humans Prioritize Multiple Movement Goals During Walking*. Journal of NeuroEngineering and Rehabilitation, 23, 184. https://doi.org/10.1186/s12984-026-01972-1

**Literature Category**  
Human Motion / Human Locomotion Objectives / Multiple Movement Goals / Human Motor Behavior / Goal Prioritization

---

### 1. Research Problem

Human walking is influenced by multiple movement goals that can compete with each other.

For example, while walking, a person may simultaneously want to:

- maintain a desired walking speed,
- maintain balance,
- place the feet accurately,
- reduce energy expenditure.

The paper asks:

> Can we determine which movement goals a person is prioritizing by observing how their gait changes?

The important idea is that human walking may not be generated by one fixed objective.

Instead, different people, or even the same person under different conditions, may assign different priorities to different movement goals.

---

### 2. Input

The study uses experimental human walking data.

Participants performed overground walking under systematically varied movement-goal conditions.

The experiment manipulated four movement goals:

1. Walking speed
2. Balance
3. Foot placement accuracy
4. Energy expenditure

The researchers collected several types of measurements, including:

- full-body motion capture,
- inertial measurement units (IMUs),
- surface EMG,
- metabolic/energy measurements,
- spatiotemporal gait metrics.

The experiment included 27 walking conditions designed to systematically vary the movement-goal demands.

Therefore:

- Human demonstrations/motion: Yes
- Human locomotion: Yes
- Multiple movement goals: Yes
- Experimental gait data: Yes
- IOC: No
- IRL: No
- Humanoid robot: No
- H1: No
- MPC: No

---

### 3. Method

The researchers systematically change the demands placed on the participant.

For example:

    Walk slowly
    +
    Maintain balance
    +
    Ignore foot placement

or:

    Walk fast
    +
    Maintain balance
    +
    Accurate foot placement

They then observe how gait changes.

The basic idea is:

    Movement Goal Prompt
            ↓
       Human Walking
            ↓
       Gait Metrics
            ↓
    Estimate Goal Priority

The study uses gait metrics and regression models to estimate the perceived ranking of movement goals.

The authors report that subject-agnostic models estimated the perceived ordering of goal importance with approximately 21% error, while subject-specific models reduced the error to approximately 11%. :contentReference[oaicite:1]{index=1}

---

### 4. Simple Example

Imagine telling a person:

    "Walk normally."

They choose their own walking strategy.

Now tell them:

    "Walk very fast."

Their gait changes.

Now:

    "Walk fast and carefully place your feet."

Their gait changes again.

Now:

    "Walk fast, carefully place your feet,
     and maintain balance."

Their gait becomes even more constrained.

Different people may respond differently.

For example:

    Person A:

    Balance
       >
    Foot placement
       >
    Speed

while another person may behave more like:

    Speed
       >
    Foot placement
       >
    Balance

The paper investigates whether these differences in priority can be inferred from measurable gait changes.

---

### 5. Movement Goals Studied

The paper focuses on four goals.

#### 5.1 Walking Speed

The participant is instructed to walk:

- slowly,
- at their typical speed,
- or quickly.

The resulting walking speed provides a direct measure of how the speed goal influences gait.

---

#### 5.2 Balance

The study manipulates visual information using a visual perturbation system.

The purpose is to create different demands on balance.

The resulting gait changes, such as changes in step-width variability, provide information about balance-related prioritization.

---

#### 5.3 Foot Placement Accuracy

Participants are given different instructions regarding how accurately they should place their feet.

The resulting foot-placement error and step-length variability provide information about the importance assigned to this goal.

---

#### 5.4 Energy Expenditure

Energy expenditure is included as an important movement goal because humans are known to regulate locomotion partly according to energetic cost.

The study therefore considers energy alongside speed, balance, and foot placement rather than treating walking as a single-objective problem.

---

### 6. Main Finding

The main finding is:

> Human walking reflects multiple competing movement goals, and individuals can use different movement strategies when the relative demands of these goals change.

The researchers found that gait became increasingly heterogeneous across participants as the walking conditions involved more demanding combinations of goals.

This suggests that different people may resolve the same set of competing movement goals differently.

The study also found systematic relationships between perceived goal importance and corresponding gait metrics, particularly for visually guided goals such as balance and foot placement. :contentReference[oaicite:2]{index=2}

---

### 7. Important Finding for Our Project: Individual Differences

One of the most important results for our project is that people do not necessarily respond identically to the same movement-goal conditions.

As the number of competing goals increased, individual gait strategies became more heterogeneous.

Conceptually:

    Same environment
          +
    Same instructions
          ↓
    Different humans
          ↓
    Different gait strategies

This suggests that human locomotion may contain an individual-specific component.

Therefore, it may be dangerous to assume:

    One universal human objective
              ↓
    Every human

A more realistic possibility is:

    Shared objective structure
              +
    Individual preferences
              ↓
    Individual movement

This is an important observation for our future generalization experiments.

---

### 8. Objective / Cost Interpretation

The paper does not directly learn a mathematical cost function of the form:

    J =
        w1 * Energy
        +
        w2 * Balance
        +
        w3 * FootPlacement
        +
        w4 * Speed

Instead, it estimates the perceived priority/order of movement goals from gait measurements.

Therefore:

    Goal Priority Estimation
            ≠
    Full Cost Function Identification

This distinction is critical.

The paper tells us something about:

    "Which goal appears more important?"

It does not fully identify:

    "What exact mathematical objective does the human optimize?"

---

### 9. No IOC

This paper is NOT an Inverse Optimal Control method.

The direction is approximately:

    Goal Manipulation
            ↓
       Human Motion
            ↓
       Gait Metrics
            ↓
    Estimate Goal Priority

IOC would instead attempt:

    Observed Human Motion
            ↓
    Infer Objective / Cost

Therefore, Feldman et al. should not be categorized as IOC.

---

### 10. No IRL

The paper also does not use Inverse Reinforcement Learning to recover a reward function from demonstrations.

There is no learned reward of the form:

    R(s,a)

or:

    J(trajectory)

that is subsequently optimized to generate human walking.

Therefore:

    Feldman et al.
        ≠
    IRL

The contribution is primarily experimental characterization and regression-based estimation of movement-goal priorities.

---

### 11. Important Limitation: Goals Are Predefined

The four movement goals are specified by the researchers:

    Speed
    Balance
    Foot Placement
    Energy

The method does not discover completely unknown goals from raw motion.

Therefore:

    Predefined Goals
          ↓
    Estimate Priorities

rather than:

    Raw Demonstrations
          ↓
    Discover Unknown Objective

This is an important limitation relative to our project.

---

### 12. Important Limitation: Goal Priority Is Not a Complete Objective

Knowing that:

    Balance > Speed

does not tell us the exact mathematical cost function.

For example, these two objectives could both imply:

    Balance > Speed

but produce different behavior:

    J1 =
        5 * Balance
        +
        1 * Speed

versus:

    J2 =
        nonlinear_function(Balance, Speed)

Therefore:

    Goal Ranking
        ≠
    Complete Objective Representation

Our project ultimately needs an objective that can be inserted into a model-based controller.

---

### 13. Important Limitation: No Robot Transfer

The paper does not test whether the estimated goal priorities can be transferred to a robot.

There is no:

    Human
      ↓
    Estimated Objective
      ↓
    Humanoid
      ↓
    Robot-specific dynamics

experiment.

Therefore, embodiment transfer remains outside the scope of this paper.

---

### 14. Important Limitation: No MPC

The estimated movement priorities are not used as the cost function of a model-based MPC controller.

The paper does not demonstrate:

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
        H1 Motion

Therefore, the final control stage of our project is not addressed.

---

### 15. Important Limitation: Experimental Population

The experiment focuses on young, healthy adults.

Therefore, the findings do not automatically generalize to:

- older adults,
- injured individuals,
- people with neurological disorders,
- athletes,
- children,
- humanoid robots,
- or arbitrary locomotion conditions.

The authors explicitly describe the study as an initial framework that could be extended beyond the laboratory. :contentReference[oaicite:3]{index=3}

---

### 16. Relevance to Our Project

**Relevance: Very High**

This paper is highly relevant because it provides recent experimental evidence that:

1. Human walking involves multiple movement goals.
2. These goals can compete with each other.
3. People change their gait when goal demands change.
4. Different people can adopt different strategies.
5. Gait measurements contain information about movement-goal priorities. :contentReference[oaicite:4]{index=4}

This directly supports the motivation for studying a latent human objective rather than assuming that human motion is generated by a single universal cost.

---

### 17. Relation to Veerkamp et al. (2021)

These two papers provide complementary evidence.

#### Veerkamp et al. (2021)

The question is approximately:

    Which predefined cost functions
    can generate human-like gait?

The approach is:

    Candidate Costs
          ↓
    Forward Optimization
          ↓
    Predicted Gait
          ↓
    Compare with Human Gait

---

#### Feldman et al. (2026)

The question is approximately:

    Which movement goals are people
    prioritizing during walking?

The approach is:

    Goal Manipulation
          ↓
    Human Walking
          ↓
    Gait Metrics
          ↓
    Estimate Goal Priority

---

Together they suggest:

    Human Locomotion
          ↓
    Multiple Goals
          ↓
    Different Relative Priorities
          ↓
    Different Movement Strategies

This is highly relevant to the concept of a latent objective.

---

### 18. Relation to Our Project

The current project asks:

    Human Demonstrations
            ↓
    Latent Human Objective
            ↓
    H1 Dynamics
            +
    H1 Constraints
            ↓
           MPC
            ↓
    Generalizable H1 Behavior

Feldman et al. address only part of this pipeline:

    Human Walking
          ↓
    Multiple Movement Goals
          ↓
    Estimate Goal Priorities

They do not perform:

    Objective Inference
          ↓
    Robot Transfer
          ↓
    MPC

Therefore, the paper provides motivation and experimental evidence for the first part of our project but does not solve the final research problem.

---

### 19. Research Gap Contribution

This paper makes the following novelty claim insufficient:

> "Human walking has multiple objectives."

This is already supported by recent experimental literature.

Similarly, this is insufficient:

> "Different humans can prioritize locomotion objectives differently."

This is also directly supported by Feldman et al.

Therefore, our project cannot claim novelty simply from:

    Multiple Human Locomotion Objectives

or:

    Individual Objective Preferences

A potentially more interesting research question is:

    Can the underlying objective structure
    or cost function be inferred directly
    from human demonstrations,

    and can that inferred objective be optimized
    under the dynamics and constraints of
    a different humanoid?

However:

**This research gap is NOT ESTABLISHED YET.**

It must be checked against the remaining IOC, IRL, human-to-humanoid, MPC, and RoMeLa literature.

---

### 20. Implication for "Generalizable Objective"

This paper gives us an important warning about the word "generalizable."

Suppose we learn:

    Objective from Person A

We cannot automatically assume:

    Objective from Person A
            =
    Objective of all humans

because individual movement strategies differ.

Therefore, our future experiments may need to distinguish between:

    Person-specific objective

and:

    Shared / generalizable objective structure

However, this should NOT yet be added to the formal problem formulation.

For now it is a literature-derived hypothesis.

---

### 21. Implication for Human Data

The paper also supports the idea that simply collecting trajectories may not be enough.

Useful information may include:

- walking speed,
- step width,
- foot placement,
- balance-related metrics,
- energy expenditure,
- task/context information.

This suggests that human demonstrations should eventually be represented with more than just joint-angle trajectories.

However:

**Decision deferred.**

The exact human-data representation belongs to:

    04_03 Human Data

and should not be finalized during the literature review.

---

### 22. Position in Our Literature Review

| Question | Feldman et al. (2026) |
|---|---|
| Human motion? | Yes |
| Human locomotion? | Yes |
| Multiple movement goals? | Yes |
| Goal prioritization? | Yes |
| Individual differences? | Yes |
| Experimental human data? | Yes |
| Motion capture? | Yes |
| IMU? | Yes |
| EMG? | Yes |
| Energy measurement? | Yes |
| Regression-based estimation? | Yes |
| IOC? | No |
| IRL? | No |
| Full cost-function inference? | No |
| Latent objective discovery? | No |
| Predefined candidate goals? | Yes |
| Humanoid robot? | No |
| H1? | No |
| Human-to-robot transfer? | No |
| Different dynamics? | No |
| MPC integration? | No |
| Generalization across embodiments? | No |

---

### 23. Role in Our Project

**Overall Role:**

**Core recent evidence for multiple and person-dependent human locomotion goals.**

The paper strengthens the motivation for our project by showing that human walking should not necessarily be viewed as the optimization of one fixed objective.

It also introduces an important consideration:

    Human locomotion
          ↓
    Multiple competing goals
          ↓
    Individual prioritization
          ↓
    Different gait strategies

This makes the concept of a "latent human objective" more interesting, but also more difficult.

---

### 24. Final Takeaway

The most important lesson from Feldman et al. is:

> Human walking involves multiple competing movement goals, and different people can prioritize these goals differently.

For our project, this means:

    Do NOT assume:

    One fixed universal cost

Instead, the literature now supports considering:

    Multiple goals
          +
    Trade-offs
          +
    Individual variation

However, Feldman et al. do not determine the complete mathematical objective, do not use IOC/IRL to recover it, and do not transfer it to a humanoid.

Therefore:

**Status: Required**

**Research-gap status: Not established yet**

**Key contribution to our literature review:**

This paper provides recent experimental evidence that gait contains information about the relative priorities of multiple movement goals and that these priorities can be person-specific. This strengthens the motivation for learning an objective from human demonstrations, while simultaneously warning us that "the human objective" may not be a single universal function shared identically by every person.







## Paper 16 — Zhang et al. (2025)

**Citation**  
Zhang, J. Z., Howell, T. A., Yi, Z., Pan, C., Shi, G., Qu, G., Erez, T., Tassa, Y., & Manchester, Z. (2025). *Whole-Body Model-Predictive Control of Legged Robots with MuJoCo*. arXiv preprint arXiv:2503.04613.

**Literature Category**  
Model-Based Control / Model-Predictive Control (MPC) / Whole-Body Humanoid Control / iLQR / Legged Robots

---

### 1. Research Problem

The paper investigates whether real-time whole-body model-predictive control can be implemented for complex legged robots, including humanoids, using a relatively simple and reproducible approach.

The central question is:

> Can a whole-body MPC based on a standard physics engine and a standard optimization method achieve effective real-time locomotion on real legged robots?

The paper focuses on the control problem rather than on learning the objective itself.

This is directly relevant to our project because our final pipeline requires:

    Learned Human Objective
            ↓
       Robot Dynamics
            ↓
           MPC
            ↓
      Humanoid Motion

Zhang et al. provide an important precedent for the final part of this pipeline:

    Robot Dynamics
            +
    Predefined Cost
            ↓
         iLQR / MPC
            ↓
      Humanoid Motion

---

### 2. Input

The controller uses:

- Robot state
- Robot dynamics modeled in MuJoCo
- A predefined objective/cost function
- Control inputs
- Contact dynamics
- Robot geometry and collision information

The method is evaluated in simulation and on real robot hardware.

The experiments include:

- dynamic quadruped locomotion,
- quadruped walking on two legs,
- other challenging whole-body behaviors,
- full-sized humanoid bipedal locomotion.

The hardware experiments include Unitree robots, including a full-sized Unitree H1 humanoid.

Therefore:

- Legged robot: Yes
- Humanoid: Yes
- Unitree H1: Yes
- Whole-body dynamics: Yes
- Real-time MPC: Yes
- Real hardware: Yes
- Human demonstrations: No
- Human objective learning: No
- IOC: No
- IRL: No

---

### 3. Method

The main method is:

    MuJoCo Dynamics
          ↓
        iLQR
          ↓
    Whole-Body MPC
          ↓
    Time-Varying LQR Feedback
          ↓
    Joint-Level PD Control
          ↓
        Robot

The main optimization problem is a nonlinear trajectory optimization problem:

    minimize

        Σ l(x_t, u_t) + l_f(x_T)

    subject to

        x_(t+1) = f(x_t, u_t)

where:

- x_t is the robot state,
- u_t is the control input,
- f represents robot dynamics,
- l is the running cost,
- l_f is the terminal cost.

The iLQR algorithm repeatedly approximates the nonlinear problem around the current trajectory and improves the control sequence.

---

### 4. Simple Explanation of iLQR

Suppose the H1 needs to walk forward.

The controller asks:

    "If I apply these torques for the next few steps,
     where will the robot end up?"

MuJoCo predicts the result.

Then the controller asks:

    "Can I change the torques slightly
     to get a better result?"

iLQR repeatedly performs this process:

    Guess control
        ↓
    Simulate
        ↓
    Measure cost
        ↓
    Improve control
        ↓
    Simulate again
        ↓
    Improve again

Eventually it obtains a good control sequence.

Because MPC repeatedly re-solves the problem from the current state, it can react to changes and disturbances.

---

### 5. What Is Important About the MPC Formulation?

The controller explicitly uses the robot's dynamics.

Conceptually:

    Robot Model
        +
    Objective
        ↓
    Optimization
        ↓
    Dynamically feasible motion

This is fundamentally different from simply replaying a trajectory.

For example:

    Human trajectory
          ↓
    Replay on H1

may fail because the human and H1 have different:

- masses,
- inertias,
- joint limits,
- actuator capabilities,
- contact properties,
- body proportions.

MPC instead asks:

    "Given H1's own dynamics,
     what motion minimizes the objective?"

This is exactly the model-based aspect that is important for our project.

---

### 6. Objective / Cost

The paper does NOT learn the objective.

The cost categories are designed beforehand.

Conceptually:

    Predefined Cost
          ↓
       Weights
          ↓
        iLQR
          ↓
    Optimal trajectory

The user can adjust cost weights and other parameters.

Therefore:

    Cost learning: No
    Cost inference: No
    Objective discovery: No

Instead:

    Cost design
        →
    Optimization
        →
    Robot behavior

This distinction is essential for our literature review.

---

### 7. Important Distinction for Our Project

Zhang et al. solve approximately:

    Objective
        ↓
    Robot Motion

Our project wants to solve:

    Human Motion
        ↓
    Human Objective
        ↓
    H1 Motion

Therefore:

    Zhang et al.

    Objective
       ↓
      MPC
       ↓
    Humanoid

versus:

    Our Project

    Human Demonstrations
       ↓
    Learned Objective
       ↓
    H1 MPC
       ↓
    Humanoid

The missing component in Zhang et al. is the objective-learning stage.

---

### 8. Whole-Body Control

The important feature of this work is that the controller reasons over the whole robot rather than treating locomotion as a simple low-dimensional problem.

The dynamics include the robot's full-body state and control inputs.

This is important for humanoids because walking depends on interactions between:

- torso,
- pelvis,
- legs,
- feet,
- contact forces,
- joint torques,
- balance,
- and whole-body momentum.

Therefore, the paper provides a useful precedent for eventually placing a learned objective inside a whole-body model-based controller.

---

### 9. Contact Dynamics

Legged robots are difficult to control with MPC because contact with the ground creates nonlinear and nonsmooth behavior.

For example:

    Foot in air
        ↓
    No ground force

versus:

    Foot touches ground
        ↓
    Contact force
        ↓
    New dynamics

The paper uses MuJoCo's contact model and finite-difference approximations of derivatives.

An important empirical result is that this relatively simple approach works surprisingly well despite model mismatch and the difficulties associated with contact dynamics.

---

### 10. Real-Time Control

One of the major contributions is demonstrating that whole-body iLQR can operate in real time on hardware.

The system architecture uses:

    iLQR planner
        ↓
    nominal trajectory
        +
    TV-LQR feedback gains
        ↓
    high-frequency controller
        ↓
    Joint PD
        ↓
    Hardware

The iLQR planner runs at a lower frequency while the feedback policy is updated at a higher frequency.

This makes the approach practical for real robot control.

---

### 11. Validation

The method is evaluated on both simulation and physical robot hardware.

The experiments include several challenging whole-body behaviors involving quadrupeds and humanoids.

Most importantly for our project, the authors demonstrate full-sized humanoid bipedal locomotion on hardware.

The paper therefore establishes that:

    Whole-Body Dynamics
          +
    MuJoCo
          +
    iLQR / MPC
          ↓
    Real Humanoid Locomotion

is experimentally feasible.

---

### 12. Main Finding

The main finding is:

> A relatively simple whole-body MPC implementation using MuJoCo dynamics, iLQR, and finite-difference derivatives can achieve effective real-time control of legged robots, including full-sized humanoids, on physical hardware.

This is important because whole-body nonlinear MPC is often considered computationally difficult due to:

- high-dimensional dynamics,
- contact,
- nonlinearities,
- real-time requirements,
- and derivative computation.

The paper shows that a simpler implementation can nevertheless work effectively.

---

### 13. Important Limitation: Objective Is Hand-Designed

The objective is not learned from demonstrations.

The cost categories are manually designed before optimization.

Therefore:

    Human Demonstrations
            ↓
    Learned Objective

is NOT addressed.

This is one of the largest differences between this work and our project.

---

### 14. Important Limitation: No Human Data

The paper does not use human demonstrations to infer the objective.

There is no:

    Human Motion
          ↓
    IOC / IRL
          ↓
    Cost

stage.

Therefore, it cannot answer our central Phase 4 question:

> What objective underlies human locomotion?

---

### 15. Important Limitation: No Human-to-Robot Objective Transfer

Although the controller can operate on humanoid hardware, it does not demonstrate:

    Human
      ↓
    Human Objective
      ↓
    H1

The objective is designed for the robot/control task rather than inferred from human behavior.

Therefore, human-to-humanoid objective transfer remains unaddressed.

---

### 16. Important Limitation: No Latent Objective

The paper does not learn a latent representation such as:

    z = latent human objective

followed by:

    z
    ↓
    H1 cost
    ↓
    MPC

There is no representation-learning component for discovering an unknown human objective.

---

### 17. Important Limitation: No Generalization of Human Objective

The paper demonstrates that its controller can generalize to real hardware with relatively few sim-to-real considerations.

However, this is not the same as our notion of objective generalization.

Their question is approximately:

    Does the MPC controller work
    when transferred from simulation
    to hardware?

Our question is:

    Does an objective learned from
    human demonstrations remain useful
    when optimized under different
    robot dynamics and conditions?

These are different forms of generalization.

---

### 18. Relevance to Our Project

**Relevance: Very High**

This paper is highly relevant to Phase 5 and Phase 6 because it provides a practical example of whole-body model-based MPC for humanoid locomotion.

It supports the feasibility of the downstream pipeline:

    Robot Dynamics
          +
    Cost Function
          ↓
        MPC
          ↓
    Whole-Body Humanoid Motion

This is precisely the control mechanism that we eventually want to use after learning the human objective.

---

### 19. Relation to Our Project Architecture

Our intended architecture is:

    Human Demonstrations
            ↓
    Latent Human Objective
            ↓
    H1-Compatible Cost
            ↓
    H1 Dynamics
            +
    H1 Constraints
            ↓
    Whole-Body MPC
            ↓
    H1 Behavior

Zhang et al. provide evidence for the right-hand side:

    H1 Dynamics
          +
    Cost
          ↓
        MPC
          ↓
    H1 Behavior

Therefore, this paper supports the feasibility of our final control stage but does not solve the objective-learning problem.

---

### 20. Relation to the "Different Robot Dynamics" Question

This paper reinforces an important conceptual advantage of our approach.

Suppose we directly imitate human motion:

    Human trajectory
          ↓
    H1

The trajectory may not be dynamically feasible for H1.

With MPC:

    Human-derived objective
            ↓
       H1 dynamics
            ↓
       H1 constraints
            ↓
       feasible H1 motion

The controller does not need to reproduce the human trajectory exactly.

Instead, it searches for a motion that satisfies the objective while obeying the robot's own physical model.

This is closely aligned with the motivation behind the project.

---

### 21. What This Paper Does NOT Prove

The paper does NOT prove that:

- human objectives can be learned,
- human objectives are transferable to robots,
- a learned human objective is sufficient for humanoid control,
- one objective is universal across humans,
- a learned objective will generalize across robot morphologies,
- MPC will automatically produce human-like behavior.

Those questions remain open.

---

### 22. Research Gap Contribution

This paper makes the following claim insufficient as novelty:

> "We use whole-body MPC to control a humanoid."

Whole-body MPC for humanoids has already been demonstrated.

Similarly:

> "We use MuJoCo/iLQR for humanoid control."

This is also established.

Therefore, our novelty should NOT be based on simply implementing MPC.

A potentially interesting distinction is:

    Existing:

    Hand-designed Cost
          ↓
    Whole-Body MPC
          ↓
    Humanoid Motion


    Our Target:

    Human Demonstrations
          ↓
    Learned Human Objective
          ↓
    Whole-Body MPC
          ↓
    H1 Motion

However:

**Whether this constitutes a genuine research gap is NOT ESTABLISHED YET.**

The remaining literature on learned costs, IOC/IRL, human-to-humanoid transfer, and humanoid MPC must be checked before making a novelty claim.

---

### 23. Implication for Our Project

This paper suggests that we do not need to invent a completely new MPC algorithm for the project.

If our research question is:

> Can a human-derived objective generate generalizable humanoid behavior?

then the MPC can potentially be a strong existing baseline.

The research contribution would primarily be in:

    Human Demonstrations
          ↓
    Objective Learning
          ↓
    Objective Transfer
          ↓
    MPC-based H1 Behavior

rather than:

    Inventing a new MPC solver

This helps keep the project small and focused.

---

### 24. Project Management Decision

**Status: Required**

Reason:

The paper directly supports the feasibility of the model-based control stage required by the project and demonstrates whole-body MPC on humanoid hardware, including Unitree H1.

It should therefore remain in the core MPC literature set.

However:

**No roadmap expansion is required.**

We do NOT need to add:

- a new MPC algorithm,
- a new simulator,
- a new humanoid platform,
- or a new control architecture

just because of this paper.

The existing plan remains:

    Isaac Lab + H1
          ↓
    Learned Objective
          ↓
    Model-Based MPC
          ↓
    H1 Control

---

### 25. Position in Our Literature Review

| Question | Zhang et al. (2025) |
|---|---|
| Model-based control? | Yes |
| MPC? | Yes |
| Whole-body control? | Yes |
| iLQR? | Yes |
| MuJoCo dynamics? | Yes |
| Contact dynamics? | Yes |
| Real-time control? | Yes |
| Real hardware? | Yes |
| Humanoid? | Yes |
| Unitree H1? | Yes |
| Human demonstrations? | No |
| Human objective learning? | No |
| IOC? | No |
| IRL? | No |
| Latent objective? | No |
| Human-to-robot transfer? | No |
| Learned cost? | No |
| Hand-designed cost? | Yes |
| Generalization of human objective? | No |
| MPC + learned human objective? | No |
| Generalization across embodiments? | No |

---

### 26. Role in Our Project

**Overall Role:**

**Core Model-Based Control / MPC paper.**

This paper demonstrates that:

    Whole-Body Dynamics
          +
    Predefined Objective
          +
    iLQR / MPC
          ↓
    Real-Time Humanoid Control

is feasible in practice.

For our project, it provides the downstream control foundation:

    Learned Objective
          ↓
    H1 Whole-Body MPC

rather than requiring us to develop a new MPC method.

---

### 27. Final Takeaway

The most important lesson for our project is:

> We do not necessarily need to invent a new MPC algorithm. Existing whole-body MPC methods are already capable of controlling full-sized humanoids in real time.

The unresolved question relevant to our project is instead:

    What happens if we replace

    Hand-Designed Robot Cost

    with

    Human-Derived Learned Objective?

Conceptually:

    Existing Work:

    Designed Cost
         ↓
        MPC
         ↓
       H1


    Our Target:

    Human Demonstrations
         ↓
    Learned Objective
         ↓
        MPC
         ↓
       H1
         ↓
    Generalization

That is the part that remains to be investigated.

**Status: Required**

**Research-gap status: Not established yet**

**Key contribution to our literature review:**

This paper establishes a strong practical baseline for whole-body model-based MPC of humanoids and demonstrates that real-time iLQR/MPC using a physics simulator can control full-sized humanoid hardware. It therefore supports the feasibility of the downstream control stage of our project, while leaving the human-objective inference and human-to-humanoid objective-transfer questions open.








## Paper 17 — Scianca et al. (2025)

**Citation**  
Scianca, N., Smaldone, F. M., Lanari, L., & Oriolo, G. (2025). *A Feasibility-Driven MPC Scheme for Robust Gait Generation in Humanoids*. Robotics and Autonomous Systems, 189, 104957. https://doi.org/10.1016/j.robot.2025.104957

**Literature Category**  
Model-Based Control / Model Predictive Control (MPC) / Humanoid Locomotion / Robust Control / Feasibility-Aware MPC

---

### 1. Research Problem

The paper investigates how a humanoid robot can maintain stable walking when it experiences disturbances such as:

- persistent disturbances,
- external pushes,
- impacts,
- or other perturbations.

The central question is:

> How can MPC determine in real time whether the current walking plan remains feasible, and what should the robot do when that plan is no longer feasible?

This is important because humanoid locomotion is not only an optimization problem.

The robot must also satisfy physical and stability constraints.

Conceptually:

    Good Objective
          +
    Feasible Motion
          +
    Stable Dynamics
          ↓
    Successful Humanoid Walking

---

### 2. Input

The controller receives information about:

- current robot state,
- planned footsteps,
- center of mass (CoM),
- Zero Moment Point (ZMP),
- disturbance estimates,
- stability constraints,
- feasibility conditions.

The system is evaluated using:

- HRP-4 simulation,
- NAO experiments,
- OP3 experiments.

Therefore:

- Humanoid locomotion: Yes
- MPC: Yes
- Robust locomotion: Yes
- Feasibility analysis: Yes
- Real robot experiments: Yes
- Human demonstrations: No
- Human objective learning: No
- IOC: No
- IRL: No
- H1: No

---

### 3. Method

The proposed method is called:

**Robust Intrinsically Stable Model Predictive Control (RIS-MPC).**

The controller has two operating modes:

    Standard Mode
          ↓
    Normal walking

and:

    Recovery Mode
          ↓
    Adapt walking plan
    when feasibility is lost

The controller continuously checks whether the current state and planned motion satisfy the required feasibility and stability conditions.

---

### 4. Simple Explanation

Imagine H1 is walking normally:

    Step 1 → Step 2 → Step 3 → Step 4

Now an external force pushes H1.

The original plan may no longer be safe:

    Step 1 → Step 2 → X → Step 4

Instead of blindly following the original plan, the controller checks:

    "Can I still execute the current plan?"

If yes:

    Continue normal MPC.

If no:

    Change the plan.

For example:

    Change foot position
          or
    Change footstep timing

and find a new feasible motion.

Conceptually:

    Current State
         ↓
    Is current plan feasible?
       /             \
     Yes              No
      ↓                ↓
 Normal MPC      Recovery MPC
      ↓                ↓
 Continue        Change steps/timing
 walking             ↓
                  Recover








## Paper 17 — Scianca et al. (2025)

**Citation**  
Scianca, N., Smaldone, F. M., Lanari, L., & Oriolo, G. (2025). *A Feasibility-Driven MPC Scheme for Robust Gait Generation in Humanoids*. Robotics and Autonomous Systems, 189, 104957. https://doi.org/10.1016/j.robot.2025.104957

**Literature Category**  
Model-Based Control / Model Predictive Control (MPC) / Humanoid Locomotion / Robust Control / Feasibility-Aware MPC

---

### 1. Research Problem

The paper investigates how a humanoid robot can maintain robust and stable walking when it experiences disturbances.

The main question is:

> How can MPC determine whether the current walking plan is still physically feasible, and what should the robot do when the current plan becomes infeasible?

This is important because humanoid locomotion is not simply an optimization problem.

A controller must find a motion that is:

- desirable,
- dynamically feasible,
- stable,
- and compatible with the robot's constraints.

Conceptually:

    Objective
        +
    Robot Dynamics
        +
    Constraints
        +
    Feasibility
        ↓
       MPC
        ↓
    Humanoid Motion

The paper focuses on the last part of this pipeline: robust model-based humanoid control.

---

### 2. Input

The controller uses information including:

- current robot state,
- planned footsteps,
- Center of Mass (CoM),
- Zero Moment Point (ZMP),
- estimated disturbances,
- stability constraints,
- feasibility conditions.

The method is evaluated in simulation and on physical humanoid robots.

The reported validation includes:

- HRP-4 simulation,
- NAO experiments,
- OP3 experiments.

Therefore:

- Humanoid locomotion: Yes
- MPC: Yes
- Robust locomotion: Yes
- Feasibility analysis: Yes
- Real robot experiments: Yes
- Human demonstrations: No
- Human objective learning: No
- IOC: No
- IRL: No
- Unitree H1: No

---

### 3. Method

The proposed framework is called:

**Robust Intrinsically Stable Model Predictive Control (RIS-MPC).**

The controller has two operating modes:

    Standard Mode
          ↓
    Normal walking

and:

    Recovery Mode
          ↓
    Recovery after strong disturbances

The important idea is that the controller chooses the mode based on whether the current state remains feasible.

In standard mode:

    Fixed footsteps
          ↓
    MPC
          ↓
    CoM + ZMP trajectories

If a strong disturbance makes the current plan infeasible:

    Feasibility lost
          ↓
    Recovery Mode
          ↓
    Modify footsteps
    and/or timing
          ↓
    Recover feasibility

The paper formulates both modes as optimization problems involving Quadratic Programs (QPs) and provides analysis of their feasibility. :contentReference[oaicite:0]{index=0}

---

### 4. Simple Explanation

Imagine that the humanoid is walking:

    Step 1 → Step 2 → Step 3 → Step 4

Now someone pushes the robot.

The original plan may no longer be safe:

    Step 1 → Step 2 → X → Step 4

A normal controller might try to continue following the original plan.

This paper instead asks:

> Can the robot still execute this plan?

If the answer is yes:

    Continue normal MPC.

If the answer is no:

    Change the walking plan.

For example:

    Change foot position
          or
    Change footstep timing

and search for a new feasible solution.

Conceptually:

    Current State
         ↓
    Is current plan feasible?
       /             \
     Yes              No
      ↓                ↓
 Standard MPC      Recovery MPC
      ↓                ↓
 Continue          Change steps
 walking           / timing
                       ↓
                  Recover walking

This is the central idea of the paper. :contentReference[oaicite:1]{index=1}

---

### 5. Why Is It Called "Feasibility-Driven"?

The important point is that MPC is not only asking:

> Which motion has a lower cost?

It is also asking:

> Is this motion still physically possible?

A motion can have a good cost but still be impossible for the humanoid to execute.

Therefore:

    Low Cost
       ≠
    Feasible Motion

The controller must satisfy both:

    Good Objective
          +
    Physical Feasibility

This distinction is highly relevant to our project.

---

### 6. Objective / Cost

The objective is predefined.

The paper does NOT learn the objective from human demonstrations.

The controller is designed to realize a predefined sequence of footsteps while maintaining stability and feasibility.

In standard mode, the MPC computes CoM and ZMP trajectories while respecting stability-related constraints.

Therefore:

- Objective learning: No
- IOC: No
- IRL: No
- Latent objective learning: No
- Human demonstration learning: No

The main contribution is not discovering what the robot should optimize.

The contribution is making the model-based controller robust when the original plan becomes infeasible.

---

### 7. Important Concept: Feasibility

For this project, "feasibility" can be understood simply as:

> Is there still a physically valid way for the robot to execute the desired motion while satisfying its constraints?

For a humanoid, this can involve:

- balance,
- ZMP constraints,
- CoM behavior,
- foot placement,
- footstep timing,
- contact conditions,
- dynamic limitations.

For example:

    Desired Motion
          ↓
    Is it dynamically possible?
          ↓
       Yes → Execute
       No  → Find another motion

This is exactly the type of issue that becomes important when a learned human objective is transferred to a robot with different dynamics.

---

### 8. Standard Mode

In standard mode:

- footsteps are treated as fixed,
- MPC computes CoM and ZMP trajectories,
- robust stability constraints are imposed,
- disturbance information is incorporated,
- the controller attempts to follow the predefined walking plan.

The purpose is to maintain stable walking while following the planned footsteps. :contentReference[oaicite:2]{index=2}

---

### 9. Recovery Mode

If a sufficiently strong disturbance violates the conditions required for the standard mode, the controller switches to recovery mode.

In recovery mode:

- footstep positions can be modified,
- footstep timings can be modified,
- a new feasible walking plan is searched for.

Conceptually:

    Disturbance
         ↓
    Current plan becomes infeasible
         ↓
    Recovery Mode
         ↓
    Change foot position/timing
         ↓
    Restore feasibility

This allows the robot to adapt the walking plan rather than blindly following an invalid trajectory. :contentReference[oaicite:3]{index=3}

---

### 10. Robustness

The paper considers different kinds of perturbations.

Two important examples are:

#### Persistent perturbation

A disturbance that remains for an extended period.

Example:

    Walking under a persistent external force
    or
    walking on an incline

#### Impulsive perturbation

A short and sudden disturbance.

Example:

    Someone pushes the robot.

The controller is designed to remain feasible and stable under such perturbations and to switch to recovery when the standard plan is no longer feasible. :contentReference[oaicite:4]{index=4}

---

### 11. MPC Formulation

The paper uses Model Predictive Control.

The basic MPC idea is:

    Current State
         ↓
    Predict future motion
         ↓
    Optimize over a horizon
         ↓
    Apply part of the solution
         ↓
    Observe new state
         ↓
    Optimize again

This allows the controller to continuously reconsider the walking motion as the robot state changes.

The important difference in this paper is that the controller also reasons about the feasibility region.

Therefore:

    State
      +
    Future prediction
      +
    Constraints
      +
    Feasibility
      ↓
    MPC decision

---

### 12. Stability and ZMP

A major part of the approach uses the relationship between:

- Center of Mass (CoM)
- Zero Moment Point (ZMP)

The controller computes trajectories that satisfy stability-related constraints.

A simple intuition is:

> The robot must keep its motion compatible with the area in which its contact with the ground can support it.

If a disturbance pushes the robot outside the conditions required for the current walking plan, the original plan may no longer be feasible.

This motivates the switch to recovery mode.

---

### 13. Validation

The method is validated through:

- simulations on HRP-4,
- experiments on NAO,
- experiments on OP3.

The experiments evaluate robust humanoid gait generation under perturbations.

The paper also provides theoretical analysis of feasibility and conditions for recursive feasibility of the standard mode. :contentReference[oaicite:5]{index=5}

---

### 14. Main Finding

The main finding is:

> A humanoid MPC controller can improve robustness by explicitly reasoning about the feasibility of the current walking plan and switching to a recovery strategy when the original plan becomes infeasible.

The important principle is:

    Optimize
       +
    Check feasibility
       +
    Adapt when necessary
       ↓
    Robust Humanoid Locomotion

rather than:

    Optimize once
       ↓
    Follow the original plan blindly

---

### 15. Important Limitation: No Human Objective

The paper does not investigate:

> What objective does a human optimize while walking?

The desired walking behavior is predefined.

Therefore, it does not address:

    Human Motion
         ↓
    Infer Human Objective

This remains outside the scope of the paper.

---

### 16. Important Limitation: No IOC / IRL

The method is not Inverse Optimal Control (IOC).

It is also not Inverse Reinforcement Learning (IRL).

There is no:

    Human Demonstration
          ↓
    Infer Cost / Reward

stage.

Instead, the structure is:

    Predefined Objective
          +
    Robot Model
          +
    Constraints
          ↓
         MPC
          ↓
    Humanoid Motion

---

### 17. Important Limitation: No Latent Objective

The paper does not learn a latent objective representation.

There is no:

    Human Demonstrations
          ↓
       Latent z
          ↓
       Cost(z)
          ↓
         MPC

Therefore, the central Phase 4 problem of our project remains unaddressed.

---

### 18. Important Limitation: No Human-to-Robot Transfer

The paper does not investigate whether a human-derived objective can be transferred to a humanoid robot.

There is no:

    Human
      ↓
    Human Objective
      ↓
    Humanoid

transfer experiment.

This is one of the important differences between this paper and our research direction.

---

### 19. Important Limitation: Different Robot Platforms

The paper evaluates the approach using HRP-4 simulation and physical experiments on NAO and OP3.

It does not evaluate Unitree H1. :contentReference[oaicite:6]{index=6}

Therefore:

    Feasibility-Aware MPC
          ↓
    Humanoid

is experimentally supported.

But:

    Feasibility-Aware MPC
          ↓
    Unitree H1

is not directly established by this paper.

This does not reduce its value for our literature review because the underlying control principle is relevant.

---

### 20. Relevance to Our Project

**Relevance: High**

This paper is highly relevant to the downstream model-based control stage.

Our intended architecture is:

    Human Demonstrations
            ↓
    Learned Human Objective
            ↓
    H1-Compatible Cost
            +
       H1 Dynamics
            +
       H1 Constraints
            +
       Feasibility
            ↓
           MPC
            ↓
        H1 Behavior

Scianca et al. strongly support the importance of:

    Robot Dynamics
          +
    Constraints
          +
    Feasibility
          ↓
         MPC

They do not address:

    Human Demonstrations
          ↓
    Learned Human Objective

Therefore, their work is complementary to our objective-learning problem.

---

### 21. Relation to Zhang et al. (2025)

Zhang et al. (2025) and Scianca et al. (2025) address complementary aspects of model-based humanoid control.

#### Zhang et al.

Main focus:

    Whole-Body Dynamics
          +
    iLQR / MPC
          ↓
    Real-Time Humanoid Control

Main lesson:

> Whole-body model-based MPC can be implemented effectively for legged and humanoid robots.

#### Scianca et al.

Main focus:

    MPC
      +
    Feasibility
      +
    Robustness
      ↓
    Recovery

Main lesson:

> Humanoid MPC should explicitly account for feasibility and should be able to modify the walking plan when disturbances make the original plan infeasible.

Together:

    Whole-Body MPC
          +
    Feasibility
          +
    Robustness
          ↓
    Practical Humanoid Control

---

### 22. Relation to Our Project

Our intended final architecture is:

    Human Demonstrations
            ↓
    Latent Human Objective
            ↓
    H1-Compatible Cost
            ↓
       H1 Dynamics
            +
       H1 Constraints
            +
        Feasibility
            ↓
           MPC
            ↓
        H1 Behavior

Scianca et al. mainly address:

    H1/Robot Dynamics
            +
       Constraints
            +
       Feasibility
            ↓
           MPC

They do not address:

    Human Demonstrations
            ↓
    Latent Human Objective

Therefore, this paper does not solve the central research problem of Phase 4.

It strengthens the justification for the downstream control architecture.

---

### 23. Research Gap Contribution

This paper makes the following novelty claims insufficient:

- "We use MPC for humanoid locomotion."
- "We use feasibility-aware MPC."
- "We make humanoid MPC robust to disturbances."
- "We adapt footsteps when the walking plan becomes infeasible."

These areas have already been investigated.

The authors' research group also has related prior work on feasibility-aware plan adaptation, joint-level whole-body MPC, and humanoid gait generation. :contentReference[oaicite:7]{index=7}

Therefore, we should NOT make feasibility-aware MPC itself the central novelty of our project.

A potentially interesting combination remains:

    Human Demonstrations
          ↓
    Learned Human Objective
          ↓
    Feasibility-Aware MPC
          ↓
    H1 Behavior

However:

**Whether this combination constitutes a genuine research gap is NOT ESTABLISHED YET.**

This must be checked against the remaining literature before making a novelty claim.

---

### 24. Implication for Our Project

This paper gives us an important design principle:

> A learned objective cannot simply be optimized without considering whether the resulting motion is physically feasible for H1.

Suppose the learned human objective prefers:

    Fast walking
    +
    Low effort
    +
    Smooth motion

The resulting optimum for a human may not be physically possible for H1.

Therefore:

    Learned Human Objective
             ↓
        H1 Dynamics
             +
        H1 Constraints
             +
         Feasibility
             ↓
            MPC
             ↓
       Feasible H1 Motion

This is exactly the type of model-based transfer that the project is trying to investigate.

---

### 25. Project Management Decision

**Status: Required**

Reason:

The paper is directly relevant to the model-based control stage and demonstrates that feasibility should be treated as a fundamental part of robust humanoid MPC.

However:

**No roadmap expansion is required.**

We do NOT need to create a new research branch for:

- feasibility-aware MPC,
- recovery MPC,
- new footstep adaptation,
- or a new humanoid MPC algorithm.

These are established research directions.

Our project should remain focused on:

    Learning the human objective
          ↓
    Applying it through model-based control

---

### 26. Position in Our Literature Review

| Question | Scianca et al. (2025) |
|---|---|
| Model-based control? | Yes |
| MPC? | Yes |
| Humanoid locomotion? | Yes |
| Robust locomotion? | Yes |
| Feasibility-aware control? | Yes |
| Stability constraints? | Yes |
| Disturbance handling? | Yes |
| Recovery behavior? | Yes |
| Footstep adaptation? | Yes |
| Real robot experiments? | Yes |
| Human demonstrations? | No |
| Human objective learning? | No |
| IOC? | No |
| IRL? | No |
| Latent objective? | No |
| Learned cost? | No |
| Human-to-robot transfer? | No |
| Unitree H1? | No |
| MPC + human objective? | No |
| Generalization of human objective? | No |

---

### 27. Role in Our Project

**Overall Role:**

**Core Model-Based Control / MPC paper.**

The paper establishes that practical humanoid MPC should consider not only the optimization objective but also:

- feasibility,
- stability,
- disturbances,
- and recovery.

It therefore strengthens the model-based-control foundation of our project.

---

### 28. Final Takeaway

The most important lesson for our project is:

> A good objective alone is not enough. The controller must find a motion that is both desirable and physically feasible.

Conceptually:

    Learned Human Objective
             +
        H1 Dynamics
             +
        H1 Constraints
             +
         Feasibility
             ↓
            MPC
             ↓
        H1 Behavior

The paper does not solve:

    Human Motion
          ↓
    Human Objective

but it strengthens:

    Objective
        +
    Robot Physics
        +
    Constraints
        +
    Feasibility
        ↓
       MPC

Therefore:

**Status: Required**

**Research-gap status: Not established yet**

**Key contribution to our literature review:**

This paper demonstrates that feasibility and robustness are fundamental components of practical humanoid MPC. It supports the idea that a learned human objective should ultimately be optimized subject to the physical dynamics, stability constraints, and feasibility of the H1 rather than being directly imposed as a human trajectory.






## Paper 18 — Molnar et al. (2025/2026)

**Citation**  
Molnar, L., Cheng, J., Fadini, G., Kang, D., Zargarbashi, F., & Coros, S. (2025). *Whole-Body Inverse Dynamics MPC for Legged Loco-Manipulation*. arXiv:2511.19709. Subsequently published in IEEE Robotics and Automation Letters, 11(1), 898–905, 2026. DOI: 10.1109/LRA.2025.3636005.

**Literature Category**  
Model-Based Control / Model Predictive Control (MPC) / Whole-Body Control / Inverse Dynamics / Torque-Level MPC / Legged Loco-Manipulation

---

### 1. Research Problem

The paper investigates how a legged robot equipped with a manipulator can perform locomotion and manipulation simultaneously while maintaining physical consistency and stability.

The central problem is:

> How can locomotion, whole-body motion, and manipulation forces be optimized together inside a single model-based controller?

This is difficult because the motion of one part of the robot affects the rest of the body.

For example:

    Arm pushes object
          ↓
    Reaction force changes body motion
          ↓
    Body motion affects balance
          ↓
    Legs must compensate
          ↓
    Whole body must coordinate

The paper therefore proposes a whole-body MPC framework that directly reasons about the robot's full-body dynamics and control inputs.

---

### 2. Input

The controller uses:

- robot state,
- robot dynamics,
- desired base velocity,
- desired end-effector velocity,
- desired end-effector force,
- contact schedule,
- gait information,
- actuator constraints,
- whole-body dynamics.

The implementation uses:

- Pinocchio,
- CasADi,
- Fatrop.

The method is evaluated on a Unitree B2 quadruped equipped with a Unitree Z1 manipulator arm.

The hardware experiments achieve real-time MPC at approximately 80 Hz.

Demonstrated tasks include:

- pulling a 10 kg load,
- pushing a box,
- wiping a whiteboard,
- whole-body loco-manipulation.

---

### 3. Method

The paper proposes a **Whole-Body Inverse Dynamics Model Predictive Control** framework.

Instead of controlling locomotion and manipulation through completely separate controllers, the optimization considers the whole robot simultaneously.

Conceptually:

    Whole Robot
         ↓
    Full-Order Dynamics
         ↓
    MPC
         ↓
    Joint Torques
         ↓
    Whole-Body Motion

The MPC directly optimizes joint torques using the robot's full-order inverse dynamics.

This allows motion and force generation to be handled together inside one predictive optimization layer.

---

### 4. Simple Explanation

Imagine a robot wants to pull a heavy object.

A naive controller might think:

    "Move the arm."

But if the arm pulls strongly:

    Arm pulls object
          ↓
    Object pulls robot
          ↓
    Robot body moves
          ↓
    Robot may lose balance
          ↓
    Legs must react

Therefore, the controller cannot think about the arm alone.

It needs to think about:

    Arm
     +
    Body
     +
    Legs
     +
    Contacts
     +
    Forces

at the same time.

The paper does this using whole-body MPC.

---

### 5. What Is Inverse Dynamics Here?

Here, "inverse dynamics" has a different meaning from **Inverse Optimal Control (IOC)**.

This distinction is extremely important.

#### Inverse Dynamics

Given:

    Desired motion
        +
    Robot dynamics

find:

    Required forces / torques

Conceptually:

    Motion
      +
    Dynamics
      ↓
    Torques

#### Inverse Optimal Control

Given:

    Observed motion

infer:

    Objective / Cost

Conceptually:

    Motion
      ↓
    Objective

Therefore:

**Inverse Dynamics ≠ Inverse Optimal Control**

The word "inverse" is used in two completely different contexts.

---

### 6. Objective / Cost

The objective is predefined.

The paper does not infer a human objective.

The optimization contains task-related tracking terms and regularization/control terms with tunable weights.

Examples include objectives related to:

- base velocity tracking,
- end-effector velocity,
- end-effector force,
- control effort,
- motion behavior,
- gait-related objectives.

Therefore:

- Human objective learning: No
- IOC: No
- IRL: No
- Latent objective learning: No
- Learned reward: No

The objective is specified by the designer.

---

### 7. Key Idea: Direct Torque Optimization

A major feature of the method is that the MPC directly optimizes joint torques through full-order inverse dynamics.

Conceptually:

    Desired behavior
          ↓
        MPC
          ↓
    Joint torques
          ↓
    Robot dynamics
          ↓
    Whole-body motion

This differs from architectures where a high-level MPC produces a trajectory and a separate low-level controller is responsible for converting that trajectory into torques.

The paper aims to unify motion and force planning and execution within a single predictive layer.

---

### 8. Why Whole-Body Dynamics Matter

A robot's joints and body are physically coupled.

For example:

    Move arm
       ↓
    Change momentum
       ↓
    Change body balance
       ↓
    Change ground reaction forces
       ↓
    Change leg behavior

A whole-body dynamics model captures these interactions.

This is especially useful for tasks where locomotion and manipulation happen simultaneously.

---

### 9. Validation

The method is evaluated both in simulation and on physical hardware.

The physical platform is:

    Unitree B2
        +
    Unitree Z1 arm

The MPC runs at approximately 80 Hz on hardware.

The experiments include physically interactive tasks such as:

- pulling a 10 kg load while maintaining locomotion,
- pushing a box,
- wiping a whiteboard,
- interacting with the environment.

These experiments demonstrate that the proposed whole-body MPC can generate physically consistent behavior in real time.

---

### 10. Main Finding

The main finding is:

> Whole-body inverse-dynamics MPC can directly coordinate locomotion, manipulation, forces, and joint torques while respecting the robot's physical dynamics and constraints.

The paper demonstrates that a single predictive control layer can generate complex whole-body behaviors on real hardware.

---

### 11. Important Limitation: No Human Demonstrations

The paper does not use human motion demonstrations to infer the objective.

There is no:

    Human Motion
         ↓
    Human Objective

stage.

Therefore, it does not address the central Phase 4 problem of our project.

---

### 12. Important Limitation: No IOC

The word "Inverse Dynamics" in the title should not be confused with Inverse Optimal Control.

The paper does NOT perform:

    Observed Motion
          ↓
    Infer Cost

Instead, it performs:

    Robot Model
        +
    Desired Tasks
        ↓
       MPC
        ↓
    Robot Torques

Therefore, it belongs to the **Model-Based Control / MPC** section of our literature review, not the IOC section.

---

### 13. Important Limitation: No Latent Objective

The paper does not learn a latent objective representation.

There is no:

    Human Demonstrations
          ↓
       Latent z
          ↓
       Cost(z)
          ↓
         MPC

The cost terms are designed by the researchers.

Therefore, the objective-learning part of our project remains open.

---

### 14. Important Limitation: No Human-to-Humanoid Objective Transfer

The paper does not investigate:

    Human
      ↓
    Human Objective
      ↓
    Different Robot
      ↓
    Robot Behavior

The robot behavior is generated from predefined task objectives.

Therefore, it does not establish generalization of human objectives across different embodiments.

---

### 15. Important Limitation: Robot Platform

The physical platform is a Unitree B2 quadruped equipped with a Z1 manipulator arm.

It is not the Unitree H1 humanoid.

Therefore:

    Whole-Body Inverse-Dynamics MPC
            ↓
    Unitree B2 + Z1

is experimentally demonstrated.

But:

    Whole-Body Inverse-Dynamics MPC
            ↓
    Unitree H1

is not directly demonstrated by this paper.

Nevertheless, the formulation is relevant to H1 because it is based on general robot dynamics and whole-body optimization rather than a morphology-specific human imitation method.

---

### 16. Relevance to Our Project

**Relevance: High**

The paper is highly relevant to the downstream model-based control stage.

Our intended architecture is:

    Human Demonstrations
            ↓
    Latent Human Objective
            ↓
    H1-Compatible Cost
            +
       H1 Dynamics
            +
       H1 Constraints
            ↓
    Whole-Body MPC
            ↓
       H1 Behavior

Molnar et al. strongly support the idea that the objective can be combined with full-body robot dynamics and constraints inside a model-based predictive controller.

However, they do not address the first step:

    Human Demonstrations
            ↓
    Latent Human Objective

---

### 17. Relation to Zhang et al. (2025)

Zhang et al. and Molnar et al. are related but focus on different aspects of model-based control.

#### Zhang et al.

Focus:

    Whole-Body MPC
          +
    iLQR
          ↓
    Real-Time Legged/Humanoid Control

Main lesson:

> Whole-body model-based MPC can be implemented effectively in real time.

#### Molnar et al.

Focus:

    Full-Order Dynamics
          +
    Inverse Dynamics
          +
    Torque-Level MPC
          ↓
    Whole-Body Loco-Manipulation

Main lesson:

> Motion and force generation can be unified in a whole-body torque-level MPC.

Together, they show that model-based MPC can operate at increasingly detailed levels of the robot dynamics.

---

### 18. Relation to Scianca et al. (2025)

Scianca et al. emphasize:

    MPC
      +
    Feasibility
      +
    Stability
      +
    Recovery

Molnar et al. emphasize:

    MPC
      +
    Full-Order Dynamics
      +
    Torque Optimization
      +
    Whole-Body Coordination

Together:

    Learned / Designed Objective
             +
       Full-Body Dynamics
             +
          Constraints
             +
         Feasibility
             ↓
            MPC
             ↓
       Whole-Body Behavior

This combination is conceptually close to the final control stage of our project.

---

### 19. Relation to Our Project

The main conceptual connection is:

    Human Objective
          ↓
    H1-Compatible Cost
          ↓
    Whole-Body MPC
          ↓
    H1 Dynamics
          +
    H1 Constraints
          ↓
    H1 Motion

Molnar et al. demonstrate the bottom part:

    Cost
      +
    Whole-Body Dynamics
      +
    Constraints
      ↓
    MPC
      ↓
    Robot Motion

Our research question adds:

    Human Demonstrations
          ↓
    Learned Objective

before the MPC stage.

---

### 20. Important Research Insight

This paper reinforces an important principle for our project:

> The learned human objective does not need to specify the exact robot trajectory.

Instead, the objective can specify what behavior is desirable.

Then:

    Learned Objective
          ↓
    H1 Dynamics
          +
    H1 Constraints
          ↓
    MPC
          ↓
    H1-specific motion

This is one of the strongest reasons to investigate objective learning instead of direct trajectory imitation.

---

### 21. Research Gap Contribution

This paper makes the following novelty claims insufficient:

- "We use whole-body MPC."
- "We use inverse-dynamics MPC."
- "We optimize joint torques with MPC."
- "We combine locomotion and manipulation in MPC."
- "We enforce robot dynamics and constraints in MPC."

These capabilities are already demonstrated.

Therefore, our project should NOT claim novelty from simply implementing whole-body inverse-dynamics MPC.

A potentially interesting research direction remains:

    Human Demonstrations
          ↓
    Learned Human Objective
          ↓
    Whole-Body Model-Based MPC
          ↓
    Different Robot Dynamics
          ↓
    Generalizable Behavior

However:

**Whether this constitutes a genuine research gap is NOT ESTABLISHED YET.**

The remaining literature on objective learning and human-to-robot transfer must be considered before making a final novelty claim.

---

### 22. Project Management Decision

**Status: Useful**

Reason:

The paper provides a strong modern example of whole-body model-based MPC with full-order dynamics, torque-level optimization, physical constraints, and real-time hardware execution.

However, it is not directly about human objective learning.

Therefore, it should support our understanding of the downstream controller but should not cause the project scope to expand.

We do NOT need to:

- build a new inverse-dynamics MPC from scratch,
- switch to a quadruped platform,
- add loco-manipulation to the project,
- or make manipulation part of the research question.

Our project remains focused on humanoid locomotion and learned human objectives.

---

### 23. Position in Our Literature Review

| Question | Molnar et al. (2025/2026) |
|---|---|
| Model-based control? | Yes |
| MPC? | Yes |
| Whole-body control? | Yes |
| Full-order dynamics? | Yes |
| Inverse dynamics? | Yes |
| Torque-level optimization? | Yes |
| Physical constraints? | Yes |
| Real-time hardware? | Yes |
| Loco-manipulation? | Yes |
| Unitree robot? | Yes |
| Unitree H1? | No |
| Human demonstrations? | No |
| Human objective learning? | No |
| IOC? | No |
| IRL? | No |
| Latent objective? | No |
| Learned cost? | No |
| Human-to-robot transfer? | No |
| Generalization across embodiments? | No |
| MPC + human objective? | No |

---

### 24. Role in Our Project

**Overall Role:**

**Modern Whole-Body Model-Based MPC reference.**

The paper demonstrates that a robot's full-order dynamics, physical constraints, joint torques, and task objectives can be integrated into a single predictive control framework.

For our project, it provides evidence for the downstream architecture:

    Learned Objective
          +
    Robot Dynamics
          +
    Robot Constraints
          ↓
    Whole-Body MPC
          ↓
    Robot Behavior

It does not address how the objective should be learned from human demonstrations.

---

### 25. Final Takeaway

The most important lesson for our project is:

> The objective tells the robot what behavior is desirable, while the robot's own dynamics and constraints determine how that behavior can physically be achieved.

This gives us the conceptual architecture:

    Human Demonstrations
            ↓
    Learn Human Objective
            ↓
    H1-Compatible Objective
            ↓
    H1 Dynamics
            +
    H1 Constraints
            ↓
    Whole-Body MPC
            ↓
       H1 Behavior

Molnar et al. strongly support the bottom half of this architecture.

The unresolved research problem remains the top half:

    Human Motion
          ↓
    Latent Human Objective
          ↓
    Transfer to H1

**Status: Useful**

**Research-gap status: Not established yet**

**Key contribution to our literature review:**

This paper provides a strong modern example of whole-body inverse-dynamics MPC that directly optimizes joint torques using full-order robot dynamics and physical constraints. It demonstrates real-time whole-body control on a Unitree B2 + Z1 platform, but does not learn objectives from human demonstrations or study human-to-humanoid objective transfer.








## Paper 19 — Zhu, Ahn & Hong (2025)

**Citation**  
Zhu, T., Ahn, M. S., & Hong, D. W. (2025). *ARTEMIS: An Open-Source, Full-Sized Humanoid Robot for Dynamic Locomotion*. Proceedings of the 2025 IEEE-RAS 24th International Conference on Humanoid Robots (Humanoids), 269–276. DOI: 10.1109/HUMANOIDS65713.2025.11203020.

**Literature Category**  
RoMeLa / Dennis Hong / Humanoid Robotics / Model-Based Locomotion / Dynamic Humanoid Control

---

### 1. Research Problem

The paper presents ARTEMIS, a full-sized humanoid robot designed for dynamic locomotion.

The main problem is:

> How can a full-sized humanoid robot be designed and controlled to achieve fast, dynamic, and robust locomotion in the real world?

The paper focuses on the robot platform, its actuation system, and the model-based locomotion controller used to demonstrate dynamic walking and running.

The paper is therefore primarily a **humanoid robotics and model-based control** contribution rather than an objective-learning paper.

---

### 2. Input

The system uses:

- the robot's state,
- robot dynamics,
- actuator measurements,
- contact information,
- locomotion commands,
- robot model,
- model-based control information.

The robot has:

- 20 active degrees of freedom,
- custom proprioceptive actuators,
- full-sized humanoid morphology.

The system is evaluated in real-world environments, including outdoor terrain.

The paper reports walking speeds of up to approximately 2.1 m/s and demonstrates transitions between walking and running.

Therefore:

- Full-sized humanoid: Yes
- Dynamic locomotion: Yes
- Walking: Yes
- Running: Yes
- Model-based control: Yes
- Real robot: Yes
- Outdoor validation: Yes
- Human demonstrations: No
- IOC: No
- IRL: No
- Human objective learning: No
- Latent objective: No
- Human-to-robot transfer: No
- Unitree H1: No

---

### 3. Method

The paper combines:

1. A custom full-sized humanoid hardware platform.
2. Custom proprioceptive actuators.
3. A robot dynamics model.
4. A model-based locomotion controller.
5. Real-world experimental validation.

The overall idea is:

    Robot Hardware
          +
    Robot Dynamics
          +
    Model-Based Controller
          ↓
    Dynamic Humanoid Locomotion

The paper also releases the robot model and baseline controllers as open-source resources.

---

### 4. Simple Explanation

Imagine we want to make a humanoid robot run.

There are two separate questions:

**Question 1:**

> Can we build a robot that is physically capable of doing it?

**Question 2:**

> Can we control that robot so that it actually walks and runs?

ARTEMIS addresses both.

It develops a full-sized humanoid and then demonstrates that the robot can perform dynamic locomotion using model-based control.

The important point for our project is:

> A humanoid does not need to copy human joint trajectories exactly in order to perform dynamic locomotion.

Instead, the controller can use the robot's own dynamics and constraints to generate an appropriate motion.

---

### 5. Objective / Cost

The paper does not attempt to discover a human objective.

There is no:

    Human Demonstration
          ↓
    Infer Human Objective

stage.

The locomotion controller uses predefined control objectives and model-based information.

Therefore:

- Objective learning: No
- IOC: No
- IRL: No
- Latent objective learning: No
- Human reward learning: No

This distinction is important for our project.

ARTEMIS demonstrates the **control side** of our proposed architecture, not the **objective-learning side**.

---

### 6. Model-Based Control

The controller uses the robot's model to generate locomotion behavior.

The basic concept is:

    Desired Locomotion
          +
    Robot Dynamics
          +
    Robot State
          ↓
    Model-Based Controller
          ↓
    Robot Motion

The important idea is that the controller does not simply replay a human trajectory.

It generates motion that is compatible with the physical robot.

This is closely related to the motivation behind our project.

---

### 7. Validation

ARTEMIS is validated on a physical full-sized humanoid robot.

The paper reports:

- walking up to approximately 2.1 m/s,
- transition between walking and running,
- locomotion on different outdoor terrains,
- robustness experiments,
- successful performance in RoboCup-related competition.

The paper therefore provides real-world evidence that the platform and model-based controller can support dynamic humanoid locomotion.

---

### 8. Main Finding

The main finding is:

> A full-sized humanoid robot with custom proprioceptive actuation and model-based control can achieve fast and dynamic locomotion, including walking and running, on real hardware.

The paper demonstrates that dynamic humanoid locomotion is achievable through the combination of:

    Appropriate Hardware
          +
    Robot Dynamics
          +
    Model-Based Control
          ↓
    Dynamic Locomotion

---

### 9. Important Limitation: No Human Objective Learning

The paper does not ask:

> What objective does a human optimize when walking or running?

It therefore does not contribute directly to:

    Human Motion
          ↓
    Human Objective

This remains part of our Phase 4 research problem.

---

### 10. Important Limitation: No IOC / IRL

The paper does not perform:

- Inverse Optimal Control,
- Inverse Reinforcement Learning,
- reward inference,
- cost inference from demonstrations.

Therefore:

    Observed Human Motion
            ↓
    Learned Objective

is not part of ARTEMIS.

---

### 11. Important Limitation: No Human-to-Robot Transfer

The paper does not investigate:

    Human
      ↓
    Human Objective
      ↓
    Humanoid Robot
      ↓
    Robot-Specific Motion

Instead, the locomotion behavior is generated using the robot's own model and controller.

Therefore, it does not establish whether a human objective can transfer across different embodiments.

---

### 12. Important Limitation: No Latent Objective

The paper does not learn a latent representation of human behavior.

There is no:

    Human Demonstrations
          ↓
       Latent z
          ↓
      Objective
          ↓
         MPC

Therefore, the main research problem of our Phase 4 remains unaddressed.

---

### 13. Important Limitation: ARTEMIS ≠ H1

ARTEMIS is a custom humanoid developed by UCLA RoMeLa.

Our target robot is Unitree H1.

Therefore:

    ARTEMIS Dynamics
          ≠
    H1 Dynamics

and:

    ARTEMIS Constraints
          ≠
    H1 Constraints

This distinction is important.

Our project should not assume that a controller or objective that works on ARTEMIS will automatically work on H1.

Instead, one of the motivations for learning an objective at a higher level is precisely to allow the robot's own dynamics and constraints to determine how the behavior is realized.

---

### 14. Relevance to Our Project

**Relevance: High**

The paper is highly relevant to the downstream part of our project:

    Learned Objective
          +
    Robot Dynamics
          +
    Robot Constraints
          ↓
    Model-Based Control
          ↓
    Humanoid Motion

ARTEMIS demonstrates the importance and feasibility of the following part:

    Robot Dynamics
          +
    Model-Based Control
          ↓
    Real Humanoid Locomotion

However, it does not address:

    Human Demonstrations
          ↓
    Learned Human Objective

Therefore, ARTEMIS should be viewed as a **RoMeLa/model-based humanoid control reference**, not as an objective-learning paper.

---

### 15. Relation to Professor Dennis Hong's Response

This paper is particularly relevant because Dennis Hong is one of the authors and the work comes directly from UCLA RoMeLa.

Hong's response to our project suggested:

    Human Demonstrations
          ↓
    Learn Underlying Objectives
          ↓
    Model-Based MPC
          ↓
    Respect Robot Dynamics
    and Physical Constraints

ARTEMIS provides strong evidence that the RoMeLa side of this proposed architecture is technically meaningful:

    Humanoid
       +
    Robot Dynamics
       +
    Model-Based Control
       ↓
    Dynamic Locomotion

Our project adds a different research question before this stage:

    Human Demonstrations
          ↓
    Learn Human Objective
          ↓
    Robot-Specific Model-Based Control

Therefore, ARTEMIS is highly relevant for understanding the **target control framework** suggested by Hong.

---

### 16. Why This Matters for Our Research Question

Suppose a human walks like this:

    Human Joint Trajectory
          ↓
    Motion A

If we directly imitate the trajectory on H1, we may encounter problems because:

    Human Dynamics
          ≠
    H1 Dynamics

Instead, our proposed approach is:

    Human Demonstrations
          ↓
    Infer Objective
          ↓
    H1 Dynamics
          +
    H1 Constraints
          ↓
    Model-Based Control
          ↓
    H1-Specific Motion

ARTEMIS supports the idea that the last step can be handled through model-based humanoid control.

The unresolved question is whether the first step can be learned in a sufficiently generalizable way.

---

### 17. Research Gap Contribution

ARTEMIS makes the following novelty claims insufficient:

- "We use model-based control for humanoid locomotion."
- "We control a full-sized humanoid using its dynamics."
- "We generate dynamic walking on a humanoid."
- "We demonstrate walking and running on a real humanoid."
- "We use robot-specific dynamics and constraints for locomotion."

These are already demonstrated by RoMeLa and other humanoid research.

Therefore, our project should not claim novelty from model-based humanoid locomotion alone.

A potentially interesting distinction remains:

    Human Demonstrations
          ↓
    Human Objective
          ↓
    Transfer Across Embodiments
          ↓
    Model-Based Control
          ↓
    Robot-Specific Motion

However:

**Whether this constitutes a genuine research gap is NOT ESTABLISHED YET.**

This must be determined from the complete IOC, IRL, human locomotion, MPC, and RoMeLa literature.

---

### 18. Important Conceptual Lesson

ARTEMIS supports an important principle for our project:

> A humanoid robot should be allowed to use its own dynamics to determine how a desired behavior is physically realized.

For example, suppose the desired behavior is:

    Walk forward
    + 
    Maintain balance
    +
    Move efficiently

We should not necessarily specify:

    "Move the left knee exactly like the human."

Instead:

    Desired Objective
          ↓
    H1 Dynamics
          +
    H1 Constraints
          ↓
    Model-Based Controller
          ↓
    H1 Motion

This is one of the motivations for studying objective-level learning rather than direct trajectory imitation.

---

### 19. Relation to Other MPC Papers

ARTEMIS complements the other model-based-control papers in our literature review.

#### Zhang et al. (2025)

Focus:

    Whole-Body MPC
          +
    iLQR
          ↓
    Legged / Humanoid Control

Main lesson:

> Whole-body model-based MPC can generate robot motion in real time.

#### Scianca et al. (2025)

Focus:

    MPC
      +
    Feasibility
      +
    Recovery
      ↓
    Robust Humanoid Locomotion

Main lesson:

> Feasibility and recovery are important for robust humanoid locomotion.

#### Molnar et al. (2025/2026)

Focus:

    Full-Order Dynamics
          +
    Inverse Dynamics
          +
    Torque-Level MPC
          ↓
    Whole-Body Loco-Manipulation

Main lesson:

> Whole-body dynamics and torques can be optimized directly inside MPC.

#### Zhu, Ahn & Hong (2025)

Focus:

    Full-Sized Humanoid
          +
    Custom Actuation
          +
    Model-Based Control
          ↓
    Dynamic Walking / Running

Main lesson:

> Model-based dynamic locomotion can be realized on a real full-sized humanoid developed in an academic lab.

Together, these papers establish a strong model-based control foundation.

---

### 20. What This Paper Does NOT Establish

The following statements cannot be concluded from ARTEMIS:

1. Humans optimize a particular locomotion objective.
2. Human locomotion objectives can be inferred from demonstrations.
3. Human objectives are transferable across robot morphologies.
4. A latent objective is more generalizable than trajectory imitation.
5. A learned human objective can control H1.
6. A learned human objective can generalize across humanoid embodiments.
7. Objective learning combined with MPC is superior to trajectory imitation.

All of these remain research questions for our project.

---

### 21. Project Management Decision

**Status: Required**

**Reason:**

The paper is directly relevant to the final part of the architecture proposed by Professor Hong:

    Robot Dynamics
          +
    Model-Based Control
          +
    Humanoid Constraints
          ↓
    Dynamic Humanoid Locomotion

It is also directly connected to RoMeLa and Dennis Hong.

However, it does NOT require any expansion of our research roadmap.

We do NOT need to:

- reproduce ARTEMIS,
- build ARTEMIS,
- use ARTEMIS as our robot,
- add running to the research question,
- or implement the entire ARTEMIS controller.

Our target remains:

    Unitree H1
          ↓
    Learned Human Objective
          ↓
    Model-Based MPC

---

### 22. Position in Our Literature Review

| Question | ARTEMIS |
|---|---|
| Full-sized humanoid? | Yes |
| Humanoid locomotion? | Yes |
| Dynamic walking? | Yes |
| Running? | Yes |
| Model-based control? | Yes |
| Real hardware? | Yes |
| Outdoor validation? | Yes |
| RoMeLa? | Yes |
| Dennis Hong? | Yes |
| Human demonstrations? | No |
| Human locomotion objective? | No |
| IOC? | No |
| IRL? | No |
| Latent objective learning? | No |
| Learned cost? | No |
| Human-to-robot transfer? | No |
| Cross-embodiment generalization? | No |
| Unitree H1? | No |
| Human objective + MPC? | No |

---

### 23. Role in Our Project

**Overall Role:**

**Core RoMeLa / Dennis Hong / Model-Based Humanoid Locomotion reference.**

The paper establishes that RoMeLa has demonstrated a full-sized humanoid capable of dynamic locomotion using model-based control and real-world validation.

It therefore provides important context for the model-based control direction suggested by Professor Hong.

However, it does not address the central objective-learning problem of our project.

---

### 24. Final Takeaway

The most important lesson for our project is:

> ARTEMIS shows that a full-sized humanoid can use its own dynamics and model-based controller to generate dynamic locomotion instead of simply replaying human trajectories.

For our project, this motivates the following architecture:

    Human Demonstrations
            ↓
    Learn Human Objective
            ↓
    H1 Dynamics
            +
    H1 Constraints
            ↓
    Model-Based MPC
            ↓
       H1-Specific Motion

ARTEMIS strongly supports the **model-based humanoid control** part of this architecture.

It does not solve the **human objective learning** part.

Therefore:

**Status: Required**

**Research-gap status: Not established yet**

**Key contribution to our literature review:**

ARTEMIS demonstrates a real full-sized humanoid platform from RoMeLa using model-based control for dynamic walking and running. It establishes strong prior art for real-world model-based humanoid locomotion and therefore prevents us from claiming that model-based humanoid control itself is novel. The potentially novel part of our project must instead be investigated around learning and transferring human objectives.
