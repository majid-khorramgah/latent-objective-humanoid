# Literature Matrix — Latent Human Objectives for Generalizable Humanoid Intelligence

## Purpose

This matrix summarizes the literature reviewed so far for Phase 4.1:

> Learning latent human objectives from human demonstrations and using those objectives with model-based control under humanoid dynamics and physical constraints.

The purpose is not to collect papers exhaustively.

Each paper is included only if it contributes to at least one of the following:

- understanding how human objectives can be inferred,
- understanding candidate objectives for human motion/locomotion,
- understanding generalization of learned objectives,
- understanding model-based optimization/control,
- identifying limitations relevant to human-to-humanoid transfer,
- or clarifying the potential research gap.

---

# 1. High-Level Literature Map

The literature reviewed so far can be organized approximately as:

    Human Motor Control
            ↓
    Optimal Control
            ↓
    Inverse Optimal Control / IRL
            ↓
    Candidate Objective / Reward
            ↓
    Human Motion / Locomotion
            ↓
    Generalizable Objective Learning

However, the complete pipeline proposed in our project is:

    Human Demonstrations
            ↓
    Latent Human Objective
            ↓
    H1 Dynamics + Constraints
            ↓
    Model-Based MPC
            ↓
    Generalizable H1 Behavior

The literature reviewed so far covers many individual components of this pipeline.

It does NOT yet establish that the complete pipeline has been demonstrated.

---

# 2. Literature Matrix

| Paper | Category | Human Motion | Objective Inference | IOC / IRL | Composite / Multiple Costs | Generalization | Locomotion | Robot Transfer | MPC / Model-Based Control | Main Contribution to Our Project |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Todorov & Jordan (2002) | Optimal Feedback Control / Motor Control | ✓ | ✗ | ✗ | Conceptual | ✗ | ✗ | ✗ | Conceptual | Provides theoretical foundation for viewing human movement as optimization rather than trajectory reproduction |
| Mombaur, Truong & Laumond (2010) | IOC / Human-to-Humanoid Locomotion | ✓ | ✓ | ✓ | Candidate costs | Limited | ✓ | Partial | Model-based / optimization | Establishes an early connection between human motion, inverse optimal control and humanoid motion generation |
| Berret et al. (2011) | IOC / Human Motor Control | ✓ | ✓ | ✓ | ✓ | Limited | ✗ | ✗ | ✗ | Shows that human movement can be explained better by a composite objective than by a single criterion |
| Maroger et al. (2022) | IOC / Human Locomotion | ✓ | ✓ | ✓ | Candidate costs | Limited | ✓ | Limited | Optimization | Direct evidence that IOC can be applied to human locomotion rather than only reaching |
| Liu et al. (2022) | Human-Robot Locomotion Objectives | ✓ | ✓ / objective comparison | IOC-related | Multiple candidate objectives | Limited | ✓ | ✓ | Model-based relevance | Connects human locomotion objectives with the problem of transferring/using them for robot locomotion |
| Infer and Adapt (2023) | Bipedal Locomotion / Reward Learning | Human/robot locomotion | Reward learning | IRL / reward learning | Learned reward | ✓ in tested setting | ✓ | ✓ | Control-oriented | Demonstrates learning/adapting locomotion rewards rather than directly reproducing trajectories |
| Single-Level IOC (2025) | IOC | ✓ | ✓ | ✓ | Depends on representation | Computational/generalization aspects | — | — | Optimization | Relevant to making IOC computationally more practical and robust |
| Riemannian IOC (2026) | IOC / Geometric Learning | Motion | ✓ | ✓ | Representation-dependent | Scalability/generalization | — | — | Optimization | Extends IOC to nonlinear/geometric state spaces and addresses scalability of objective inference |
| Global Intent Inference (2026) | IRL / Generalizable Human Objective | ✓ | ✓ | ✓ / IRL | ✓ | ✓✓ | ✗ | ✗ | ✗ | Demonstrates subject-independent and posture-independent time-varying objective inference from human demonstrations |

---

# 3. Paper-by-Paper Interpretation

## Paper 1 — Todorov & Jordan (2002)

### Core idea

Human movement can be viewed as the result of an optimization process.

Instead of assuming that the exact trajectory is the important object, the theory asks what task objective the nervous system is trying to achieve.

Conceptually:

    Objective
        ↓
    Optimal Control
        ↓
    Human Motion

### What it gives us

This paper provides the theoretical motivation for our project.

It supports the shift from:

    "How do we copy the human trajectory?"

to:

    "What objective produced the human trajectory?"

### What it does NOT do

It does not infer an objective from demonstrations.

Therefore:

    Objective → Motion

rather than:

    Motion → Objective

### Role

**Theoretical foundation**

---

# 4. Paper 2 — Mombaur, Truong & Laumond (2010)

### Core idea

Human motion can be analyzed through inverse optimal control and then used to inform humanoid motion generation.

The important connection is:

    Human Motion
          ↓
    Infer / analyze objective
          ↓
    Humanoid Motion Generation

### What it gives us

This paper is important because it connects the human-motion objective problem to humanoid robotics.

It therefore provides an early bridge between:

- human movement,
- optimization,
- inverse optimal control,
- and humanoid motion.

### What it does NOT establish

It does not establish the complete modern pipeline:

    Generalizable latent objective
              ↓
    Different humanoid dynamics
              ↓
    MPC
              ↓
    Generalizable behavior

### Role

**Early human-to-humanoid connection**

---

# 5. Paper 3 — Berret et al. (2011)

### Core idea

Human movement may be generated by optimizing several criteria simultaneously.

For example:

    Effort
       +
    Smoothness

may explain human movement better than either criterion alone.

IOC reverses the usual direction:

    Objective → Motion

becomes:

    Observed Motion → Objective

### Important distinction

The paper mainly learns the contribution/weights of predefined candidate costs.

Therefore:

    Learning weights
        ≠
    Discovering arbitrary objective representation

### What it gives us

It establishes that:

> Human movement may be governed by a composite objective.

### What it does NOT establish

It concerns arm reaching, not locomotion.

It does not demonstrate:

- humanoid dynamics,
- morphology transfer,
- robot constraints,
- H1 control,
- MPC,
- or generalization across robot dynamics.

### Role

**Composite-objective evidence**

---

# 6. Paper 4 — Maroger et al. (2022)

### Core idea

The IOC framework is applied to human locomotion.

The important transition is:

    Human Reaching
          ↓
    Human Locomotion

The paper investigates whether walking motion can be explained by optimizing candidate locomotion criteria.

### What it gives us

This is important because our project concerns locomotion.

It shows that IOC is not limited to simple reaching tasks and can be applied to the more complex problem of human gait.

### What it does NOT establish

It does not automatically establish that the inferred objective:

- generalizes across humans,
- generalizes across tasks,
- transfers to a different morphology,
- survives different dynamics,
- or can directly be used by H1 MPC.

### Role

**Direct IOC-for-locomotion evidence**

---

# 7. Paper 5 — Liu et al. (2022)

### Core idea

Human locomotion can be studied in terms of underlying movement objectives and these objectives are relevant to human-to-robot locomotion.

The important conceptual question becomes:

    What makes human locomotion "human-like"?

rather than:

    How do we reproduce the exact human trajectory?

### What it gives us

It strengthens the connection between:

    Human locomotion objectives
              ↓
    Robot locomotion

This is directly relevant to the motivation of our project.

### What it does NOT establish

It does not establish that a latent objective learned from human demonstrations can be universally transferred to arbitrary humanoid dynamics.

### Role

**Human-to-robot objective connection**

---

# 8. Paper 6 — Infer and Adapt (2023)

### Core idea

Instead of directly imitating a locomotion trajectory, the approach learns/adapts a reward that can be used to generate locomotion behavior.

Conceptually:

    Demonstrations / behavior
            ↓
        Reward
            ↓
    Locomotion policy/behavior

### Why this matters

This is closer to our philosophy than trajectory imitation.

The robot is not required to copy the exact human joint trajectory.

Instead, it learns what behavior should be considered good.

### What it gives us

Evidence that:

> Reward/objective learning can be used for bipedal locomotion.

### Important limitation

Reward learning by itself does not solve the specific model-based transfer problem we are targeting.

Our desired pipeline is:

    Human demonstrations
            ↓
    Human objective
            ↓
    H1 dynamics
            +
    H1 constraints
            ↓
            MPC

### Role

**IRL/reward-learning bridge to locomotion**

---

# 9. Paper 7 — Single-Level IOC (2025)

### Core idea

IOC can become computationally difficult when the optimization/inference problem is complicated.

This work investigates a more efficient/robust formulation of IOC.

### Why it matters

If our project eventually needs to infer objectives from many human demonstrations, computational efficiency becomes important.

We cannot build a method that works only on a tiny toy example.

### What it gives us

It contributes to:

- computational efficiency,
- robustness,
- practical IOC formulation.

### What it does NOT establish

It does not by itself solve:

    Human locomotion
        ↓
    Generalizable objective
        ↓
    H1
        ↓
    MPC

### Role

**IOC scalability/computational practicality**

---

# 10. Paper 8 — Riemannian IOC (2026)

### Core idea

Human/robot motion often lives on nonlinear state spaces.

For example, orientations and rotations do not naturally live in ordinary Euclidean coordinates.

Riemannian/geometric formulations attempt to make IOC work more naturally with these spaces.

### Why it matters

Humanoid motion contains:

- rotations,
- joint configurations,
- nonlinear dynamics,
- contact-related states.

Therefore, the representation used by objective inference matters.

### What it gives us

It demonstrates that IOC can be formulated for more complex nonlinear/geometric spaces and addresses scalability.

### What it does NOT establish

It does not demonstrate generalizable human locomotion objectives transferred to H1.

### Role

**Geometric/scalable IOC**

---

# 11. Paper 9 — Global Intent Inference (2026)

### Core idea

The paper asks whether a common objective can explain human movements across:

- different subjects,
- different initial postures.

It uses MO-IRL and learns a time-varying objective.

Conceptually:

    Multiple humans
          +
    Multiple postures
          ↓
        IRL
          ↓
    Generalizable objective

### Important finding

The learned objective can generalize across subjects and initial postures in the tested reaching task.

The inferred objective is also time-varying rather than necessarily having fixed weights throughout the motion.

### Why this is important for our project

This paper means that:

> "Learning a generalizable human objective"

by itself is NOT a sufficient novelty claim.

Generalization across people has already been investigated.

### But there is still a major difference

Their pipeline:

    Human Reaching
          ↓
    Generalizable Objective
          ↓
    Human Motion Prediction

Our target:

    Human Locomotion
          ↓
    Generalizable Objective
          ↓
    Different Humanoid Dynamics
          ↓
    Physical Constraints
          ↓
    MPC
          ↓
    H1 Behavior

### Role

**Closest current evidence for generalizable objective inference**

---

# 12. Cross-Paper Comparison

## 12.1 Can human objectives be inferred?

**Yes.**

IOC and IRL literature establish this.

    Human Motion
         ↓
    IOC / IRL
         ↓
    Objective / Reward

Therefore this is **not new by itself**.

---

## 12.2 Can multiple objective components be used?

**Yes.**

Berret et al. provide evidence for composite objectives.

Therefore:

    "Human movement has multiple objectives"

is also **not new by itself**.

---

## 12.3 Can objectives be inferred for locomotion?

**Yes.**

The locomotion literature has already applied objective inference to walking/bipedal behavior.

Therefore:

    Human Locomotion
          ↓
    IOC / Reward Learning

is also **not new by itself**.

---

## 12.4 Can objectives generalize across humans?

**Yes, at least in some tasks.**

The 2026 Global Intent Inference work demonstrates subject-independent and posture-independent objective inference for reaching.

Therefore:

    Generalizable human objective

is **not sufficient as a novelty claim by itself**.

---

## 12.5 Can learned objectives transfer to a different robot morphology/dynamics?

**Unknown / Not established yet.**

This is one of the most important questions for the remaining literature review.

We specifically need to determine whether previous work has demonstrated:

    Human objective
          ↓
    Different robot morphology
          ↓
    Different dynamics
          ↓
    Generated behavior

---

## 12.6 Can the learned objective be used directly in model-based humanoid control?

**Not established yet from the literature reviewed so far.**

Our intended architecture is:

    Learned Human Objective
              ↓
       H1 Dynamics Model
              +
       H1 Constraints
              ↓
             MPC
              ↓
         H1 Behavior

This specific combination has not yet been established by the papers reviewed so far.

This must be checked against the remaining MPC and RoMeLa literature.

---

# 13. Current Research Gap Status

At this point, the following claims are already ruled out as sufficient novelty:

### Not sufficient

- "We use human demonstrations."
- "We use IOC."
- "We use IRL."
- "We learn a composite objective."
- "We learn a reward from demonstrations."
- "We learn a generalizable objective across humans."
- "We apply objective learning to locomotion."

All of these have relevant prior art.

---

# 14. Candidate Research Gap

The strongest candidate gap currently appears to be the intersection of:

    Human Demonstrations
             +
    Human Locomotion
             +
    Generalizable Objective
             +
    Different Robot Dynamics
             +
    Physical Constraints
             +
    Model-Based MPC

Conceptually:

    Human locomotion demonstrations
                ↓
       Learn human objective
                ↓
        Remove dependence on
        human morphology/dynamics
                ↓
        Apply objective to H1
                ↓
        H1 dynamics + constraints
                ↓
               MPC
                ↓
       Generate new H1 behavior

However:

> This is a CANDIDATE research gap, not an established research gap.

It must remain **NOT ESTABLISHED YET** until the remaining IRL, locomotion, MPC, and RoMeLa literature is checked.

---

# 15. Major Literature Lessons for Phase 4

## Lesson 1 — Do not learn trajectories directly

The literature supports the conceptual distinction:

    Trajectory Imitation

versus:

    Objective Inference
         +
    New Motion Generation

Our project should remain on the second path.

---

## Lesson 2 — Do not assume the objective beforehand

We currently have candidate hypotheses such as:

- effort,
- energy,
- smoothness,
- stability,
- robustness,
- task success.

These must NOT yet be treated as the final objective.

They remain:

**Candidate Objective Components**

until supported by locomotion literature and experiments.

---

## Lesson 3 — Weight learning is not the same as latent representation learning

Many existing methods start with:

    J = Σ wi Φi

and learn:

    wi

This means the representation:

    Φ1, Φ2, ..., Φn

was already chosen.

Therefore:

    Parameter/weight learning
             ≠
    unrestricted latent objective discovery

This distinction is important for Phase 4.2–4.5.

---

## Lesson 4 — Generalization must be defined explicitly

"Generalization" can mean:

1. across subjects,
2. across initial postures,
3. across tasks,
4. across environments,
5. across dynamics,
6. across morphology,
7. across robots.

The 2026 work already addresses some of the first two.

Our project is potentially interested in the much harder:

    Human → Robot

and potentially:

    Human Dynamics → H1 Dynamics

generalization.

---

## Lesson 5 — Objective may be time-varying

The recent IRL literature suggests that the contribution of different objectives may change throughout a movement.

Therefore we should not prematurely assume:

    J = constant weighted sum

A time-varying representation remains a candidate.

However:

> Whether time-varying objectives are necessary or useful for human locomotion is still UNKNOWN.

---

# 16. Current Decision Matrix

| Question | Current Answer | Confidence |
|---|---|---|
| Can human motion be viewed as optimization? | Yes | High |
| Can objectives be inferred from motion? | Yes | High |
| Can composite objectives explain human motion? | Yes | High |
| Can IOC be applied to human locomotion? | Yes | High |
| Can rewards/objectives be learned for bipedal locomotion? | Yes | High |
| Can objective inference generalize across humans? | Yes, in some tasks | High |
| Is generalizable objective learning itself novel? | No | High |
| Is a completely unconstrained latent objective representation already established? | Unknown | Medium |
| Is human locomotion objective transferable across robot morphology? | Not established yet | Low/Unknown |
| Is human objective transferable across substantially different dynamics? | Not established yet | Low/Unknown |
| Is learned human objective used as the central objective of H1 MPC? | Not established yet | Low/Unknown |
| Is the complete Human Objective → H1 Dynamics → MPC pipeline established? | Not established yet | Low/Unknown |

---

# 17. Current Research Question

The original research question was:

> Can humanoid robots learn generalizable behaviors by discovering latent physical objectives underlying human motion rather than directly imitating trajectories?

After the literature reviewed so far, this question should NOT yet be considered final.

A more precise temporary formulation is:

> **Can a generalizable objective underlying human locomotion be inferred from human demonstrations and subsequently used to generate humanoid behavior under different robot dynamics and physical constraints?**

This is a **working research question**, not the final formulation.

---

# 18. Current Candidate Architecture

The current conceptual architecture is:

    HUMAN DEMONSTRATIONS
             │
             ▼
    Objective Inference
       IOC / IRL
             │
             ▼
    Human Objective
    / Cost Representation
             │
             ▼
    ┌──────────────────────┐
    │   Unitree H1 Model   │
    │                      │
    │ Dynamics             │
    │ Joint Limits         │
    │ Torque Limits        │
    │ Contact Constraints  │
    └──────────────────────┘
             │
             ▼
            MPC
             │
             ▼
       H1 Motion
             │
             ▼
      Generalization
