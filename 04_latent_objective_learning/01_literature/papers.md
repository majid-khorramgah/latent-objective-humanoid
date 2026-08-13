## Paper 1 — Todorov & Jordan (2002)

### Citation

Todorov, E., & Jordan, M. I. (2002).

Optimal feedback control as a theory of motor coordination.

Nature Neuroscience, 5, 1226–1235.

DOI: 10.1038/nn963

### Research Problem

The paper addresses how humans coordinate many biomechanical degrees of freedom to achieve task goals despite uncertainty and variability in movement.

### Input

The framework considers a dynamical system, task objectives, control constraints, and uncertainty/noise.

The paper also considers experimental motor behavior to evaluate predictions of the optimal feedback control framework.

### Method

The authors formulate human motor coordination as stochastic optimal feedback control.

Instead of planning and reproducing a fixed trajectory, the controller continuously uses feedback to select actions that optimize task performance under uncertainty.

### Objective / Cost

The performance criterion is assumed rather than inferred from demonstrations.

The framework allows the cost to represent task performance and control-related penalties.

### Main Finding

Optimal feedback control can explain how humans achieve reliable task outcomes while allowing variability in task-irrelevant dimensions.

The theory shows that variability does not necessarily represent motor error. An optimal controller can allow variability where it has little effect on task success while correcting deviations that affect important task variables.

### Limitation

The paper does not solve the inverse problem of recovering the unknown human objective or cost function from observed human motion.

The performance criterion is part of the model rather than something learned from demonstrations.

### Relevance to Our Project

This paper provides an important theoretical foundation for our research.

It supports the idea that human motion should not be treated only as a trajectory to imitate. Instead, observed motion can be interpreted as the result of an underlying optimization process involving task goals, dynamics, uncertainty, and a performance criterion.

This motivates the inverse problem studied in our project:

Human Motion Demonstrations
→ Infer Underlying Objective / Cost
→ Use the Learned Objective for Model-Based Control

### Research Gap Contribution

The paper establishes the forward relationship:

Objective / Cost
→ Optimal Feedback Control
→ Human Motion

Our research investigates the complementary inverse direction:

Human Motion
→ Objective / Cost Inference

Therefore, this work provides the theoretical motivation for investigating Inverse Optimal Control in the next stage of the literature review.



## Paper 2 — Mombaur, Truong & Laumond (2010)

### Citation

Mombaur, K., Truong, A., & Laumond, J.-P. (2010).

From Human to Humanoid Locomotion—An Inverse Optimal Control Approach.

Autonomous Robots, 28, 369–383.

DOI: 10.1007/s10514-009-9170-7

### Research Problem

The paper addresses how human locomotion behavior can be transferred to humanoid robots without directly reproducing the observed human trajectories.

The authors investigate whether an underlying locomotion objective can be inferred from human motion and subsequently used to generate new motions for a humanoid robot.

### Input

The framework uses human motion-capture demonstrations of locomotion toward different target configurations.

The motion representation focuses on the global position and orientation of the human body rather than full-body joint trajectories.

### Method

The authors formulate the problem as Inverse Optimal Control.

The human locomotion cost is represented as a weighted combination of manually selected cost functions. The weights of these cost functions are inferred by repeatedly solving a forward optimal control problem and comparing the resulting trajectories with the observed human demonstrations.

The inferred objective is then used to generate new locomotion trajectories for different target configurations.

### Objective / Cost

The objective is represented using several manually selected components, including:

* locomotion time,
* forward acceleration,
* rotational acceleration,
* orthogonal acceleration,
* body orientation alignment with the direction toward the target.

The objective representation is defined in advance. The IOC procedure learns the relative importance of these components rather than discovering the objective representation itself.

### Main Finding

A shared locomotion objective can explain multiple human locomotion demonstrations and can be used to generate new trajectories for previously unseen target configurations.

The work demonstrates that human locomotion can be modeled through an underlying optimization criterion rather than being treated only as a trajectory to reproduce.

The inferred objective can also be used as part of a human-to-humanoid locomotion transfer pipeline.

### Limitation

The objective representation is manually designed rather than learned from the demonstrations.

The locomotion model is simplified and does not represent full-body humanoid dynamics, contact interactions, or whole-body balance constraints.

The approach is demonstrated for a relatively specific locomotion task and does not establish a general latent representation of human objectives.

The work also does not systematically investigate robustness to disturbances, changes in robot dynamics, or substantially different physical constraints.

### Relevance to Our Project

This paper is highly relevant to our research because it demonstrates a pipeline closely related to our proposed approach:

Human Motion Demonstrations
→ Infer Underlying Objective / Cost
→ Model-Based Optimization
→ Humanoid Motion

Importantly, it shows that Human → IOC → Humanoid is not by itself a novel research direction.

Our project therefore needs to investigate whether a learned objective representation can provide advantages beyond manually specified cost functions, particularly when the learned objective is optimized under the different dynamics and physical constraints of the Unitree H1.

### Research Gap Contribution

The paper establishes that an underlying human locomotion objective can be inferred from demonstrations and subsequently used for humanoid motion generation.

However, the objective representation itself is manually specified and only its parameters are inferred.

This leaves an important distinction for our research:

Manually Designed Objective Representation
→ Learn Objective Parameters

versus the direction investigated in our project:

Human Motion
→ Learn Latent Objective Representation
→ Optimize under H1 Dynamics and Constraints

Whether this distinction represents a genuine research gap is **Not established yet** and must be evaluated against subsequent Inverse Optimal Control, Inverse Reinforcement Learning, human locomotion, and model-based control literature.




## Berret et al. (2011)

**Citation**
Berret, B., Chiovetto, E., Nori, F., & Pozzo, T. (2011). *Evidence for Composite Cost Functions in Arm Movement Planning: An Inverse Optimal Control Approach*. PLoS Computational Biology, 7(10), e1002183.

**Literature Category**
Inverse Optimal Control (IOC) / Human Motor Control / Composite Objective Learning

---

### 1. Research Problem

The paper investigates whether human arm movements can be explained by optimizing a **combination of multiple movement criteria**, rather than a single criterion.

The central question is:

> Can the underlying objective of human movement be inferred from observed trajectories, and is this objective better represented as a combination of multiple costs?

This is important for our project because it provides evidence that human behavior may arise from **multiple simultaneously optimized criteria** rather than one simple objective.

**Important scope distinction:** the study concerns human **arm reaching**, not locomotion.

---

### 2. Input

The input consists of observed human arm-reaching movements.

Participants perform reaching movements toward specified targets, and the resulting kinematic trajectories are used to infer the movement criterion.

The modeled system is a simplified planar two-joint human arm rather than a whole-body humanoid.

Therefore:

* Human motion: ✓
* Demonstration trajectories: ✓
* Arm reaching: ✓
* Locomotion: ✗
* Whole-body humanoid dynamics: ✗
* Robot morphology transfer: ✗

---

### 3. Method

The paper uses **Inverse Optimal Control (IOC)**.

In ordinary optimal control:

> Given an objective, determine the motion that minimizes that objective.

Conceptually:

[
\text{Objective} \rightarrow \text{Motion}
]

IOC reverses this direction:

[
\text{Observed Motion} \rightarrow \text{Objective}
]

The researchers observe how humans move and ask:

> What combination of candidate movement costs would make the observed human trajectory approximately optimal?

Several candidate cost functions are predefined. IOC then estimates their relative contributions by comparing motions generated under the candidate objective with experimentally observed human movements.

The important point is that the method **learns the weights of predefined objective components** rather than discovering an entirely new objective representation from raw motion.

---

### 4. Objective / Cost

The study evaluates several candidate criteria related to human arm movement, including measures associated with:

* mechanical effort / work,
* joint acceleration,
* movement smoothness,
* and other kinematic or dynamic criteria.

The main result is that a **composite cost** explains the observed movements better than individual criteria alone.

The most successful formulation combines:

[
\text{Mechanical Effort}
+
\text{Joint-Level Smoothness}
]

More specifically, the reported composite objective combines a measure based on the absolute work of joint torques with a measure based on integrated squared joint acceleration.

Conceptually:

[
J =
w_E J_{\text{effort}}
+
w_S J_{\text{smoothness}}
]

where (w_E) and (w_S) determine how strongly each criterion contributes to the overall objective.

### Interpretation

A simple example:

Suppose a person can reach a target using:

* a very energy-efficient but jerky movement, or
* a very smooth but energetically expensive movement.

If humans consistently choose something between these extremes, a composite objective can explain this behavior:

> The human is not optimizing only energy or only smoothness; both appear to influence the selected motion.

This is the key conceptual contribution relevant to our project.

---

### 5. Validation

The candidate objectives are evaluated by comparing trajectories generated by optimizing different cost formulations with experimentally observed human reaching trajectories.

The study finds that a combination of effort and smoothness-related terms reproduces important characteristics of human arm trajectories better than individual criteria alone.

Thus, the paper provides experimental evidence that:

[
\text{Human Motion}
\not\approx
\text{single criterion optimization}
]

and that:

[
\text{Human Motion}
\approx
\text{optimization of a composite objective}
]

within the studied arm-reaching task.

---

### 6. Main Finding

The main finding is:

> Human arm movements are better explained by a **composite cost function** than by a single movement criterion.

This supports the broader hypothesis that human behavior may emerge from simultaneous optimization of several competing objectives.

However, the finding is **task-specific**.

It establishes composite objectives for the studied arm-reaching behavior; it does **not** establish that human locomotion necessarily optimizes the same criteria.

---

### 7. Limitations

#### 7.1 Task limitation

The experiments concern arm reaching rather than locomotion.

Therefore, the results cannot directly establish that human walking or running optimizes mechanical effort and smoothness in the same way.

**Implication for our project:** candidate locomotion objectives must still be determined experimentally.

---

#### 7.2 Predefined objective representation

The candidate objective components are specified before learning.

The method primarily estimates the contribution/weight of candidate costs.

Therefore:

[
\text{Learning objective weights}
\neq
\text{Learning the objective representation itself}
]

This is an important distinction for our project.

Our project is interested in whether a more general or latent objective representation can be learned from human demonstrations rather than assuming all relevant objective components in advance.

---

#### 7.3 Simplified dynamics

The modeled system is a simplified human arm rather than a full humanoid.

It does not address:

* whole-body dynamics,
* legged locomotion,
* foot-ground contact,
* balance constraints,
* humanoid actuation limits,
* whole-body torque limits,
* or robot-specific physical constraints.

---

#### 7.4 No morphology/dynamics transfer

The paper does not investigate whether an inferred human objective remains meaningful when optimized under substantially different dynamics or morphology.

There is no:

[
\text{Human dynamics}
\rightarrow
\text{different humanoid dynamics}
]

transfer problem.

This is important because our target system is the Unitree H1, whose dynamics, actuation, contacts, and constraints differ substantially from those of a human.

---

#### 7.5 No model-based humanoid control

The learned objective is not demonstrated as the central cost of a modern whole-body humanoid MPC operating under realistic robot dynamics and constraints.

Therefore, the paper does not establish:

[
\text{Learned Human Objective}
+
\text{H1 Dynamics}
+
\text{H1 Constraints}
\rightarrow
\text{MPC}
]

---

#### 7.6 Generalization

The study primarily evaluates the ability of the candidate cost formulations to explain the studied arm-reaching behavior.

It does not establish generalization of an inferred objective across:

* different robot morphologies,
* different dynamics,
* substantially different tasks,
* disturbances,
* contact conditions,
* or unseen locomotion environments.

---

### 8. Relevance to Our Project

**Relevance: High, but indirect.**

This paper is important for the conceptual foundation of Phase 4 because it demonstrates that the underlying objective of human movement may be **composite**.

It supports considering multiple candidate objective components instead of assuming that human movement is governed by one simple criterion.

However, the paper does **not** justify assuming that the objective of human locomotion consists of effort + smoothness.

For our project:

> **Effort, smoothness, stability, energy, robustness, task success, etc. must remain candidate hypotheses until supported by locomotion literature and experiments.**

The paper is therefore relevant to **objective representation and learning**, but not sufficient evidence for the final H1 locomotion objective.

---

### 9. Research Gap Contribution

This paper establishes an important prior-art result:

> Human movement objectives can be inferred from demonstrations using IOC, and a composite objective can explain observed behavior better than individual candidate criteria.

Combined with Mombaur et al. (2010), the literature already establishes:

[
\text{Human Motion}
\rightarrow
\text{IOC}
\rightarrow
\text{Weighted Candidate Objectives}
]

Therefore, the following are **not sufficient novelty claims** for our project:

* using human demonstrations,
* applying IOC,
* learning weights of multiple hand-designed costs,
* or claiming that human behavior can be represented by a composite objective.

A potentially relevant distinction is that these works rely on **predefined objective components**, whereas our project is investigating whether a more generalizable objective representation can be learned and subsequently optimized under a different robot's dynamics and constraints.

However:

> **Whether this distinction constitutes a genuine research gap is NOT ESTABLISHED YET.**

It must be checked against subsequent IOC and IRL literature.

---

### 10. Direct Implications for Our Project

This paper gives us three concrete rules for the remainder of Phase 4.1:

**Rule 1 — Do not assume the objective structure.**

We should not begin with:

[
J =
w_1J_{\text{stability}}
+
w_2J_{\text{energy}}
+
w_3J_{\text{robustness}}
+
w_4J_{\text{task}}
]

as if these were known facts.

They are only candidate hypotheses.

---

**Rule 2 — Distinguish representation learning from weight learning.**

A method that starts with:

[
J =
\sum_i w_i\phi_i
]

and only learns (w_i) has learned the **parameters of a predefined representation**.

It has not necessarily discovered the underlying representation itself.

This distinction must remain explicit throughout Phase 4.

---

**Rule 3 — Locomotion evidence is required.**

Because Berret et al. study arm movement, their results cannot be directly transferred to human locomotion.

Therefore, the next relevant literature must determine:

> Which objective structures have actually been supported for human locomotion?

---

### 11. Position in Our Literature Review

| Question                                       | Berret et al. (2011)  |
| ---------------------------------------------- | --------------------- |
| Human demonstrations used?                     | Yes                   |
| IOC used?                                      | Yes                   |
| Objective inferred from motion?                | Yes                   |
| Composite objective investigated?              | Yes                   |
| Objective components predefined?               | Yes                   |
| Objective representation learned from scratch? | No                    |
| Human locomotion?                              | No                    |
| Humanoid dynamics?                             | No                    |
| Robot morphology transfer?                     | No                    |
| MPC integration?                               | No                    |
| H1-specific constraints?                       | No                    |
| Generalization across different dynamics?      | No                    |
| Evidence for multiple human objectives?        | Yes, for arm reaching |
| Direct evidence for locomotion objective?      | No                    |

**Overall role in our project:**
**Important conceptual IOC paper for composite objectives, but not direct evidence for humanoid locomotion.**

**Status:** **Required**

