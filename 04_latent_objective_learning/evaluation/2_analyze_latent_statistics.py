# ============================================================
# 33.1_analyze_latent_statistics.py
#
# Analyze latent representation statistics
#
# Stage 33.1
#
# Checks:
# - Mean
# - Std
# - Min / Max
# - Variance
# - Norm distribution
# - Diversity
# - Collapse detection
#
# ============================================================


import os
import json
import torch
import numpy as np
from tqdm import tqdm



# ============================================================
# PATHS
# ============================================================


LATENT_DIR = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\latent_outputs"
)


OUTPUT_FILE = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\latent_outputs"
    r"\latent_statistics_report.json"
)



# ============================================================
# LATENT FILES
# ============================================================


LATENT_FILES = {


    "temporal":

        "temporal_latents.pt",



    "physics":

        "physics_latents.pt",



    "fusion":

        "fusion_latents.pt"

}



# ============================================================
# ANALYSIS FUNCTIONS
# ============================================================



def analyze_tensor(name, tensor):


    print("\n")
    print("="*70)

    print(
        "ANALYZING:",
        name
    )

    print("="*70)



    print(
        "Shape:",
        tuple(tensor.shape)
    )



    # flatten samples

    samples = tensor.shape[0]


    flat = tensor.reshape(
        samples,
        -1
    )



    print(
        "Flattened:",
        flat.shape
    )



    # --------------------------------------------------------
    # statistics
    # --------------------------------------------------------


    mean = flat.mean().item()

    std = flat.std().item()

    min_val = flat.min().item()

    max_val = flat.max().item()



    variance = flat.var().item()



    # --------------------------------------------------------
    # norm analysis
    # --------------------------------------------------------


    norms = torch.norm(
        flat,
        dim=1
    )



    norm_mean = norms.mean().item()

    norm_std = norms.std().item()

    norm_min = norms.min().item()

    norm_max = norms.max().item()



    # --------------------------------------------------------
    # per dimension variance
    # --------------------------------------------------------


    dim_variance = flat.var(
        dim=0
    )


    active_dimensions = (
        dim_variance > 1e-6
    ).sum().item()



    total_dimensions = (
        dim_variance.shape[0]
    )



    active_ratio = (
        active_dimensions /
        total_dimensions
    )



    # --------------------------------------------------------
    # collapse detection
    # --------------------------------------------------------


    collapsed = False



    if std < 1e-5:

        collapsed = True



    if active_ratio < 0.05:

        collapsed = True



    result = {


        "name":

            name,


        "shape":

            list(tensor.shape),



        "mean":

            mean,



        "std":

            std,



        "variance":

            variance,



        "min":

            min_val,



        "max":

            max_val,



        "norm_mean":

            norm_mean,



        "norm_std":

            norm_std,



        "norm_min":

            norm_min,



        "norm_max":

            norm_max,



        "active_dimensions":

            active_dimensions,



        "total_dimensions":

            total_dimensions,



        "active_ratio":

            active_ratio,



        "collapse_detected":

            collapsed

    }



    print("\nStatistics:")

    for k,v in result.items():

        print(
            k,
            ":",
            v
        )


    return result





# ============================================================
# MAIN
# ============================================================



print("="*70)

print(
    "LATENT STATISTICS ANALYZER"
)

print("="*70)



report = {}



for name,file in LATENT_FILES.items():


    path = os.path.join(
        LATENT_DIR,
        file
    )


    print(
        "\nLoading:",
        path
    )



    latent = torch.load(
        path,
        map_location="cpu",
        weights_only=True
    )



    report[name] = analyze_tensor(
        name,
        latent
    )



    del latent




# ============================================================
# SAVE REPORT
# ============================================================


with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        report,
        f,
        indent=4
    )



print("\n")
print("="*70)

print(
    "REPORT SAVED"
)

print(
    OUTPUT_FILE
)

print("="*70)