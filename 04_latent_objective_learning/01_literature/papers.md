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

## Paper 4 — Clever & Mombaur (2016); Clever, Hu & Mombaur (2018)

**Primary References**

1. Clever, D., & Mombaur, K. (2016). *An Inverse Optimal Control Approach for the Transfer of Human Walking Motions in Constrained Environment to Humanoid Robots*. Robotics: Science and Systems XII. DOI: 10.15607/RSS.2016.XII.005.

2. Clever, D., Hu, Y., & Mombaur, K. (2018). *Humanoid Gait Generation in Complex Environments Based on Template Models and Optimality Principles Learned from Human Beings*. The International Journal of Robotics Research, 37(10), 1184–1204. DOI: 10.1177/0278364918765620.

**Literature Category**
Inverse Optimal Control (IOC) / Human Locomotion / Human-to-Humanoid Transfer / Optimal Control

---

### 1. Research Problem

The work investigates whether optimality principles underlying human walking can be identified from human motion-capture data and then transferred to humanoid robots for gait generation in constrained or complex environments.

The key idea is to avoid direct trajectory imitation:

[
\text{Human Motion}
\rightarrow
\text{Infer Optimality Criteria}
\rightarrow
\text{Optimize for Humanoid}
]

The 2016 work demonstrates the computational transfer pipeline in constrained walking scenarios, particularly irregular stepping stones. The 2018 journal paper extends this framework and includes further transfer and robot-level gait generation results.

---

### 2. Input

The input consists of human walking motion-capture data collected in constrained locomotion scenarios.

The approach uses a simplified 3D locomotion **template model** rather than a full detailed human musculoskeletal model.

The template represents locomotion through variables including:

* center-of-mass trajectory,
* foot trajectories,
* upper-body/torso orientation,
* single- and double-support phase durations.

The model includes dynamics and constraints and can be parameterized to represent both human and humanoid locomotion.

**Important:** the method is focused on human locomotion, unlike Berret et al. (2011), which studies arm reaching.

---

### 3. Method

The method is based on **Inverse Optimal Control (IOC)**.

In ordinary optimal control:

[
\text{Known Objective}
\rightarrow
\text{Optimal Motion}
]

In IOC, the direction is reversed:

[
\text{Observed Human Motion}
\rightarrow
\text{Infer Objective}
]

The authors define an objective as a weighted combination of physically meaningful candidate criteria:

[
J =
\sum_i w_i J_i
]

where (J_i) are predefined candidate locomotion criteria and (w_i) are their unknown weights.

The IOC procedure searches for objective weights such that the motion generated by solving the forward optimal-control problem resembles the observed human walking motion.

After identifying the objective from human motion, the same optimality strategy is used in a robot-specific forward optimal-control problem.

The robot optimization incorporates the robot's own model parameters, constraints, and environmental conditions.

---

### 4. Objective / Cost

The objective is represented as a weighted combination of physically meaningful locomotion criteria motivated by optimal humanoid gait generation.

The important structural assumption is:

[
J =
w_1J_1+w_2J_2+\cdots+w_nJ_n
]

The candidate criteria are defined before IOC and the method identifies their relative importance from human walking data.

Therefore, the method learns:

**objective weights**

rather than:

**the objective representation itself.**

This distinction is important for our project.

The work demonstrates that several locomotion criteria can jointly explain human walking behavior and that the resulting optimality strategy can subsequently be used for humanoid gait generation.

---

### 5. Human-to-Humanoid Transfer

The key transfer mechanism is:

[
\boxed{
\text{Human Motion}
\rightarrow
\text{IOC}
\rightarrow
\text{Human Optimality Criteria}
\rightarrow
\text{Robot-Specific Optimal Control}
\rightarrow
\text{Humanoid Motion}
}
]

The human trajectory is **not simply copied** onto the humanoid.

Instead, the inferred optimality strategy is re-optimized using the humanoid's own dynamics, model parameters, constraints, and environment.

This allows the resulting robot motion to differ from the human trajectory while preserving the inferred optimization principle.

The 2016 study demonstrates transfer to different humanoid embodiments, including iCub@Heidelberg and HRP-2@LAAS, in an irregular stepping-stone scenario.

The 2018 extension further develops the framework for humanoid gait generation in complex environments and demonstrates transfer to iCub in simulation and on the real robot.

---

### 6. Validation

The approach is evaluated on human walking in constrained environments and subsequently used to generate humanoid gait.

The 2016 work demonstrates a complete computational cycle from:

[
\text{Human Motion Capture}
\rightarrow
\text{IOC}
\rightarrow
\text{Optimized Robot Template Motion}
]

for walking over irregular stepping stones.

The inferred strategy is then applied to different humanoid models.

The 2018 journal extension expands the framework and reports robot-level gait generation, including transfer of optimized template motion to iCub through inverse kinematics and evaluation in simulation and on the real robot.

The results demonstrate that human-derived optimality criteria can be used to generate feasible humanoid motions in environments that differ from the original human experiments.

---

### 7. Main Finding

The main finding is:

> Optimality criteria identified from human walking can be transferred from human motion to humanoid gait generation when the optimization is re-solved using the robot's own model and constraints.

This provides strong evidence that the **underlying optimization principle**, rather than the exact human trajectory, can be useful for human-to-humanoid motion transfer.

The work therefore establishes a direct precedent for:

[
\text{Human Demonstrations}
\rightarrow
\text{IOC}
\rightarrow
\text{Humanoid Optimal Control}
]

---

### 8. Limitations

#### 8.1 Novelty limitation for our project

Human locomotion demonstrations + IOC + humanoid transfer is **already established prior art**.

Therefore, the following cannot independently constitute the novelty of our project:

* learning an objective from human walking,
* using IOC,
* generating new humanoid motion from the inferred objective,
* or transferring an optimization strategy between different humanoid embodiments.

---

#### 8.2 Predefined objective representation

The candidate objective components are manually specified based on physically meaningful criteria.

IOC identifies their weights.

Therefore:

[
\text{Weight Learning}
\neq
\text{Objective Representation Learning}
]

The method does not discover an arbitrary latent objective representation directly from human motion.

---

#### 8.3 Template-model limitation

The approach relies on an abstract 3D locomotion template rather than full-body, high-dimensional humanoid dynamics during objective identification.

The template captures important locomotion variables but does not represent every detail of human or humanoid whole-body dynamics.

Therefore, it does not establish that the inferred objective remains unchanged when moving from a simplified template to a high-dimensional robot such as Unitree H1.

---

#### 8.4 Robot-specific adaptation

The inferred strategy is not transferred completely unchanged.

Robot-specific model parameters, objective scaling, bounds, and constraints are adjusted for the target humanoid.

Therefore, the work demonstrates **transfer of an optimization strategy**, but not complete morphology-independent objective transfer.

---

#### 8.5 Limited modern MPC integration

The work uses optimal control to generate robot motions, but it does not establish the use of a learned human objective as a continuously replanned, whole-body MPC objective for a modern humanoid platform such as Unitree H1.

The distinction between offline trajectory optimization and online model-predictive control remains relevant to our project.

---

#### 8.6 Generalization under changed dynamics

Although transfer to different humanoid embodiments and new environmental conditions is demonstrated, the work does not systematically establish that a learned human objective remains invariant under broad changes in:

* morphology,
* mass distribution,
* actuator limits,
* contact dynamics,
* external disturbances,
* or model uncertainty.

Therefore, broad **dynamics-invariant objective generalization** is not established by this work.

---

### 9. Relevance to Our Project

**Relevance: Very High.**

This is one of the closest existing works to our research direction.

It directly demonstrates:

[
\text{Human Walking}
\rightarrow
\text{Objective Identification}
\rightarrow
\text{Humanoid Optimization}
]

and shows that the human trajectory itself does not need to be directly imitated.

This strongly supports the conceptual direction proposed by Professor Dennis Hong.

However, it also means that our project cannot claim novelty simply from combining human demonstrations, IOC, and humanoid optimal control.

The more important question for our project is whether a **more generalizable objective representation** can be learned and then optimized under the substantially different dynamics and physical constraints of Unitree H1.

---

### 10. Research Gap Contribution

This work establishes the following prior art:

> Human walking data can be used with IOC to identify weighted locomotion optimality criteria, and the resulting strategy can be re-optimized for humanoid robots with different embodiments and environmental constraints.

Therefore, the following potential contributions are already substantially covered:

* human → IOC,
* locomotion objective identification,
* human → humanoid transfer,
* transfer across different humanoid embodiments,
* optimization under robot-specific constraints.

A remaining potential distinction is:

[
\boxed{
\text{Learned / latent objective representation}
}
]

combined with:

[
\boxed{
\text{generalization across substantially different dynamics}
}
]

and:

[
\boxed{
\text{direct integration with model-based MPC}
}
]

However, these are **candidate research gaps only**.

**Status: Not established yet.**

They must be checked against subsequent IOC, IRL, human-locomotion, and model-based-control literature before being used as a novelty claim.

---

### 11. Direct Implications for Our Project

This work establishes three important constraints for our research design.

**Constraint 1 — Do not claim Human → IOC → Humanoid as the main novelty.**

This pipeline already exists.

**Constraint 2 — Do not assume that the human objective can simply be copied to H1.**

The prior work itself adapts the optimization to the target robot's dynamics, parameters, and constraints.

**Constraint 3 — The important unresolved question is potentially the representation and transferability of the objective.**

Our project should therefore investigate whether the objective inferred from human demonstrations can remain useful when:

[
\text{Human Dynamics}
\neq
\text{H1 Dynamics}
]

while still allowing:

[
\text{Learned Objective}
+
\text{H1 Dynamics}
+
\text{H1 Constraints}
\rightarrow
\text{Feasible H1 Motion}
]

Whether this is genuinely novel remains **Not established yet**.

---

### 12. Position in Our Literature Review

| Question                                                                                     | Clever & Mombaur 2016/2018 |
| -------------------------------------------------------------------------------------------- | -------------------------- |
| Human demonstrations used?                                                                   | Yes                        |
| Human locomotion?                                                                            | Yes                        |
| IOC used?                                                                                    | Yes                        |
| Objective inferred from human motion?                                                        | Yes                        |
| Multiple candidate criteria?                                                                 | Yes                        |
| Candidate criteria predefined?                                                               | Yes                        |
| Objective representation learned from scratch?                                               | No                         |
| Humanoid transfer?                                                                           | Yes                        |
| Different humanoid embodiments?                                                              | Yes                        |
| Environmental constraints?                                                                   | Yes                        |
| Robot-specific dynamics/constraints?                                                         | Yes                        |
| Template model?                                                                              | Yes                        |
| Full high-dimensional humanoid dynamics during IOC?                                          | No                         |
| Direct Unitree H1 application?                                                               | No                         |
| Whole-body H1 MPC?                                                                           | No                         |
| Objective generalization across substantially different dynamics systematically established? | No                         |
| Direct trajectory imitation?                                                                 | No                         |
| Human optimality principle transferred rather than trajectory?                               | Yes                        |

**Overall role in our project:**
**Direct prior art and critical baseline for human-to-humanoid objective transfer.**

**Status:** **Required**

