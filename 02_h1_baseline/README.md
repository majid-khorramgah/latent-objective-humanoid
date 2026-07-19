# Unitree H1 Locomotion Baseline

## Objective

This milestone focuses on training a baseline locomotion policy for the Unitree H1 humanoid robot using reinforcement learning in NVIDIA Isaac Lab.

The purpose of this baseline is to establish a reference controller before introducing latent objective learning.


## Method

Algorithm:

- Proximal Policy Optimization (PPO)

Framework:

- NVIDIA Isaac Lab
- RSL-RL


## Goals

- Train H1 walking policy
- Evaluate locomotion performance
- Record training metrics
- Save policy checkpoints


## Experiment Pipeline

Isaac Lab Environment

        |

        v

Unitree H1 Simulation

        |

        v

PPO Training

        |

        v

Walking Policy


## Expected Results

- Stable walking behavior
- Increasing episode reward
- Successful locomotion policy
