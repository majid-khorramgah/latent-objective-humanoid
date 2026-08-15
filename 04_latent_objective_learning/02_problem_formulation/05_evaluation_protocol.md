# Evaluation Protocol

## 1. Purpose

The purpose of this document is to define how the proposed human
objective inference method will be evaluated.

The evaluation must determine whether the learned objective:

1. explains human demonstrations,
2. generalizes to unseen human motions,
3. is different from simply memorizing trajectories,
4. remains meaningful under changes in motion and context,
5. can eventually be transferred to a different humanoid system.

The evaluation protocol is therefore designed around the central
research question:

> Can an objective inferred from human demonstrations capture
> transferable behavioral preferences rather than merely reproducing
> observed human trajectories?

---

# 2. Core Evaluation Principle

The project does NOT aim to maximize similarity between a human
trajectory and a robot trajectory.

Instead, the intended chain is:

    Human Demonstrations
            ↓
    Infer Human Objective
            ↓
    Evaluate Objective
            ↓
    Transfer to Robot
            ↓
    Robot optimizes objective

Therefore, trajectory imitation error alone is not a sufficient
evaluation criterion.

The evaluation must distinguish between:

    Trajectory Memorization

and:

    Objective Generalization

---

# 3. Evaluation Stages

The evaluation will be divided into four stages.

    Stage 1
    Synthetic Validation

        ↓

    Stage 2
    Human Demonstration Validation

        ↓

    Stage 3
    Held-Out Human Evaluation

        ↓

    Stage 4
    Robot Transfer Evaluation

The first three stages can be performed without a physical robot.

Robot transfer is evaluated later using simulation.

---

# 4. Stage 1 — Synthetic Validation

Before using human data, the objective inference method should be
validated on controlled synthetic problems.

The purpose is to determine whether the inference algorithm can
recover a known objective when the ground truth is available.

Conceptually:

    Known Objective
          ↓
    Generate Demonstrations
          ↓
    Objective Inference
          ↓
    Recovered Objective
          ↓
    Compare with Ground Truth

For example:

    J_true = w1 φ1 + w2 φ2 + w3 φ3

Synthetic demonstrations can be generated from this objective.

The inference method then attempts to recover:

    w1, w2, w3

---

# 5. Synthetic Evaluation Metrics

The following metrics may be used.

## Parameter Recovery

Compare inferred objective parameters with the known ground truth.

For example:

    ||w_learned - w_true||

A smaller value indicates better parameter recovery.

However, parameter distance alone may not be sufficient because
different parameterizations can sometimes produce similar behavior.

---

## Objective Ranking Agreement

Compare how the learned objective ranks candidate trajectories
relative to the ground-truth objective.

For candidate trajectories:

    τ1, τ2, ..., τN

compare:

    J_true(τ)

with:

    J_learned(τ)

The goal is to determine whether both objectives prefer similar
behaviors.

Possible measures include:

- Rank correlation
- Pairwise preference accuracy
- Spearman correlation

---

## Behavior Recovery

Optimize the learned objective and compare the resulting behavior
with behavior generated using the true objective.

The purpose is to determine whether:

    Learned Objective
          ↓
       Optimization
          ↓
       Similar Behavior

to:

    True Objective
          ↓
       Optimization
          ↓
       Ground-Truth Behavior

---

# 6. Stage 2 — Human Demonstration Validation

After synthetic validation, the method is evaluated using AMASS
human motion data.

The goal is not simply to reconstruct the training trajectories.

Instead, the learned objective should explain meaningful properties
of human locomotion.

The basic pipeline is:

    AMASS
      ↓
    Human Motion Representation
      ↓
    Candidate Features
      ↓
    Objective Inference
      ↓
    Learned Human Objective

The learned objective is then evaluated against the observed
demonstrations.

---

# 7. Demonstration Reconstruction Test

The learned objective should be able to explain the demonstrations
from which it was inferred.

Given:

    Demonstration τ_h

and learned objective:

    J_learned

we evaluate whether τ_h receives a relatively low cost compared
with alternative candidate motions.

The test is therefore:

    Human Demonstration
            vs.
    Alternative Motions

The learned objective should prefer the human demonstration when the
alternative motions violate the inferred behavioral preferences.

---

# 8. Perturbation Test

A stronger test is to create controlled perturbations of human
motion.

For example:

    Human Motion
         ↓
    Small Perturbation
         ↓
    Alternative Motion

Possible perturbations include:

- Modified joint trajectories
- Altered timing
- Modified foot placement
- Increased acceleration
- Reduced stability
- Modified walking speed

The learned objective should assign different costs to these
perturbations according to the behavioral preferences inferred from
the demonstrations.

This tests whether the objective captures meaningful structure
rather than merely assigning similar scores to all motions.

---

# 9. Ablation of Objective Components

Candidate objective components should be evaluated individually
and in combination.

For example:

    Task only

    Task + Stability

    Task + Efficiency

    Task + Motion Quality

    Full Candidate Objective

The purpose is not to assume that the full objective is correct.

Instead, we determine experimentally which components contribute
to explaining human motion.

This also prevents unnecessary complexity.

---

# 10. Held-Out Human Evaluation

The most important evaluation is performed on demonstrations that
were NOT used during objective inference.

The dataset should be divided into:

    Training Demonstrations
            ↓
    Objective Inference

and:

    Held-Out Demonstrations
            ↓
    Evaluation

The learned objective must be evaluated on the held-out data.

This tests whether the objective generalizes beyond the trajectories
used for learning.

---

# 11. Subject-Level Generalization

Where sufficient data is available, demonstrations should be
separated by subject.

For example:

    Subjects 1...N-1
          ↓
    Objective Learning

    Subject N
          ↓
    Held-Out Evaluation

This tests whether the learned objective captures shared movement
preferences rather than individual trajectory patterns.

Subject-level generalization is particularly important because
different people may perform the same locomotion task differently.

---

# 12. Sequence-Level Generalization

A second split should be performed at the motion-sequence level.

For example:

    Training Sequences
          ↓
    Objective Learning

    Unseen Sequences
          ↓
    Evaluation

This determines whether the objective generalizes to new motion
instances.

---

# 13. Context Generalization

If the available data supports different locomotion conditions,
evaluation can also be performed across contexts.

For example:

    Context A
        ↓
    Objective Learning

    Context B
        ↓
    Evaluation

The purpose is to determine whether the objective is:

    Context-independent

or:

    Context-dependent

This should be treated as an experimental question rather than an
assumption.

---

# 14. Objective Generalization vs. Trajectory Generalization

A central distinction in this project is:

### Trajectory Generalization

Can a model predict or reconstruct unseen human trajectories?

versus:

### Objective Generalization

Can the inferred objective correctly evaluate or rank unseen
movements?

The second question is more important for this project.

A model may fail to reconstruct the exact human trajectory while still
correctly capturing the behavioral objective.

Therefore:

    Low trajectory error
        ≠
    Correct human objective

and:

    Different trajectory
        +
    Similar objective preference
        =
    Potentially successful transfer

---

# 15. Baselines

The proposed method should be compared with simpler alternatives.

Possible baselines include:

### Baseline 1 — Hand-Designed Objective

Use predefined objective weights.

Example:

    J = Energy + Stability + Smoothness

This establishes how much is gained by learning the objective.

---

### Baseline 2 — Single-Criterion Objective

Evaluate individual criteria separately.

Examples:

    Energy only

    Stability only

    Smoothness only

    Task objective only

This determines whether a single criterion is sufficient.

---

### Baseline 3 — Direct Motion Matching

Use trajectory imitation or motion tracking as the baseline.

This represents the conventional approach:

    Human Trajectory
          ↓
    Robot Motion Matching

It provides an important comparison against objective-based transfer.

---

### Baseline 4 — Learned Objective

The proposed approach:

    Human Demonstrations
          ↓
    Objective Inference
          ↓
    Learned Objective

The comparison should determine whether the learned objective
provides better generalization than predefined or trajectory-based
approaches.

---

# 16. Primary Evaluation Metrics

The exact metrics will be finalized after the objective representation
and inference method are defined.

Candidate metrics include:

### Objective Ranking Accuracy

How accurately does the learned objective rank preferred versus
non-preferred motions?

---

### Pairwise Preference Accuracy

Given two candidate trajectories:

    τA
    τB

can the learned objective correctly predict which one is preferred
by the demonstration-derived objective?

---

### Held-Out Prediction Performance

How well does the learned objective explain demonstrations that were
not used during training?

---

### Objective Stability

Does the inferred objective remain stable when:

- Demonstrations change?
- Subjects change?
- Sequences change?
- Small perturbations are introduced?

---

### Behavioral Recovery

When the learned objective is optimized, does it produce behavior
consistent with the preferences observed in human demonstrations?

---

# 17. Transfer Evaluation

The final research objective is not complete until the learned
objective can be tested on a different embodiment.

The eventual transfer experiment is:

    Human Demonstrations
            ↓
    Human Objective
            ↓
    H1-Compatible Objective
            ↓
    H1 Dynamics + Constraints
            ↓
           MPC
            ↓
       H1 Behavior

The H1 should NOT be required to reproduce the human trajectory.

Instead, the H1 should optimize the transferred objective using its
own dynamics and physical constraints.

---

# 18. Transfer Success Criteria

A successful transfer should demonstrate that:

1. The objective remains mathematically meaningful on H1.
2. The H1 can optimize the objective.
3. The resulting behavior satisfies the intended task.
4. The robot does not need to reproduce human joint trajectories.
5. The behavior remains meaningful under changes in robot dynamics
   or physical constraints.

Transfer performance will therefore be evaluated using both:

- Task-level metrics
- Objective-related metrics

---

# 19. Generalization Tests

The following generalization dimensions should be considered.

### Unseen Human Sequences

    Train → Seen subjects / sequences
    Test  → Unseen sequences

### Unseen Subjects

    Train → Subjects A...N-1
    Test  → Subject N

### Unseen Conditions

    Train → Condition A
    Test  → Condition B

### Different Robot Dynamics

    Human
      ↓
    H1

The last case is the most important for the final research claim.

---

# 20. What Would Count as Failure?

The project should explicitly define failure conditions.

The approach would be considered unsuccessful if:

- The learned objective only memorizes training trajectories.
- It performs poorly on held-out demonstrations.
- It cannot distinguish meaningful motion perturbations.
- It is highly unstable across demonstrations.
- It provides no advantage over simple predefined objectives.
- It cannot be expressed in a form usable by H1.
- H1 optimization produces physically invalid or meaningless behavior.
- Generalization disappears when robot dynamics change.

Negative results are scientifically useful because they reveal where
the proposed objective-transfer hypothesis breaks down.

---

# 21. Evaluation Order

The experiments should follow the smallest-to-largest progression:

    1. Synthetic Validation
             ↓
    2. Human Demonstration Validation
             ↓
    3. Held-Out Human Evaluation
             ↓
    4. Baseline Comparison
             ↓
    5. H1 Transfer
             ↓
    6. Generalization Tests

This order avoids spending significant computational effort on H1
control before verifying that the objective inference itself works.

---

# 22. Computational Principle

The initial evaluation should be performed entirely in simulation
and offline using existing human motion data.

No physical robot is required.

The early stages require:

- AMASS
- SMPL-X
- Python
- Numerical optimization / learning tools

Isaac Lab becomes important when the learned objective is transferred
to the H1.

Therefore:

    Human Objective Learning
            ↓
       Offline / CPU-GPU
            ↓
    Validate Objective
            ↓
       Isaac Lab
            ↓
    H1 Transfer

---

# 23. Experimental Discipline

To avoid overfitting and circular evaluation:

- Training and evaluation demonstrations must be separated.
- Test sequences must not influence objective inference.
- Test subjects should remain isolated where possible.
- Evaluation metrics should be defined before final experiments.
- Baselines should use comparable information.
- Hyperparameter tuning should not use the final test set.
- Results should be reported across multiple demonstrations where
  possible.

---

# 24. Minimum Viable Evaluation

The first experimental version does NOT need to implement every
possible evaluation.

The minimum useful evaluation is:

    Synthetic Ground Truth
            ↓
    Objective Recovery

    +

    Human Demonstrations
            ↓
    Objective Inference
            ↓
    Held-Out Human Sequences
            ↓
    Objective Ranking / Preference Test

If this stage fails, there is no reason to immediately proceed to
complex H1 transfer experiments.

---

# 25. Final Evaluation Question

The complete evaluation should ultimately answer:

> Does the inferred objective capture a behavioral principle that
> generalizes beyond the demonstrations used to learn it and remains
> meaningful when optimized by a humanoid robot with different
> morphology and dynamics?

This is the central criterion for evaluating the proposed research
direction.

---

# Status

Evaluation protocol:

**Defined at the preliminary level**

Synthetic validation:

**Required**

Human held-out evaluation:

**Required**

Baseline comparison:

**Required**

H1 transfer:

**Future experimental stage**

Real robot validation:

**Not required for the initial research**

Next step:

**Define assumptions, scope, and exact experimental boundaries.**
