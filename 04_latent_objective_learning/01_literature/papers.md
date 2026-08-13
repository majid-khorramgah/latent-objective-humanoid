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



## Paper 3 — Berret et al. (2011)

**Citation**
Berret, B., Chiovetto, E., Nori, F., & Pozzo, T. (2011). *Evidence for Composite Cost Functions in Arm Movement Planning: An Inverse Optimal Control Approach*. PLoS Computational Biology, 7(10), e1002183.

**Literature Category**
Inverse Optimal Control (IOC) / Human Motor Control / Composite Objective Learning

---

### 1. Research Problem

The paper investigates whether human arm movements can be explained by optimizing a **combination of multiple movement criteria**, rather than a single criterion.

The central question is:

> Can the underlying objective of human movement be inferred from observed trajectories, and is this objective better represented as a combination of multiple costs?

In simple terms, the authors ask whether humans are optimizing only one thing during movement, such as minimizing energy, or whether several criteria influence the selected motion simultaneously.

This is important for our project because it provides evidence that human behavior may arise from **multiple simultaneously optimized criteria** rather than one simple objective.

**Important scope distinction:** the study concerns human **arm reaching**, not locomotion.

---

### 2. Input

The input consists of observed human arm-reaching movements.

Participants perform reaching movements toward specified targets, and the resulting kinematic trajectories are used to evaluate which candidate movement objectives best explain the observed behavior.

The modeled system is a simplified planar two-joint human arm rather than a whole-body humanoid.

Therefore:

* Human motion: ✓
* Demonstration trajectories: ✓
* Arm reaching: ✓
* Locomotion: ✗
* Whole-body humanoid dynamics: ✗
* Foot-ground contact: ✗
* Robot morphology transfer: ✗

---

### 3. Method

The paper uses **Inverse Optimal Control (IOC)**.

A simple way to understand IOC is to compare it with ordinary optimal control.

In ordinary optimal control:

**Objective → Motion**

We know what we want the system to optimize, and we calculate the motion that best satisfies that objective.

IOC reverses the direction:

**Observed Motion → Objective**

We observe how a human actually moved and ask:

> What objective could make this observed movement approximately optimal?

The researchers define several candidate movement costs in advance. They then use IOC to determine which combination of these candidate costs can best explain the observed human trajectories.

Therefore, the method is primarily:

**Human motion → candidate costs → learned cost weights → reconstructed motion**

The important point is that the method **learns the contribution/weights of predefined objective components** rather than discovering an entirely new objective representation from raw motion.

---

### 4. Objective / Cost

The study evaluates several candidate criteria related to human arm movement, including measures associated with:

* mechanical effort / work,
* joint acceleration,
* movement smoothness,
* and other kinematic or dynamic criteria.

The main result is that a **composite cost** explains the observed movements better than individual criteria alone.

The most successful formulation combines criteria related to:

* **mechanical effort**, and
* **joint-level smoothness**.

Conceptually:

`J = w_E * J_effort + w_S * J_smoothness`

where:

* `J_effort` represents the effort-related component,
* `J_smoothness` represents the smoothness-related component,
* `w_E` and `w_S` determine their relative contribution.

More specifically, the reported successful formulation combines a measure based on the absolute work of joint torques with a measure based on integrated squared joint acceleration.

### Interpretation

Consider two possible movements to the same target:

* Movement A uses relatively little effort but contains abrupt changes in acceleration.
* Movement B is very smooth but requires more effort.

If human movements tend to lie between these extremes, a composite objective can explain this behavior:

> The human is not optimizing only effort or only smoothness; both criteria can contribute to the selected movement.

This is the key conceptual contribution relevant to our project.

**Important:** this does **not** mean that effort and smoothness are established as the objectives of human locomotion. The evidence in this paper is for the studied arm-reaching task.

---

### 5. Validation

The candidate objectives are evaluated by comparing trajectories generated under different cost formulations with experimentally observed human reaching trajectories.

The study finds that a combination of effort- and smoothness-related terms reproduces important characteristics of human arm trajectories better than individual criteria alone.

Therefore, within the studied task, the paper provides evidence that:

**Human Motion ≠ optimization of only one candidate criterion**

and that:

**Human Motion ≈ optimization of a composite objective**

The important conclusion is not that one particular objective has been proven to be the universal human objective, but that **a combination of multiple criteria can provide a better explanation of observed behavior**.

---

### 6. Main Finding

The main finding is:

> Human arm movements are better explained by a **composite cost function** than by a single movement criterion.

This supports the broader hypothesis that human behavior may emerge from simultaneous optimization of several competing objectives.

However, the finding is **task-specific**.

It establishes evidence for a composite objective in the studied arm-reaching behavior. It does **not** establish that human locomotion necessarily optimizes the same criteria.

---

### 7. Limitations

#### 7.1 Task limitation

The experiments concern **arm reaching**, not locomotion.

Therefore, the results cannot directly establish that human walking or running optimizes mechanical effort and smoothness in the same way.

**Implication for our project:** candidate locomotion objectives must still be determined from locomotion-specific literature and experiments.

---

#### 7.2 Predefined objective representation

The candidate objective components are specified before learning.

The method primarily estimates the contribution or weight of these candidate costs.

Therefore:

**Learning objective weights ≠ learning the objective representation itself**

This distinction is important for our project.

If we define:

`J = w_1 * φ_1 + w_2 * φ_2 + ...`

and only learn the `w_i`, then we have learned the parameters of a predefined objective representation.

We have not necessarily discovered what the relevant objective features `φ_i` should be.

---

#### 7.3 Simplified dynamics

The modeled system is a simplified human arm rather than a full humanoid.

The study does not address:

* whole-body humanoid dynamics,
* legged locomotion,
* foot-ground contact,
* whole-body balance,
* humanoid actuation limits,
* whole-body torque constraints,
* or robot-specific physical constraints.

---

#### 7.4 No morphology/dynamics transfer

The paper does not investigate whether an inferred human objective remains meaningful when optimized under substantially different dynamics or morphology.

There is no demonstrated:

**Human dynamics → different humanoid dynamics**

transfer problem.

This is important for our project because the target system is the Unitree H1, whose morphology, dynamics, actuation limits, contacts, and physical constraints differ from those of a human.

---

#### 7.5 No model-based humanoid control

The learned objective is not demonstrated as the central cost of a whole-body humanoid MPC operating under realistic robot dynamics and physical constraints.

Therefore, the paper does not establish the pipeline:

**Learned Human Objective + H1 Dynamics + H1 Constraints → MPC**

This remains a separate problem for our project.

---

#### 7.6 Limited generalization scope

The study evaluates how well candidate cost formulations explain the studied human arm-reaching behavior.

It does not establish generalization of the inferred objective across:

* different robot morphologies,
* substantially different dynamics,
* locomotion tasks,
* contact conditions,
* external disturbances,
* or unseen humanoid environments.

---

### 8. Relevance to Our Project

**Relevance: High, but indirect.**

This paper is important for the conceptual foundation of Phase 4 because it demonstrates that the underlying objective of human movement may be **composite**.

It supports the idea that we should consider multiple candidate objective components rather than assume that human behavior is governed by one simple criterion.

However, this paper does **not** justify assuming that human locomotion has an objective such as:

`effort + smoothness`

For our project:

> **Effort, smoothness, stability, energy, robustness, task success, etc. must remain candidate hypotheses until supported by locomotion-specific literature and experiments.**

The paper is therefore highly relevant to **objective representation and IOC**, but it is not direct evidence for the final H1 locomotion objective.

---

### 9. Research Gap Contribution

This paper establishes an important prior-art result:

> Human movement objectives can be investigated from demonstrations using IOC, and a composite objective can explain observed behavior better than individual candidate criteria.

Combined with Mombaur et al. (2010), the literature already establishes the following general approach:

**Human Motion → IOC → Weighted Candidate Objectives**

Therefore, the following are **not sufficient novelty claims** for our project:

* using human demonstrations,
* applying IOC,
* learning weights of multiple hand-designed costs,
* or showing that human behavior can be represented by a composite objective.

A potentially relevant distinction is that these approaches rely on **predefined objective components**, whereas our project is investigating whether a more generalizable objective representation can be learned and subsequently optimized under a different robot's dynamics and physical constraints.

However:

> **Whether this distinction constitutes a genuine research gap is NOT ESTABLISHED YET.**

This must be checked against subsequent IOC and IRL literature before being used as a novelty claim.

---

### 10. Direct Implications for Our Project

This paper gives us three concrete rules for the remainder of Phase 4.1.

#### Rule 1 — Do not assume the objective structure

We should not begin with an objective such as:

`J = w_1 * J_stability + w_2 * J_energy + w_3 * J_robustness + w_4 * J_task`

as if these components were already established.

At this stage, they are only **candidate hypotheses**.

The literature and experiments must determine which components are actually supported.

---

#### Rule 2 — Distinguish representation learning from weight learning

A method that starts with:

`J = Σ w_i * φ_i`

and only learns `w_i` has learned the **parameters of a predefined representation**.

It has not necessarily discovered the underlying objective representation itself.

This distinction must remain explicit throughout Phase 4.

---

#### Rule 3 — Locomotion evidence is required

Because Berret et al. study arm movement, their findings cannot be directly transferred to human locomotion.

Therefore, the next literature must answer:

> Which objective structures have actually been supported by experiments on human locomotion?

This question is more important for our project than simply collecting additional IOC papers.

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
**Important conceptual IOC paper for composite objectives, but not direct evidence for human locomotion or humanoid control.**

**Status:** **Required**
