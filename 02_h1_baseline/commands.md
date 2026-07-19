# H1 Baseline Training Commands

This document contains the commands used for training and evaluating the Unitree H1 humanoid locomotion baseline.

---

# 1. Train Unitree H1 Walking Policy

Command:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py --task=Isaac-Velocity-Flat-H1-v0
```

Purpose:

Train a baseline humanoid locomotion policy using:

- NVIDIA Isaac Lab
- RSL-RL
- PPO Reinforcement Learning

---

# 2. Resume Training

Command:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py --task=Isaac-Velocity-Flat-H1-v0 --resume
```

Purpose:

Continue training from a previously saved checkpoint.

---

# 3. Evaluate Trained Policy

Command:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/play.py --task=Isaac-Velocity-Flat-H1-v0
```

Purpose:

Visual evaluation of the learned H1 locomotion policy.

---

# 4. Verify Available Isaac Lab Tasks

Before training, verify the exact task name available in the installed Isaac Lab version.

Navigate to Isaac Lab:

```bash
cd C:\IsaacLab
```

List available environments:

```bash
isaaclab.bat -p scripts/environments/list_envs.py
```

Expected humanoid tasks:

```
Isaac-Velocity-Flat-H1-v0
Isaac-Velocity-Rough-H1-v0
```

The exact task name depends on the installed Isaac Lab version.

---

# Current Status

Completed:

- Isaac Sim setup
- Isaac Lab setup
- Unitree H1 environment validation

Next:

- Verify H1 locomotion task
- Train PPO walking baseline
- Save checkpoints
- Record training results
- Analyze locomotion performance

---

# Research Connection

The H1 locomotion baseline provides the reference controller for future experiments.

Baseline:

```
Standard PPO Locomotion Policy
```

Future research:

```
Latent Objective Conditioned Humanoid Learning
```

The comparison between these approaches will evaluate whether latent human objectives improve humanoid generalization.
