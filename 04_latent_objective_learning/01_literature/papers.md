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

### Mombaur, Truong & Laumond (2010)

**Citation**
Mombaur, K., Truong, A., & Laumond, J.-P. (2010). *From Human to Humanoid Locomotion—An Inverse Optimal Control Approach*. Autonomous Robots, 28(3), 369–383. DOI: 10.1007/s10514-009-9170-7.

**Research Problem**
Infer an underlying locomotion objective from observed human motion and use the inferred objective to generate humanoid locomotion, rather than directly reproducing human trajectories.

**Input**
Human motion-capture demonstrations of planar locomotion toward different target configurations. The motion representation focuses on the global position and orientation of the body rather than full-body joint trajectories.

**Method**
The authors formulate an inverse optimal control problem in which the locomotion cost is represented as a weighted combination of manually selected basis functions. The weights are inferred by repeatedly solving a forward optimal control problem and comparing the resulting trajectory with human demonstrations.

**Objective / Cost**
The final objective combines:

* locomotion time,
* squared forward acceleration,
* squared rotational acceleration,
* squared orthogonal acceleration,
* alignment between body orientation and the direction toward the target.

The objective representation is manually specified; IOC learns the corresponding weights rather than discovering the objective representation itself.

**Validation**
The objective is learned from multiple human demonstrations across different target scenarios and evaluated on additional held-out scenarios. The learned objective is able to reproduce characteristic human locomotion paths and generalize to unseen target configurations. The approach is also demonstrated in a human-to-humanoid transfer setting.

**Main Finding**
A shared locomotion objective can explain multiple human locomotion demonstrations and can be optimized to generate new trajectories rather than directly imitating observed trajectories.

**Limitation**

* The objective basis functions are manually designed rather than learned.
* The locomotion model is simplified and does not capture full-body humanoid dynamics or contact-rich whole-body behavior.
* The inferred objective is task-specific and does not establish a general latent representation of human objectives.
* Transfer to humanoid motion relies on additional robot-specific motion-generation mechanisms.
* Robustness to disturbances, changes in dynamics, and substantially different robot constraints is not systematically studied.
* Objective identifiability remains limited because different cost formulations may produce similar observed trajectories.

**Relevance to Our Project**
**Very High.** This work is a direct predecessor of the Human Demonstrations → Objective Inference → Humanoid Motion pipeline proposed in our project. It establishes that human locomotion objectives can be inferred through IOC and subsequently used for motion generation.

However, it also shows that **Human → IOC → Humanoid** alone is not a sufficient novelty claim. Our project must investigate whether a richer or learned objective representation can generalize under the different dynamics and physical constraints of the Unitree H1 and be directly integrated with model-based MPC.

**Research Gap Contribution**
This paper establishes the following prior art:

> Human locomotion demonstrations can be used to infer a shared objective and generate humanoid locomotion through inverse optimal control.

A preliminary distinction relevant to our project is:

> **Mombaur et al. learn objective parameters within a manually specified cost representation; they do not learn a latent objective representation itself.**

Potential gaps concerning learned objective representations, morphology/dynamics transfer, constraint-aware MPC integration, and generalization remain **Not established yet** and must be evaluated against subsequent IOC, IRL, locomotion, and model-based control literature.


### Mombaur, Truong & Laumond (2010)

**Citation**
Mombaur, K., Truong, A., & Laumond, J.-P. (2010). *From Human to Humanoid Locomotion—An Inverse Optimal Control Approach*. Autonomous Robots, 28(3), 369–383. DOI: 10.1007/s10514-009-9170-7.

**Research Problem**
Infer an underlying locomotion objective from observed human motion and use the inferred objective to generate humanoid locomotion, rather than directly reproducing human trajectories.

**Input**
Human motion-capture demonstrations of planar locomotion toward different target configurations. The motion representation focuses on the global position and orientation of the body rather than full-body joint trajectories.

**Method**
The authors formulate an inverse optimal control problem in which the locomotion cost is represented as a weighted combination of manually selected basis functions. The weights are inferred by repeatedly solving a forward optimal control problem and comparing the resulting trajectory with human demonstrations.

**Objective / Cost**
The final objective combines:

* locomotion time,
* squared forward acceleration,
* squared rotational acceleration,
* squared orthogonal acceleration,
* alignment between body orientation and the direction toward the target.

The objective representation is manually specified; IOC learns the corresponding weights rather than discovering the objective representation itself.

**Validation**
The objective is learned from multiple human demonstrations across different target scenarios and evaluated on additional held-out scenarios. The learned objective is able to reproduce characteristic human locomotion paths and generalize to unseen target configurations. The approach is also demonstrated in a human-to-humanoid transfer setting.

**Main Finding**
A shared locomotion objective can explain multiple human locomotion demonstrations and can be optimized to generate new trajectories rather than directly imitating observed trajectories.

**Limitation**

* The objective basis functions are manually designed rather than learned.
* The locomotion model is simplified and does not capture full-body humanoid dynamics or contact-rich whole-body behavior.
* The inferred objective is task-specific and does not establish a general latent representation of human objectives.
* Transfer to humanoid motion relies on additional robot-specific motion-generation mechanisms.
* Robustness to disturbances, changes in dynamics, and substantially different robot constraints is not systematically studied.
* Objective identifiability remains limited because different cost formulations may produce similar observed trajectories.

**Relevance to Our Project**
**Very High.** This work is a direct predecessor of the Human Demonstrations → Objective Inference → Humanoid Motion pipeline proposed in our project. It establishes that human locomotion objectives can be inferred through IOC and subsequently used for motion generation.

However, it also shows that **Human → IOC → Humanoid** alone is not a sufficient novelty claim. Our project must investigate whether a richer or learned objective representation can generalize under the different dynamics and physical constraints of the Unitree H1 and be directly integrated with model-based MPC.

**Research Gap Contribution**
This paper establishes the following prior art:

> Human locomotion demonstrations can be used to infer a shared objective and generate humanoid locomotion through inverse optimal control.

A preliminary distinction relevant to our project is:

> **Mombaur et al. learn objective parameters within a manually specified cost representation; they do not learn a latent objective representation itself.**

Potential gaps concerning learned objective representations, morphology/dynamics transfer, constraint-aware MPC integration, and generalization remain **Not established yet** and must be evaluated against subsequent IOC, IRL, locomotion, and model-based control literature.

