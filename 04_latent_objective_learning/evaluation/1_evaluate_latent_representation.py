# ============================================================
# 33_evaluate_latent_representation.py
#
# Evaluate learned latent representation
# Stage 33
# ============================================================


import os
import torch
import numpy as np
from tqdm import tqdm


# ------------------------------------------------------------
# PATHS
# ------------------------------------------------------------

CHECKPOINT = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\checkpoints"
    r"\foundation_encoder_best.pt"
)


CHUNK_DIR = (
    r"D:\majid\foundation_motion_dataset_v2"
    r"\chunks"
)


OUTPUT_DIR = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\latent_outputs"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


DEVICE = "cuda"



# ------------------------------------------------------------
# LOAD MODEL
# ------------------------------------------------------------


print("="*70)
print("LATENT REPRESENTATION EVALUATION")
print("="*70)


checkpoint = torch.load(
    CHECKPOINT,
    map_location="cuda",
    weights_only=False
)


print(
    checkpoint.keys()
)



# ------------------------------------------------------------
# IMPORT MODEL
# ------------------------------------------------------------

from importlib.machinery import SourceFileLoader


model_file = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\models"
    r"\32_multibranch_motion_foundation_encoder.py"
)


module = SourceFileLoader(
    "encoder_module",
    model_file
).load_module()



model = module.FoundationTrainingModel()



model.load_state_dict(
    checkpoint["model"]
)


model.to(DEVICE)

model.eval()



# فقط encoder

encoder = model.encoder

encoder.eval()



# ------------------------------------------------------------
# LOAD CHUNKS
# ------------------------------------------------------------


chunks = sorted(
    [
        os.path.join(
            CHUNK_DIR,
            x
        )
        for x in os.listdir(CHUNK_DIR)
        if x.endswith(".pt")
    ]
)


print(
    "Chunks:",
    len(chunks)
)



temporal_all = []
physics_all = []
fusion_all = []



# ------------------------------------------------------------
# EXTRACTION
# ------------------------------------------------------------


with torch.no_grad():

    for path in tqdm(chunks):


        data = torch.load(
            path,
            map_location="cpu",
            weights_only=True
        )


        motion = data["motion"]


        motion = motion.to(
            DEVICE
        )


        joints = motion[:,:,:381]

        velocity = motion[:,:,381:762]

        acceleration = motion[:,:,762:1143]

        energy = motion[:,:,1143:]



        output = encoder(
            joints,
            velocity,
            acceleration,
            energy
        )


        temporal_all.append(
            output["temporal_latent"]
            .cpu()
        )


        physics_all.append(
            output["physics_latent"]
            .cpu()
        )


        fusion_all.append(
            output["fusion_latent"]
            .cpu()
        )



# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------


torch.save(
    torch.cat(
        temporal_all
    ),
    os.path.join(
        OUTPUT_DIR,
        "temporal_latents.pt"
    )
)


torch.save(
    torch.cat(
        physics_all
    ),
    os.path.join(
        OUTPUT_DIR,
        "physics_latents.pt"
    )
)


torch.save(
    torch.cat(
        fusion_all
    ),
    os.path.join(
        OUTPUT_DIR,
        "fusion_latents.pt"
    )
)



print("\nDONE")

print(
    "Temporal:",
    torch.cat(temporal_all).shape
)

print(
    "Physics:",
    torch.cat(physics_all).shape
)

print(
    "Fusion:",
    torch.cat(fusion_all).shape
)