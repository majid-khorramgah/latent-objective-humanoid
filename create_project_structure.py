import os

folders = [
    "docs",

    "01_isaaclab_setup/screenshots",
    "01_isaaclab_setup/videos",

    "02_h1_baseline/configs",
    "02_h1_baseline/training",
    "02_h1_baseline/checkpoints",
    "02_h1_baseline/results",
    "02_h1_baseline/videos",

    "03_human_motion/datasets",
    "03_human_motion/preprocessing",
    "03_human_motion/models",
    "03_human_motion/results",

    "04_latent_objective_learning/models",
    "04_latent_objective_learning/losses",
    "04_latent_objective_learning/experiments",
    "04_latent_objective_learning/results",

    "05_objective_conditioned_rl/baseline",
    "05_objective_conditioned_rl/ours",
    "05_objective_conditioned_rl/evaluation",
    "05_objective_conditioned_rl/results",

    "06_generalization/experiments",
    "06_generalization/results"
]


files = [
    "docs/research_goal.md",
    "docs/methodology.md",
    "docs/experiments.md",

    "01_isaaclab_setup/README.md",
    "01_isaaclab_setup/commands.md",

    "02_h1_baseline/README.md",

    "03_human_motion/README.md",

    "04_latent_objective_learning/README.md",

    "05_objective_conditioned_rl/README.md",

    "06_generalization/README.md",

    "requirements.txt",
    "environment.yml"
]


for folder in folders:
    os.makedirs(folder, exist_ok=True)

for file in files:
    with open(file, "w") as f:
        f.write("")


print("Project structure created successfully!")