# ============================================================
# 33.2_visualize_latent_space.py
#
# Latent Space Visualization
#
# Stage 33.2
#
# PCA + UMAP
#
# ============================================================


import os
import torch
import numpy as np

from tqdm import tqdm

import matplotlib.pyplot as plt


from sklearn.decomposition import PCA

import umap





# ============================================================
# PATHS
# ============================================================


LATENT_DIR = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\latent_outputs"
)


OUTPUT_DIR = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\latent_outputs"
    r"\visualizations"
)


os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)




# ============================================================
# SETTINGS
# ============================================================


SAMPLE_SIZE = 5000


RANDOM_SEED = 42



np.random.seed(
    RANDOM_SEED
)



LATENTS = {


    "fusion":

    "fusion_latents.pt",



    "physics":

    "physics_latents.pt",



    "temporal":

    "temporal_latents.pt"

}





# ============================================================
# LOAD + PREPARE
# ============================================================


def load_latent(name,path):


    print("\n")
    print("="*70)

    print(
        "Loading:",
        name
    )

    print("="*70)



    latent=torch.load(

        os.path.join(
            LATENT_DIR,
            path
        ),

        map_location="cpu",

        weights_only=True

    )



    print(
        "Original shape:",
        latent.shape
    )



    # -------------------------------------
    # Flatten token based latent
    # -------------------------------------


    if len(latent.shape)==3:


        latent = latent.mean(
            dim=1
        )


        print(
            "After temporal pooling:",
            latent.shape
        )



    return latent.numpy()





# ============================================================
# VISUALIZATION
# ============================================================


def visualize(name,data):


    print("\nProcessing:",name)



    n=len(data)



    # sample

    if n>SAMPLE_SIZE:


        idx=np.random.choice(

            n,

            SAMPLE_SIZE,

            replace=False

        )


        data=data[idx]



    print(
        "Samples:",
        data.shape
    )



    # --------------------------------
    # PCA
    # --------------------------------


    print(
        "Running PCA..."
    )



    pca=PCA(

        n_components=50

    )



    reduced=pca.fit_transform(
        data
    )



    print(

        "PCA explained variance:",

        pca.explained_variance_ratio_.sum()

    )




    # --------------------------------
    # UMAP
    # --------------------------------


    print(
        "Running UMAP..."
    )



    reducer=umap.UMAP(

        n_components=2,

        n_neighbors=30,

        min_dist=0.1,

        random_state=42

    )



    embedding=reducer.fit_transform(

        reduced

    )



    print(
        "UMAP shape:",
        embedding.shape
    )




    # --------------------------------
    # SAVE
    # --------------------------------


    np.save(

        os.path.join(

            OUTPUT_DIR,

            name+"_umap.npy"

        ),

        embedding

    )




    # --------------------------------
    # PLOT
    # --------------------------------


    plt.figure(

        figsize=(10,8)

    )



    plt.scatter(

        embedding[:,0],

        embedding[:,1],

        s=3

    )



    plt.title(

        name+" Latent Space"

    )


    plt.xlabel(
        "UMAP-1"
    )


    plt.ylabel(
        "UMAP-2"
    )


    plt.tight_layout()



    save_path=os.path.join(

        OUTPUT_DIR,

        name+"_latent_umap.png"

    )



    plt.savefig(

        save_path,

        dpi=300

    )


    plt.close()



    print(
        "Saved:",
        save_path
    )





# ============================================================
# MAIN
# ============================================================


print("="*70)

print(
    "LATENT SPACE VISUALIZATION"
)

print("="*70)




for name,file in LATENTS.items():


    latent=load_latent(

        name,

        file

    )


    visualize(

        name,

        latent

    )



print("\n")
print("="*70)

print(
    "DONE"
)

print(
    OUTPUT_DIR
)

print("="*70)