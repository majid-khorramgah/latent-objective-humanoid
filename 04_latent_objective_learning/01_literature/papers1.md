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
