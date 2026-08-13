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





## Paper 5 — Maroger, Stasse & Watier (2022)

**Title:** *Inverse Optimal Control to Model Human Trajectories During Locomotion*

**Citation**  
Maroger, I., Stasse, O., & Watier, B. (2022). *Inverse Optimal Control to Model Human Trajectories During Locomotion*. Computer Methods in Biomechanics and Biomedical Engineering, 25(5), 499–511. DOI: 10.1080/10255842.2021.1962311.

**Literature Category**  
Inverse Optimal Control (IOC) / Human Locomotion / Human Trajectory Modeling / Model-Based Simulation

---

### 1. Research Problem

The paper investigates whether human walking trajectories can be modeled using an **Optimal Control (OC) model whose cost-function parameters are inferred from human walking demonstrations using Inverse Optimal Control (IOC).**

The main motivation is human-robot collaboration.

The authors want a model that can generate human-like walking trajectories so that a humanoid robot can better predict and anticipate human motion during collaborative tasks.

In simple terms:

> Instead of directly copying a recorded human walking trajectory, can we find an optimization problem that generates trajectories similar to how humans actually walk?

This is directly relevant to our project because it establishes a concrete example of:

**Human locomotion demonstrations → IOC → learned cost parameters → generated locomotion trajectories**

However, the generated motion is a simplified **Center of Mass (CoM) trajectory**, not full-body humanoid motion.

---

### 2. Input

The study uses human walking demonstrations from:

- 10 healthy subjects
- 10 starting positions
- 4 starting orientations
- 1 common goal position
- 40 start/orientation combinations per subject
- 400 recorded trajectories in total

Subjects were instructed to walk at a self-selected normal speed toward the goal.

The motion-capture system recorded pelvis markers at 200 Hz.

The model uses:

- horizontal CoM position `(x, y)`
- pelvis orientation `theta`

as the main representation of locomotion.

The human body is therefore **not modeled as a full articulated humanoid**.

Instead, it is approximated as a simplified holonomic locomotion system moving in the horizontal plane. :contentReference[oaicite:1]{index=1}

Therefore:

- Human motion: ✓
- Human locomotion: ✓
- Human demonstrations: ✓
- Motion capture: ✓
- CoM trajectory: ✓
- Pelvis orientation: ✓
- Full-body human dynamics: ✗
- Full-body humanoid dynamics: ✗
- Foot-ground contact dynamics: ✗
- H1 morphology: ✗

---

### 3. Method

The paper uses a combination of:

**Optimal Control (OC)**  
+  
**Inverse Optimal Control (IOC)**

The basic idea is:

**Human Demonstration → IOC → Cost Parameters → Optimal Control → Generated Human-like Trajectory**

A simple way to understand IOC here:

Suppose we already have a model that says:

> "A walking system chooses its trajectory by minimizing a cost."

But we do not know the correct weights inside that cost.

For example:

`Cost = w1 * forward_acceleration + w2 * sideward_acceleration + w3 * orientation_cost + ...`

IOC asks:

> What values of `w1`, `w2`, `w3`, ... make the trajectory generated by the OC model look most like the trajectory measured from humans?

Therefore, this paper is **learning the parameters of a predefined cost function**, not discovering an arbitrary objective from scratch.

---

### 4. Locomotion Model

The human is modeled as a **holonomic locomotion system**.

The state contains:

- horizontal position `(x, y)`
- orientation `theta`
- forward velocity
- sideward velocity
- angular velocity

The controls correspond to:

- forward acceleration
- sideward acceleration
- angular acceleration

The model allows sideward motion.

This is important because humans do not always move strictly in the direction they are facing. Humans can make sideward or oblique movements when approaching a target.

The authors argue that a holonomic model can therefore represent human walking paths better than simpler non-holonomic models such as a unicycle model. :contentReference[oaicite:2]{index=2}

---

### 5. Objective / Cost

The objective contains both **running costs** and **terminal costs**.

The running cost contains terms associated with:

- a constant running cost,
- squared forward acceleration,
- squared sideward acceleration,
- squared angular acceleration,
- orientation/path-related error.

The terminal cost contains terms associated with:

- final position error,
- final orientation error,
- final forward/sideward velocity,
- final angular velocity.

Conceptually:

`Total Cost = Running Cost + Terminal Cost`

The important point is that the researchers do **not** invent an arbitrary neural latent objective.

Instead, they define a structured cost function first and use IOC to find its parameters.

The learned weights reported in the paper are approximately:

`alpha = (7.87, 4.00, 20.15, 0.000001, 10.00)`

for the running cost, and:

`beta = (10.00, 10.00, 0.38, 3.36)`

for the terminal cost.

These weights are specific to the model, formulation, dataset, and evaluation metric used in this study. They should **not** be interpreted as universal weights of human locomotion. :contentReference[oaicite:3]{index=3}

---

### 6. What Does the Learned Cost Mean?

An important result is that the learned weight for **sideward acceleration** is relatively large, while the weight for angular acceleration is almost zero.

The authors interpret this as evidence that the ability to move laterally is important for reproducing human walking trajectories.

In other words:

> A model that can only move forward is too restrictive to represent some human walking behavior.

This supports the use of a **holonomic locomotion model** rather than a simpler non-holonomic model.

However, the very small angular-acceleration weight does **not** necessarily mean that pelvis orientation is irrelevant.

The authors explicitly suggest that this term may be redundant because orientation already influences other terms in the model. :contentReference[oaicite:4]{index=4}

Therefore, we should **not** interpret individual learned weights as direct measurements of psychological or biological importance.

---

### 7. Validation

The authors compare generated trajectories with measured human trajectories.

For each of the 40 start/orientation conditions, the average trajectory across the 10 subjects is used as the reference human trajectory.

Two main errors are evaluated:

- linear distance between generated and measured CoM trajectories
- angular distance between generated and measured pelvis orientations

The optimized model generates 40 trajectories for evaluation.

The reported average errors are approximately:

`linear error = 0.0767 ± 0.0450 m`

`angular error = 0.3786 ± 0.1336 rad`

The generated trajectories are therefore reasonably close to the **average human behavior** under the chosen model and metric. :contentReference[oaicite:5]{index=5}

The paper also reports that the model produces homogeneous results across the tested starting orientations and global distances.

---

### 8. Main Finding

The main finding is:

> A relatively simple Optimal Control model, whose cost-function parameters are inferred from human walking trajectories using IOC, can reproduce the average horizontal CoM path and pelvis orientation of human locomotion.

The model is also computationally efficient enough to be considered for real-time humanoid applications.

The authors report an average generation time of approximately 1.45 seconds for the tested trajectories. :contentReference[oaicite:6]{index=6}

This establishes an important result for our literature review:

**IOC is not limited to arm movement. It has already been applied directly to human locomotion.**

---

### 9. Important Limitation: Average Human Behavior

The model does not reproduce every individual's walking behavior equally well.

The paper reports substantial variability between subjects.

The model describes the **average human trajectory** well, but it cannot accurately fit every individual behavior.

This is important for our project because it raises a fundamental question:

> Is there one shared human objective, or are there multiple subject-specific objectives that produce different but valid behaviors?

This question is highly relevant to our concept of a **generalizable latent human objective**.

However, this paper does not solve that problem.

---

### 10. Limitations

#### 10.1 Simplified representation

The model represents human locomotion primarily through:

- CoM position,
- pelvis orientation,
- forward/sideward velocities,
- and accelerations.

It does not model the full human body.

Therefore it does not capture:

- joint-level motion,
- leg configuration,
- foot placement,
- contact forces,
- joint torques,
- whole-body balance,
- muscle dynamics,
- or detailed humanoid dynamics.

---

#### 10.2 Predefined cost representation

The objective structure is manually specified.

IOC learns the parameters of that predefined structure.

Therefore:

**Learning cost weights ≠ discovering the objective representation**

This is one of the most important limitations for our project.

The paper does not demonstrate that the system can discover an unknown latent objective representation from raw human motion.

---

#### 10.3 No robot morphology transfer

The model represents human locomotion.

The learned objective is not demonstrated as a general objective that can be transferred between:

**Human morphology → humanoid morphology**

The paper therefore does not establish that the same learned objective can be optimized successfully under H1's dynamics.

---

#### 10.4 No full-body humanoid dynamics

Although the motivation is humanoid robotics and the paper discusses applications to humanoid robots, the locomotion model itself is not a full-body humanoid dynamics model.

There is no optimization over:

- H1 joint configurations,
- H1 joint torques,
- contact forces,
- foot contact constraints,
- actuator limits,
- friction constraints,
- whole-body momentum,
- or H1-specific dynamics.

Therefore, this is **human trajectory modeling for humanoid applications**, not yet **human objective transfer to a humanoid robot**.

---

#### 10.5 No direct MPC transfer of a human objective

The paper uses Optimal Control to generate trajectories from the learned cost.

However, it does not demonstrate the full pipeline:

**Human Demonstrations → Learned General Objective → H1 Dynamics → H1 Constraints → Whole-Body MPC**

That remains outside the scope of the study.

---

#### 10.6 Limited generalization

The study evaluates several starting positions and orientations, but the generalization is within the same simplified locomotion model and experimental task.

It does not establish generalization across:

- different robot morphologies,
- different physical dynamics,
- different walking speeds,
- disturbances,
- uneven terrain,
- contact changes,
- external perturbations,
- or humanoid-specific constraints.

---

#### 10.7 Objective identifiability

The paper demonstrates that a particular predefined cost model can reproduce human trajectories.

It does **not** establish that the inferred cost is the unique objective underlying human locomotion.

Different cost functions can potentially produce similar trajectories.

Therefore:

> A good trajectory fit does not automatically prove that the recovered cost is the true underlying human objective.

This distinction is critical for our project.

---

### 11. Relevance to Our Project

**Relevance: Very High.**

This is currently one of the most directly relevant papers in our IOC literature.

Unlike Berret et al. (2011), which studies arm reaching, this paper explicitly studies **human locomotion**.

It establishes that:

**Human Locomotion Demonstrations → IOC → Cost Parameters → Generated Human-like Locomotion**

has already been demonstrated.

This means our project cannot claim novelty simply because it:

- uses human locomotion demonstrations,
- uses IOC,
- learns locomotion cost weights,
- or generates human-like locomotion from an inferred cost.

Those ideas already have direct prior art.

---

### 12. Research Gap Contribution

This paper significantly narrows the possible research gap.

Before this paper, we could have considered:

> "Learning a locomotion objective from human demonstrations using IOC"

as a possible contribution.

After this paper, that is **not novel by itself**.

The existing pipeline is already:

**Human Locomotion → Predefined OC Cost → IOC Weight Learning → Human-like Trajectory Generation**

Therefore, our project needs to go beyond this.

Potential distinctions that remain worth investigating are:

1. **Objective representation**

   Can we learn a more general objective representation rather than only the weights of manually designed terms?

2. **Transfer across dynamics**

   Can an objective inferred from human demonstrations remain useful when optimized under the dynamics of a different humanoid?

3. **Constraint-aware transfer**

   Can the learned objective be optimized while satisfying the physical constraints of a real humanoid?

4. **Model-based MPC integration**

   Can the inferred objective become the actual cost of a model-based controller rather than only a trajectory-generation model?

5. **Generalization**

   Does the learned objective remain useful under unseen tasks, initial conditions, dynamics, or constraints?

6. **Separating objective from morphology**

   Can we distinguish what comes from the human's underlying task objective from what comes from the human body's own morphology and dynamics?

However:

> **None of these is established as a research gap yet.**

They are candidate directions that must be checked against the remaining IOC, IRL, locomotion-objective, and model-based-control literature.

---

### 13. Direct Implications for Our Project

This paper gives us several important decisions.

#### Rule 1 — "IOC for human locomotion" is already done

We should **not** use:

> "We learn human locomotion objectives using IOC."

as the main novelty claim.

That problem has already been addressed. :contentReference[oaicite:7]{index=7}

---

#### Rule 2 — Human-like trajectory generation is not enough

The paper demonstrates that an inferred cost can generate human-like CoM trajectories.

Therefore, our project needs to ask a harder question:

> Can an inferred objective be useful when the dynamics and constraints are changed from human to humanoid?

This is much closer to the question suggested by Professor Hong.

---

#### Rule 3 — Objective representation matters

Maroger et al. use a predefined cost structure.

Therefore, our literature review must distinguish between:

**Learning parameters of a known cost**

and:

**Learning an objective representation from demonstrations.**

These are not the same research problem.

---

#### Rule 4 — Trajectory fit is not proof of the true objective

A cost that produces a trajectory close to human data is evidence that the cost is **behaviorally explanatory under the chosen model**.

It is not proof that the cost represents the actual internal objective used by humans.

Therefore, our future evaluation should eventually consider:

- held-out demonstrations,
- unseen conditions,
- alternative objective formulations,
- and whether the inferred objective produces useful behavior outside the demonstrations used for learning.

---

### 14. Position in Our Literature Review

| Question | Maroger et al. (2022) |
|---|---|
| Human demonstrations used? | Yes |
| Human locomotion? | Yes |
| IOC used? | Yes |
| Objective inferred from motion? | Yes |
| Cost weights learned? | Yes |
| Objective components predefined? | Yes |
| Objective representation learned from scratch? | No |
| Full-body human dynamics? | No |
| Full-body humanoid dynamics? | No |
| Humanoid morphology transfer? | No |
| H1 dynamics? | No |
| H1 constraints? | No |
| Whole-body MPC? | No |
| Learned objective used directly in H1 MPC? | No |
| Generalization across different dynamics? | No |
| Individual human behavior modeled well? | Limited |
| Average human behavior modeled? | Yes |
| Direct human-locomotion IOC prior art? | Yes |

---

### 15. Comparison with Previous Papers

The progression is now important:

**Mombaur et al. (2010)**  
Human locomotion → IOC → predefined locomotion cost → humanoid-oriented motion generation.

**Berret et al. (2011)**  
Human arm motion → IOC → composite cost → evidence that multiple criteria can explain human movement.

**Maroger et al. (2022)**  
Human locomotion → IOC → predefined CoM locomotion cost → human-like trajectory generation for humanoid/cobotic applications.

Therefore, the literature has already established:

**Human Demonstrations → IOC → Cost Parameters → Human-like Motion**

Our project must therefore investigate what comes **after** this established pipeline.

The potentially important next step is:

**Human Demonstrations → Generalizable Objective → New Robot Dynamics + Constraints → Model-Based MPC**

But this remains:

**Not Established Yet.**

---

### 16. Overall Role in Our Project

**Very important prior-art paper.**

This paper is the strongest evidence so far that the basic idea of learning a human locomotion cost from demonstrations using IOC is **not novel by itself**.

Its most important contribution to our project is therefore not simply its method, but the way it **constrains our research question**.

It tells us:

> We cannot make "IOC for human locomotion" the contribution.

Instead, we need to determine whether there is a scientifically defensible gap involving:

- learned/generalizable objective representation,
- transfer across morphology and dynamics,
- physical constraints,
- model-based MPC,
- or generalization to unseen conditions.

**Status:** Required






## Paper 6 — Liu et al. (2022)

**Citation**  
Liu, W., Zhong, J., Wu, R., Fylstra, B. L., Si, J., & Huang, H. H. (2022). *Inferring Human-Robot Performance Objectives During Locomotion Using Inverse Reinforcement Learning and Inverse Optimal Control*. IEEE Robotics and Automation Letters, 7(2), 2549–2556. DOI: 10.1109/LRA.2022.3143579.

**Literature Category**  
Inverse Reinforcement Learning (IRL) / Inverse Optimal Control (IOC) / Human-Robot Locomotion / Wearable Robotics / Performance Objective Learning

---

### 1. Research Problem

The paper investigates whether the locomotion performance objective of a **human-robot system** can be inferred from observed walking behavior.

The target application is lower-limb wearable robotics, particularly systems such as robotic prostheses.

The central question is:

> Can observed human-robot walking behavior be used to infer a quantitative performance objective that characterizes how the human-robot system behaves?

The paper approaches this as an inverse problem and evaluates two approaches:

- Inverse Reinforcement Learning (IRL)
- Inverse Optimal Control (IOC)

The important distinction from conventional control is:

**Forward problem:**

`Objective → Controller → Behavior`

**Inverse problem:**

`Observed Behavior → Objective`

---

### 2. Input

The study uses human-robot locomotion behavior from a robotic lower-limb system.

The experimental component involves human walking with a **robotic transfemoral prosthesis**.

The robot controller is an impedance controller whose parameters influence the behavior of the robotic knee.

The state representation uses gait-related performance errors.

One example defines:

`ΔP = P - Pd`

`ΔD = D - Dd`

where:

- `P` is the measured peak knee angle,
- `Pd` is the desired peak knee angle,
- `D` is the measured timing/duration,
- `Dd` is the desired timing/duration.

Thus the state can be represented as:

`s = [ΔP, ΔD]`

The corresponding control/action variables represent changes to robotic impedance parameters.

Therefore:

- Human behavior: ✓
- Human locomotion: ✓
- Human-robot locomotion: ✓
- Wearable robot: ✓
- Robotic prosthesis: ✓
- Full-body humanoid: ✗
- Independent humanoid robot: ✗
- H1 dynamics: ✗

---

### 3. Method

The paper formulates the problem using both:

- Inverse Reinforcement Learning (IRL)
- Inverse Optimal Control (IOC)

The basic pipeline is:

`Human-Robot Walking Behavior`
  
`→ State / Feature Representation`
  
`→ IRL or IOC`
  
`→ Estimated Objective`
  
`→ Analysis of Human-Robot System`

The two approaches serve somewhat different purposes.

#### IRL

IRL is used with human-robot behavioral data to infer a cost function that explains the observed behavior.

Conceptually:

`Observed behavior → IRL → Cost`

#### IOC

IOC is used with a modeled human-robot system to infer objective parameters and then analyze control-theoretic properties of the system.

This allows the authors to investigate properties such as:

- stability,
- robustness,
- and other system-level control characteristics.

The paper emphasizes that these properties can be difficult to obtain directly from human experiments.

---

### 4. Objective / Cost Representation

The paper uses a **quadratic cost representation**.

The general form is:

`r(s) = s^T H s`

where:

- `s` is the vector of state/performance features,
- `H` is a weighting matrix,
- the entries of `H` are unknown objective weights to be inferred.

For the example with:

`s = [ΔP, ΔD]`

the cost can be represented as:

`J = w1 * (ΔP)^2 + w2 * (ΔD)^2`

where:

- `w1` determines the importance of peak error,
- `w2` determines the importance of duration error.

The important methodological point is:

> The feature representation is specified before learning; the inverse method estimates the relative weighting of those features.

Therefore:

**Learning objective weights ≠ discovering the objective representation from scratch.**

---

### 5. Experimental Design

The human experiments involve walking with a robotic transfemoral prosthesis.

The robotic knee controller is designed around gait-cycle features.

Different behavioral protocols are used to test whether changes in human-robot behavior can be reflected in the inferred performance objective.

The experimental data are then supplied to the IRL procedure.

The authors report that different behavioral protocols result in different inferred performance representations, supporting the feasibility of using inverse learning to characterize human-robot locomotion performance.

---

### 6. Validation

The paper uses two complementary validation components.

#### 6.1 Human-robot experiment

The IRL approach is evaluated using experimentally collected human-robot walking data.

This demonstrates the practical applicability of the inverse approach to a real human-robot locomotion system.

#### 6.2 Simulation / IOC analysis

A simulation study is used to evaluate the IOC formulation.

The IOC analysis allows the researchers to extract system properties such as:

- stability,
- robustness,
- and control-theoretic characteristics.

These properties are difficult to directly infer from human experiments alone.

Therefore, the paper demonstrates both:

`Human-robot behavior → IRL → inferred objective`

and:

`Modeled human-robot system → IOC → objective/system properties`

---

### 7. Main Finding

The main finding is:

> Human-robot locomotion performance objectives can be inferred from observed behavior using inverse learning methods.

Both IRL and IOC are shown to be feasible for the proposed inverse formulation.

The experimental IRL results demonstrate that the method can be applied to real human-robot walking behavior.

The IOC analysis demonstrates that an inferred objective can also be used to investigate system-level properties such as stability and robustness.

The paper therefore provides a concrete example of:

`Human-Robot Locomotion Demonstrations`

`→ Inferred Performance Objective`

rather than simply reproducing observed trajectories.

---

### 8. Important Interpretation

The inferred objective should not automatically be interpreted as the **true biological objective** of the human.

The method identifies an objective representation that explains the observed behavior under the selected system model and feature representation.

Therefore:

`Observed Behavior → Estimated Objective`

does not necessarily imply:

`Estimated Objective = True Internal Human Objective`

Different objective formulations may potentially explain similar behavior.

This objective-identifiability issue remains important for our project.

---

### 9. Limitations

#### 9.1 Predefined feature representation

The objective is represented using predefined features and a quadratic form.

For example:

`J = w1 * (Peak Error)^2 + w2 * (Duration Error)^2`

The inverse method learns the weights but does not discover the relevant features from raw motion.

Therefore:

**Parameter learning ≠ representation discovery**

This is directly relevant to our project.

---

#### 9.2 Wearable robot rather than independent humanoid

The robot is a lower-limb wearable system / robotic prosthesis.

The robot physically participates in the human's locomotion rather than acting as an independent humanoid with its own complete morphology and locomotion dynamics.

Therefore, the paper does not establish transfer from:

`Human Objective → Independent Humanoid`

---

#### 9.3 No full-body humanoid dynamics

The study does not optimize a full humanoid model containing:

- whole-body joint dynamics,
- foot-ground contacts,
- whole-body momentum,
- contact forces,
- actuator limits,
- joint torque limits,
- friction constraints,
- or humanoid-specific balance constraints.

Therefore it does not address H1's full physical constraints.

---

#### 9.4 No morphology transfer

The inferred objective is not demonstrated under substantially different robot morphology.

There is no experiment of:

`Human behavior → inferred objective → different humanoid morphology`

Therefore, transfer across morphology remains unaddressed.

---

#### 9.5 No H1 model-based MPC

The paper does not demonstrate:

`Learned human objective`

`+ H1 dynamics`

`+ H1 constraints`

`→ whole-body MPC`

This is outside the scope of the study.

---

#### 9.6 Limited objective representation

The quadratic feature representation is useful for tractability and interpretation, but it constrains what the inverse method can learn.

If the real behavior depends on features not included in the representation, the inverse method cannot discover them.

Therefore, the method cannot establish that the selected feature set is complete.

---

#### 9.7 Objective depends on the human-robot system

The paper focuses on a **collective human-robot performance objective**.

Therefore, the inferred objective may reflect interaction between the human and the specific wearable robotic system.

This is different from learning a morphology-independent objective belonging only to the human.

This distinction is important for our project.

---

#### 9.8 Generalization across robot dynamics

The paper does not establish that the inferred objective remains valid when the robot dynamics change substantially.

There is no demonstrated transfer across:

- different humanoid morphologies,
- different whole-body dynamics,
- different contact models,
- or different actuator constraints.

---

### 10. Relevance to Our Project

**Relevance: High, but conceptually different from our target problem.**

This paper is important because it demonstrates that inverse methods can infer a quantitative locomotion performance objective from **human-robot behavior**.

It also demonstrates the useful combination of:

`Inverse Learning + Model-Based Control Analysis`

However, the robot is a wearable lower-limb device rather than an independent humanoid.

Therefore, the paper does not solve our target problem:

`Human Demonstrations`

`→ Human Objective`

`→ H1 Dynamics`

`→ H1 Physical Constraints`

`→ Model-Based MPC`

---

### 11. Research Gap Contribution

This paper rules out another overly broad novelty claim.

The following is **not sufficient novelty**:

> "We infer a locomotion objective from human-robot walking behavior using IRL or IOC."

That has already been demonstrated.

The paper also shows that inverse learning can produce an objective useful for analyzing stability and robustness of a modeled human-robot system.

Therefore, simply claiming:

- objective learning,
- IRL,
- IOC,
- quadratic cost learning,
- or human-robot locomotion objective inference

is not enough.

Potentially relevant distinctions for our project remain:

1. Learning a more generalizable objective representation.
2. Separating human objective from robot morphology and dynamics.
3. Transferring a learned objective from human behavior to an independent humanoid.
4. Optimizing the learned objective under different robot dynamics.
5. Enforcing humanoid-specific physical constraints.
6. Using the learned objective directly inside whole-body model-based MPC.
7. Evaluating generalization under unseen robot dynamics, tasks, or disturbances.

However:

> **Whether any of these constitutes a genuine research gap is NOT ESTABLISHED YET.**

They remain candidate directions until the remaining IOC, IRL, human-locomotion-objective, and model-based-control literature has been reviewed.

---

### 12. Direct Implications for Our Project

#### Rule 1 — Human-robot objective inference is already prior art

We cannot claim novelty simply because we infer a locomotion objective from human-robot behavior.

This has already been demonstrated using both IRL and IOC.

---

#### Rule 2 — Do not confuse human objective with human-robot objective

Liu et al. study a **collective human-robot performance objective**.

Our project is currently interested in:

`Human demonstrations → latent human objective`

before applying that objective to H1.

Therefore, the distinction between:

`Human objective`

and:

`Human-robot system objective`

must remain explicit.

---

#### Rule 3 — Representation remains a key question

The paper uses a predefined quadratic feature representation.

Therefore, it does not establish that the correct objective representation for human locomotion is known.

This supports keeping the objective representation as an **open research question** in Phase 4.

---

#### Rule 4 — Model-based analysis is relevant

The IOC component shows that an inferred objective can be connected to model-based analysis of stability and robustness.

This is conceptually relevant to the later transition:

`Learned Objective → Model-Based Control`

but the paper does not perform the H1/MPC transfer we are targeting.

---

### 13. Position in Our Literature Review

| Question | Liu et al. (2022) |
|---|---|
| Human demonstrations used? | Yes |
| Human locomotion? | Yes |
| Human-robot locomotion? | Yes |
| IRL used? | Yes |
| IOC used? | Yes |
| Objective inferred from behavior? | Yes |
| Quadratic objective? | Yes |
| Objective features predefined? | Yes |
| Objective representation learned from scratch? | No |
| Human-only objective? | No |
| Human-robot collective objective? | Yes |
| Wearable robot? | Yes |
| Robotic prosthesis? | Yes |
| Independent humanoid? | No |
| Full-body humanoid dynamics? | No |
| H1 dynamics? | No |
| H1 constraints? | No |
| Whole-body MPC? | No |
| Morphology transfer? | No |
| Generalization across robot dynamics? | No |
| Stability/robustness analysis? | Yes |
| Objective transfer to a different robot? | No |

---

### 14. Comparison With Previous Papers

The current literature progression is:

**Mombaur et al. (2010)**

`Human locomotion → IOC → predefined locomotion cost → humanoid-oriented trajectory generation`

**Berret et al. (2011)**

`Human arm motion → IOC → composite cost → evidence for multiple criteria`

**Maroger et al. (2022)**

`Human locomotion → IOC → predefined locomotion cost → human-like trajectory generation`

**Liu et al. (2022)**

`Human + wearable robot → IRL / IOC → human-robot performance objective → stability/robustness analysis`

Therefore, the literature has already established that inverse methods can infer objectives from both:

- human movement,
- and human-robot locomotion behavior.

The remaining question for our project is not simply:

> Can we infer an objective?

but potentially:

> Can an objective inferred from human demonstrations be represented and validated in a way that remains useful when optimized by a different humanoid with different dynamics and physical constraints?

**This remains a candidate research direction, not an established research gap.**

---

### 15. Overall Role in Our Project

**Important prior-art paper.**

Liu et al. (2022) is important because it extends objective inference beyond purely human motion to **human-robot locomotion** and demonstrates both IRL- and IOC-based approaches.

Its most important consequence for our project is that it further narrows the novelty space.

We cannot claim novelty based only on:

- learning locomotion objectives,
- using IRL,
- using IOC,
- learning quadratic cost weights,
- or inferring objectives from human-robot locomotion.

The potentially more distinctive problem is the transition from:

`Human Demonstrations`

to:

`Generalizable Objective`

to:

`Independent Humanoid Dynamics + Constraints`

to:

`Model-Based MPC`

But:

> **Not Established Yet.**

**Status:** Required





## Paper 7 — Wu et al. (2023 / ICRA 2024)

**Citation**  
Wu, F., Gu, Z., Wu, H., Wu, A., & Zhao, Y. (2023). *Infer and Adapt: Bipedal Locomotion Reward Learning from Demonstrations via Inverse Reinforcement Learning*. arXiv:2309.16074. Published in IEEE International Conference on Robotics and Automation (ICRA), 2024, pp. 16243–16250.

**Literature Category**  
Inverse Reinforcement Learning (IRL) / Bipedal Locomotion / Reward Learning / Learning from Demonstrations / Generalization

---

### 1. Research Problem

The paper investigates whether a bipedal robot can learn locomotion behavior from expert demonstrations by first inferring the underlying reward function rather than directly imitating the expert policy.

The motivation is that imitation learning learns how the expert behaves, while inverse reinforcement learning attempts to learn what objective may have produced that behavior.

The central idea is:

`Expert Demonstrations`

`→ Inverse Reinforcement Learning`

`→ Learned Reward Function`

`→ Robot Policy Learning`

The paper focuses on bipedal locomotion over complex and uneven terrains.

---

### 2. Input

The input consists of expert demonstrations of bipedal locomotion.

The demonstrations contain locomotion behavior that can be used by the inverse reinforcement learning algorithm to infer a reward function.

The learned reward is then used to train a locomotion policy.

Therefore:

- Expert demonstrations: ✓
- Bipedal locomotion: ✓
- Locomotion reward learning: ✓
- IRL: ✓
- Human motion demonstrations: Not necessarily
- Full human biomechanical demonstrations: No
- H1-specific human transfer: No
- Whole-body humanoid MPC: No

An important distinction is that the paper addresses **expert bipedal locomotion demonstrations**, not the specific problem of recovering a human's internal biological objective from human motion.

---

### 3. Method

The paper applies inverse reinforcement learning to bipedal locomotion.

The conceptual pipeline is:

`Expert Demonstrations`

`↓`

`Inverse Reinforcement Learning`

`↓`

`Learned Reward Function`

`↓`

`Reinforcement Learning`

`↓`

`Bipedal Locomotion Policy`

The key idea is to avoid directly reproducing the demonstrated trajectory or policy.

Instead, the method attempts to recover a reward function that explains the demonstrated behavior.

The paper investigates IRL methods using nonlinear function approximation for learning the expert reward.

---

### 4. Objective / Reward

Unlike approaches that simply assign manually designed weights to a small set of predefined costs, this work uses nonlinear function approximation to represent the learned reward.

Conceptually:

`State`

`↓`

`Nonlinear Reward Function`

`↓`

`Reward`

The reward function is then analyzed to understand which locomotion-related behaviors are encoded in the learned reward.

This allows the researchers to investigate the structure of the learned reward and extract insights about the expert locomotion strategy.

However, the learned reward should not automatically be interpreted as the true internal objective of the expert.

It is an inferred reward that explains the observed behavior under the selected IRL formulation and representation.

---

### 5. Validation

The learned reward functions are evaluated by training bipedal locomotion policies using the inferred rewards.

The resulting policies are tested on terrains that were not present in the demonstrations.

The paper reports that policies trained using inferred rewards demonstrate improved walking performance on unseen terrains.

This is an important result because it suggests that learning the underlying reward can provide better adaptability than simply reproducing the demonstrated behavior.

The key experimental idea is:

`Training / Demonstration Terrains`

`↓`

`Learn Reward`

`↓`

`Train Locomotion Policy`

`↓`

`Test on Unseen Terrains`

---

### 6. Main Finding

The main finding is:

> Inverse reinforcement learning can be used to infer reward functions from bipedal locomotion demonstrations, and policies trained with the inferred rewards can improve adaptability to unseen terrains.

The paper therefore provides evidence that learning a reward/objective rather than directly imitating behavior can help with locomotion generalization.

The learned reward also provides an interpretable object that can be analyzed to understand aspects of the expert's locomotion strategy.

---

### 7. Important Interpretation

The important conceptual contribution is the separation between:

`Demonstrated Behavior`

and:

`Underlying Reward`

Instead of learning:

`Demonstration → Copy the motion`

the paper investigates:

`Demonstration → Infer Reward → Learn New Behavior`

This is highly relevant to our project because our project also aims to avoid direct trajectory imitation.

However, the paper does not establish that the learned reward is a universal human locomotion objective.

It establishes that an inferred reward can be useful for learning and generalizing bipedal locomotion behavior.

---

### 8. Limitations

#### 8.1 Not a direct human-objective study

The paper focuses on expert bipedal locomotion demonstrations.

Therefore, it does not directly establish that the learned reward represents a biological or cognitive human locomotion objective.

This distinction is important for our project, which specifically starts from human demonstrations.

---

#### 8.2 Reward identifiability

Different reward functions can potentially produce similar behavior.

Therefore:

`Observed Behavior → One Unique True Reward`

cannot automatically be assumed.

The learned reward should be interpreted as an objective that explains the demonstrated behavior under the chosen model and learning framework.

---

#### 8.3 Dependence on reward representation

Although nonlinear function approximation provides more flexibility than a simple weighted sum of manually selected features, the learned reward is still constrained by the chosen model, state representation, and IRL formulation.

Therefore, the paper does not establish that the learned reward is the unique or complete representation of the expert's locomotion objective.

---

#### 8.4 No human-to-humanoid morphology transfer

The paper does not demonstrate:

`Human`

`↓`

`Learned Human Objective`

`↓`

`Different Humanoid Morphology`

There is no direct transfer of a human objective to the Unitree H1.

---

#### 8.5 No model-based MPC integration

The learned reward is used to train locomotion policies through reinforcement learning.

The paper does not demonstrate the specific pipeline:

`Learned Human Objective`

`+ H1 Dynamics`

`+ H1 Constraints`

`→ Model-Based MPC`

Therefore, the model-based control component proposed in our project remains outside the scope of this work.

---

#### 8.6 No explicit dynamics-transfer study

Although the learned reward improves performance on unseen terrains, this is not the same as transferring the objective across substantially different robot dynamics.

Terrain generalization:

`Same Robot + New Terrain`

is different from dynamics/morphology generalization:

`Human → Different Robot`

This distinction is critical for our project.

---

### 9. Relevance to Our Project

**Relevance: Very High.**

This is one of the most directly relevant papers in our current literature review because it combines:

- demonstrations,
- inverse reinforcement learning,
- bipedal locomotion,
- learned reward functions,
- and generalization to unseen environments.

It provides strong prior art for the idea:

`Demonstrations → Learned Locomotion Reward → New Behavior`

Therefore, our project cannot claim novelty simply from learning a locomotion reward from demonstrations.

However, the paper does not perform the complete target pipeline of our project:

`Human Demonstrations`

`→ Human Objective`

`→ Different Humanoid Dynamics`

`→ H1 Constraints`

`→ Model-Based MPC`

This distinction remains potentially important.

---

### 10. Research Gap Contribution

This paper eliminates another broad novelty claim:

> "We learn a locomotion reward from demonstrations and use it to improve generalization."

This has already been demonstrated.

It also shows that reward learning can provide useful generalization to unseen terrains.

Therefore, the novelty of our project should not simply be:

- applying IRL to locomotion,
- learning a reward from demonstrations,
- or testing on unseen terrain.

Potentially more distinctive directions include:

1. Learning an objective specifically from human locomotion.
2. Separating the human objective from the dynamics and morphology of the demonstrator.
3. Transferring the learned objective to a different humanoid morphology.
4. Optimizing the learned objective under the target robot's own dynamics.
5. Explicitly enforcing humanoid physical constraints.
6. Using the learned objective inside model-based MPC rather than only policy learning.
7. Evaluating generalization across dynamics, morphology, and physical constraints rather than only terrain.

However:

> **Whether these differences constitute a genuine research gap is NOT ESTABLISHED YET.**

Further literature review is required.

---

### 11. Direct Implications for Our Project

#### Rule 1 — Reward learning from demonstrations is established

We cannot claim:

`Demonstrations → IRL → Locomotion Reward`

as the primary novelty.

---

#### Rule 2 — Generalization to unseen terrain is also established

Testing whether a learned reward improves performance on unseen terrain is valuable, but it is not sufficient novelty by itself.

---

#### Rule 3 — Human objective remains a different question

The paper demonstrates learning an expert locomotion reward.

It does not establish that this reward is the underlying human objective.

Therefore our project must distinguish:

`Expert locomotion reward`

from:

`Latent human objective`

---

#### Rule 4 — Dynamics transfer remains important

The paper demonstrates environment/terrain generalization.

Our project is interested in a harder form of generalization:

`Human dynamics`

`→`

`H1 dynamics`

This is not the same problem.

---

#### Rule 5 — Model-based control remains a major distinction

The paper primarily uses the learned reward to train locomotion policies.

Our project aims to use the learned objective with:

`H1 Dynamics + Physical Constraints + MPC`

This difference is directly connected to the model-based direction suggested by Dennis Hong.

---

### 12. Position in Our Literature Review

| Question | Wu et al. (2023/2024) |
|---|---|
| Demonstrations used? | Yes |
| Bipedal locomotion? | Yes |
| IRL used? | Yes |
| Reward learned from demonstrations? | Yes |
| Nonlinear reward representation? | Yes |
| Reward analyzed? | Yes |
| Human demonstrations specifically? | Not established as the central setting |
| Human biological objective? | No |
| Predefined simple weighted cost only? | No |
| Generalization to unseen terrain? | Yes |
| Different robot morphology? | No |
| Human → humanoid transfer? | No |
| H1 dynamics? | No |
| H1 physical constraints? | No |
| Model-based MPC? | No |
| Whole-body MPC? | No |
| Objective transfer across dynamics? | No |
| Direct trajectory imitation? | No; reward learning is used instead |
| Learned reward used for new behavior? | Yes |

---

### 13. Comparison With Previous Papers

The literature progression is now:

**Berret et al. (2011)**

`Human arm motion → IOC → composite cost`

**Maroger et al. (2022)**

`Human locomotion → IOC → predefined locomotion cost`

**Liu et al. (2022)**

`Human + wearable robot → IRL/IOC → human-robot performance objective`

**Wu et al. (2023/2024)**

`Bipedal demonstrations → IRL → nonlinear learned reward → policy learning → unseen-terrain generalization`

This progression is important because the literature increasingly approaches our target idea.

The key remaining distinction is potentially:

`Human Demonstration`

`→ Latent Human Objective`

`→ Transfer across morphology/dynamics`

`→ Model-Based H1 Control`

However:

> **Research gap: NOT ESTABLISHED YET.**

---

### 14. Overall Role in Our Project

**Required — Very High Relevance**

This paper is a major prior-art reference for Phase 4 because it demonstrates that:

> Learning a locomotion reward from demonstrations can be more useful for generalization than directly reproducing demonstrated behavior.

It also demonstrates that the learned reward can be analyzed to obtain insight into locomotion strategies.

Most importantly, it prevents us from claiming novelty for:

`IRL + bipedal locomotion + demonstrations + unseen terrain`

as a standalone contribution.

Our potential contribution must therefore be more specific, particularly around:

`Human Objective`

`+`

`Different Robot Dynamics / Morphology`

`+`

`Model-Based MPC`

`+`

`Physical Constraints`

**Status:** Required




## Paper 8 — Bečanović, Jovanović & Bonnet (2024 / 2025)

**Citation**  
Bečanović, F., Jovanović, K., & Bonnet, V. (2024). *Reliability of Single-Level Equality-Constrained Inverse Optimal Control*. IEEE-RAS 23rd International Conference on Humanoid Robots (Humanoids), pp. 623–630. arXiv preprint: arXiv:2510.08406, 2025.

**Literature Category**  
Inverse Optimal Control (IOC) / Computational Efficiency / Robustness / Optimal Control / Human Motion

---

### 1. Research Problem

A major computational difficulty in Inverse Optimal Control is that the classical IOC formulation is naturally a bilevel optimization problem.

The inner problem solves the optimal-control problem associated with a candidate human objective.

The outer problem changes the objective parameters so that the resulting optimal trajectory matches the observed human motion.

Conceptually:

    Candidate Objective
          ↓
    Optimal Control
          ↓
    Predicted Motion
          ↓
    Compare with Human Motion
          ↓
    Update Objective
          ↓
    Repeat

This can be computationally expensive because the optimal-control problem must be solved repeatedly.

The paper investigates whether IOC can instead be reformulated as a **single-level optimization problem** that is both computationally efficient and robust to noisy motion data.

---

### 2. Input

The input is a modeled motion-generation problem together with observed motion data.

The experiments use a human-like planar reaching task with a 2-DoF model.

The observed trajectories are corrupted with different levels of noise to evaluate the robustness of the IOC method.

Therefore:

- Motion demonstrations: ✓
- Human-like motion: ✓
- IOC: ✓
- Noise robustness: ✓
- Human locomotion: ✗
- Whole-body humanoid: ✗
- H1: ✗
- Morphology transfer: ✗

---

### 3. Method

The classical bilevel IOC problem is reformulated into a **single-level optimization problem**.

The basic idea is to replace the repeated inner optimal-control solve with constraints related to the optimality conditions of the underlying control problem.

Conceptually:

**Classical IOC**

    Outer optimization
          ↓
    Inner optimal control
          ↓
    Predicted trajectory

**Proposed approach**

    Single optimization problem
          ↓
    Optimality conditions
          +
    Motion matching
          ↓
    Objective parameters

The purpose is to obtain the same or equivalent behavioral parameters without repeatedly solving the complete inner optimal-control problem.

---

### 4. Objective / Cost

The paper does not propose a new universal human objective.

Instead, it assumes an objective represented using candidate basis functions:

    J = Σ θᵢ φᵢ

where:

- φᵢ represents a candidate objective component.
- θᵢ represents its behavioral weight.

The IOC method estimates the parameters θ from observed motion.

Therefore:

    Predefined Objective Representation
              ↓
         Learn Parameters

This is important for our project.

The paper improves **how efficiently the parameters can be inferred**, but it does not solve the broader problem of discovering an entirely unknown objective representation.

---

### 5. Validation

The method is evaluated using a simulated 2-DoF planar reaching problem.

The experiments introduce different levels of noise into the observed trajectories and compare the proposed single-level IOC formulation with a classical bilevel IOC formulation.

The paper reports that the proposed method remains robust to substantial noise and reduces computation time by approximately a factor of 15 compared with the classical bilevel implementation for the tested task.

---

### 6. Main Finding

The main finding is:

> A carefully formulated single-level IOC problem can provide substantially better computational efficiency than classical bilevel IOC while maintaining robustness to noisy motion observations.

This is important because IOC can otherwise become computationally expensive when the underlying motion-generation problem must be solved repeatedly.

---

### 7. Simple Interpretation

Suppose we want to discover whether a human values:

    70% smoothness
    30% effort

A classical IOC method may repeatedly do:

    Guess weights
        ↓
    Solve optimal control
        ↓
    Compare with human
        ↓
    Change weights
        ↓
    Solve again

The proposed method reformulates the problem so that the optimization can be solved more directly.

Therefore, the contribution is primarily:

    Faster / more robust IOC

rather than:

    Discovery of a new human objective.

---

### 8. Limitations

#### 8.1 Equality constraints

The proposed formulation is developed for equality-constrained optimal-control models.

Inequality constraints such as control limits and path constraints are not handled in the main formulation because they introduce additional mathematical difficulties.

This is important for humanoid robotics because realistic humanoid control contains many inequality constraints.

---

#### 8.2 Simplified motion model

The validation uses a 2-DoF planar reaching model.

It does not demonstrate the method on:

- whole-body human locomotion,
- humanoid walking,
- foot-ground contact,
- whole-body dynamics,
- humanoid torque limits,
- friction constraints,
- or Unitree H1 dynamics.

---

#### 8.3 No morphology transfer

The paper does not investigate:

    Human Motion
          ↓
    Learned Objective
          ↓
    Different Humanoid

Therefore, it does not address whether an inferred objective can remain meaningful when optimized under different robot morphology and dynamics.

---

#### 8.4 No model-based humanoid MPC

The learned behavioral parameters are not demonstrated as the objective of a whole-body humanoid MPC system.

Therefore, the complete pipeline:

    Human Objective
          +
    H1 Dynamics
          +
    H1 Constraints
          ↓
         MPC

is not established by this work.

---

#### 8.5 Objective representation remains predefined

The method estimates parameters of candidate objective functions.

It does not establish that the true underlying human objective can be uniquely discovered from arbitrary motion data.

Therefore:

    Efficient parameter inference
          ≠
    Complete discovery of human objective

---

#### 8.6 Validation is simulation-based

The primary validation is performed on a simulated planar reaching problem rather than a full real-world human locomotion dataset.

Therefore, robustness on the tested reaching task should not automatically be generalized to humanoid locomotion.

---

### 9. Relevance to Our Project

**Relevance: High for methodology, moderate for the research question.**

The paper is relevant because our project must eventually solve an IOC/IRL-type inverse problem from human demonstrations.

A computationally efficient IOC formulation could be useful during Phase 4.

However, the paper does not answer our central scientific question:

> What objective underlies human locomotion, and can that objective transfer to a humanoid with different dynamics and constraints?

Instead, it addresses:

> How can a particular IOC problem be solved more efficiently and robustly?

Therefore, this paper should influence our **method selection**, but should not define our research question.

---

### 10. Research Gap Contribution

This paper eliminates another possible assumption:

> "IOC is inherently too computationally expensive to be useful."

The results show that suitable single-level formulations can significantly reduce computational cost.

However, it does not eliminate the broader research gap potentially relevant to our project.

The following remains unresolved by this paper:

    Human locomotion
          ↓
    Generalizable objective
          ↓
    Different humanoid dynamics
          ↓
    Physical constraints
          ↓
    Model-based MPC

Whether this constitutes a genuine research gap is:

**NOT ESTABLISHED YET.**

---

### 11. Direct Implications for Our Project

#### Rule 1 — Computational efficiency matters

If IOC is used for our human-motion dataset, the computational cost of the inverse problem must be considered from the beginning.

---

#### Rule 2 — Do not assume single-level IOC automatically solves H1

The proposed method has not been demonstrated for the full constrained dynamics of a humanoid such as H1.

---

#### Rule 3 — Separate objective learning from objective representation

The method can efficiently estimate parameters of a chosen objective representation.

This does not mean that it discovers the correct objective representation automatically.

---

#### Rule 4 — Constraints are a major unresolved issue for our target system

The H1 control problem contains important inequality constraints.

Therefore, if our final system uses IOC for objective learning and MPC for control, the compatibility between the learned objective, IOC formulation, and constrained H1 dynamics must be explicitly investigated.

---

### 12. Position in Our Literature Review

| Question | Bečanović et al. |
|---|---|
| IOC? | Yes |
| Human-like motion? | Yes |
| Single-level IOC? | Yes |
| Computational efficiency? | Major contribution |
| Noise robustness? | Major contribution |
| Objective parameters inferred? | Yes |
| Objective representation discovered from scratch? | No |
| Human locomotion? | No |
| Bipedal locomotion? | No |
| Humanoid dynamics? | No |
| H1 dynamics? | No |
| Morphology transfer? | No |
| Inequality-constrained humanoid control? | No |
| MPC integration? | No |
| Generalization across morphology/dynamics? | No |

---

### 13. Overall Role in Our Project

**Required — Methodological Reference**

This paper is important for understanding how the IOC component of our project could potentially be made computationally practical.

Its main contribution is not a new human locomotion objective, but a more efficient and noise-robust way to solve a class of IOC problems.

It therefore belongs in our literature review as a **methodological IOC paper** rather than as direct evidence for the final human-locomotion research gap.

**Status:** Required
