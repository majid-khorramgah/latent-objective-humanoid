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

