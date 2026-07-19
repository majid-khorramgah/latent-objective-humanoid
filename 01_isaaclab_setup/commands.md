# Isaac Lab Setup Commands

This document contains all commands used during the Isaac Lab environment setup and validation.

---

# 1. Activate Isaac Lab Environment

```bash
conda activate env_isaaclab
```

---

# 2. Navigate to Isaac Lab Directory

```bash
cd C:\IsaacLab
```

---

# 3. Verify Isaac Lab Installation

```bash
isaaclab.bat -p scripts/environments/list_envs.py
```

Purpose:

Check available Isaac Lab environments and tasks.

---

# 4. Test Basic Reinforcement Learning Pipeline

## Ant Robot

Command:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py --task=Isaac-Ant-v0
```

Purpose:

Validate:

- Isaac Lab installation
- RSL-RL integration
- PPO training pipeline
- GPU simulation


---

# 5. Test Rough Terrain Locomotion

## ANYmal C Robot

Command:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py --task=Isaac-Velocity-Rough-Anymal-C-v0
```

Purpose:

Validate:

- Terrain generation
- Locomotion learning
- Curriculum learning
- Parallel simulation


---

# 6. Unitree H1 Humanoid Environment

## Random Agent Test

Command:

```bash
isaaclab.bat -p scripts/environments/random_agent.py --task Isaac-Velocity-Flat-H1-v0
```

Purpose:

Validate:

- Unitree H1 asset loading
- Humanoid articulation
- Observation space
- Action space


---

# 7. H1 Locomotion Training Baseline

Command:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Velocity-Flat-H1-v0
```

Purpose:

Train the first humanoid walking policy.

Expected outputs:

- Episode reward
- Episode length
- Policy checkpoints
- Training logs


---

# 8. Resume Training

Example:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Velocity-Flat-H1-v0 --resume
```

Purpose:

Continue training from saved checkpoint.


---

# 9. Play Trained Policy

Example:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/play.py --task Isaac-Velocity-Flat-H1-v0
```

Purpose:

Visual evaluation of the learned humanoid controller.


---

# 10. Experiment Tracking

For every experiment save:

```
Experiment Name
Date
Task Name
Command Used
Training Time
GPU
Number of Environments
Reward Results
Video Recording
Checkpoint Files
```

---

# Current Verified Commands

Completed:

✅ Isaac-Ant-v0 training  
✅ Isaac-Velocity-Rough-Anymal-C-v0 training  
✅ Isaac Lab GPU simulation  
✅ Unitree H1 environment loading  


---

# Next Commands to Execute

The next experiment:

```bash
isaaclab.bat -p scripts/reinforcement_learning/rsl_rl/train.py --task Isaac-Velocity-Flat-H1-v0
```

Goal:

Establish humanoid walking baseline before introducing:

- Human motion imitation
- Latent objective learning
- Objective-conditioned reinforcement learning
