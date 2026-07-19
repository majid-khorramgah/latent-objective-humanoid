# H1 Locomotion Policy Checkpoint


## Overview

This folder contains the trained reinforcement learning checkpoint for the Unitree H1 humanoid locomotion policy.

The checkpoint was generated during Milestone 2 using NVIDIA Isaac Lab and the RSL-RL PPO framework.


---

# Training Information

Robot:

```
Unitree H1 Humanoid Robot
```


Simulator:

```
NVIDIA Isaac Sim 5.1
```


Framework:

```
NVIDIA Isaac Lab
```


Algorithm:

```
Proximal Policy Optimization (PPO)
```


Environment:

```
Isaac-Velocity-Flat-H1-v0
```


Training Iterations:

```
5000
```


---

# Checkpoint File

Final trained policy:

```
model_4999.pt
```


This checkpoint can be used for:

- Policy evaluation
- Resume training
- Future locomotion experiments
- Transfer learning research


---

# Usage

The checkpoint can be loaded using Isaac Lab evaluation tools:

```
play.py --task=Isaac-Velocity-Flat-H1-v0
```

---

# Research Purpose

This baseline policy provides the starting point for future experiments on:

- Human motion representation learning
- Latent objective discovery
- Objective-conditioned reinforcement learning
- Generalizable humanoid intelligence
