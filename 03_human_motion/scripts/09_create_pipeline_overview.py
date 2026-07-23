import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch



# =====================================================
# PATH
# =====================================================

ROOT = r"C:\latent-objective-humanoid\03_human_motion"


OUTPUT = os.path.join(
    ROOT,
    "media",
    "screenshots",
    "05_pipeline_overview.png"
)


os.makedirs(
    os.path.dirname(OUTPUT),
    exist_ok=True
)



# =====================================================
# CREATE FIGURE
# =====================================================

fig, ax = plt.subplots(
    figsize=(10,14)
)


ax.axis("off")



# =====================================================
# DRAW BOX FUNCTION
# =====================================================

def draw_box(
        y,
        title,
        subtitle,
        color
):


    box = FancyBboxPatch(

        (0.25, y),

        0.5,

        0.10,

        boxstyle="round,pad=0.02",

        linewidth=2,

        edgecolor="black",

        facecolor=color

    )


    ax.add_patch(
        box
    )


    ax.text(

        0.5,

        y+0.065,

        title,

        ha="center",

        va="center",

        fontsize=15,

        fontweight="bold"

    )


    ax.text(

        0.5,

        y+0.025,

        subtitle,

        ha="center",

        va="center",

        fontsize=9

    )





# =====================================================
# TITLE
# =====================================================


ax.text(

    0.5,

    0.96,

    "AMASS Human Motion Representation Pipeline",

    ha="center",

    fontsize=20,

    fontweight="bold"

)



ax.text(

    0.5,

    0.92,

    "Milestone 3: Humanoid Intelligence Research",

    ha="center",

    fontsize=13

)



# =====================================================
# PIPELINE BOXES
# =====================================================


draw_box(

    0.78,

    "AMASS Dataset",

    "CMU | KIT | ACCAD | HumanEva\nHuman Motion Capture",

    "#b9dcff"

)



draw_box(

    0.60,

    "SMPL-X Reconstruction",

    "Pose Parameters\n→ 3D Human Body Model",

    "#bde8c2"

)



draw_box(

    0.42,

    "3D Joint Representation",

    "127 Joints\nPosition + Temporal Motion",

    "#ffd7a8"

)



draw_box(

    0.24,

    "Motion Features",

    "Velocity\nAcceleration\nEnergy Dynamics",

    "#ffd7a8"

)



draw_box(

    0.06,

    "Motion Encoder",

    "Future Work\nPhysics-aware Transformer-VAE",

    "#dddddd"

)



# =====================================================
# ARROWS
# =====================================================


for y in [0.73,0.55,0.37,0.19]:

    ax.text(

        0.5,

        y,

        "↓",

        ha="center",

        fontsize=30,

        color="black"

    )




# =====================================================
# FOOTER
# =====================================================


ax.text(

    0.5,

    -0.03,

    "Human Motion → Representation → Humanoid Intelligence",

    ha="center",

    fontsize=14,

    fontweight="bold"

)



# =====================================================
# SAVE
# =====================================================


plt.savefig(

    OUTPUT,

    dpi=300,

    bbox_inches="tight",

    facecolor="white"

)


plt.close()



print("Pipeline overview saved:")
print(OUTPUT)