import os
import numpy as np
import torch
import smplx
from tqdm import tqdm



# =====================================================
# PATHS
# =====================================================

ROOT = r"C:\latent-objective-humanoid\03_human_motion"


AMASS_PATH = os.path.join(
    ROOT,
    "data",
    "AMASS",
    "raw"
)


SMPLX_MODEL_PATH = os.path.join(
    ROOT,
    "external",
    "smplx",
    "models"
)


RESULT_PATH = os.path.join(
    "D:\\",
    "results"
)


FEATURE_PATH = os.path.join(
    RESULT_PATH,
    "features"
)


LOG_FILE = os.path.join(
    RESULT_PATH,
    "processing_log.txt"
)



# =====================================================
# LOG FUNCTION
# =====================================================

def write_log(message):

    os.makedirs(
        RESULT_PATH,
        exist_ok=True
    )

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(message + "\n")



# =====================================================
# LOAD SMPL-X
# =====================================================


print("\nLoading SMPL-X model...\n")


model = smplx.create(

    model_path=SMPLX_MODEL_PATH,

    model_type="smplx",

    gender="neutral",

    use_pca=False,

    batch_size=1

)


model.eval()


print("SMPL-X loaded successfully")

write_log(
    "SMPL-X model loaded"
)



# =====================================================
# PROCESS FUNCTION
# =====================================================


def process_file(
    npz_file,
    dataset_name
):


    filename = os.path.basename(
        npz_file
    ).replace(
        "_poses.npz",
        ""
    )


    feature_folder = os.path.join(
        FEATURE_PATH,
        dataset_name
    )


    os.makedirs(
        feature_folder,
        exist_ok=True
    )


    feature_file = os.path.join(
        feature_folder,
        filename + "_features.npz"
    )



    # ==========================================
    # RESUME CHECK
    # ==========================================

    if os.path.exists(feature_file):

        print("\nAlready processed:")
        print(feature_file)


        write_log(
            "SKIPPED: " + feature_file
        )


        return



    print("\n===================================")
    print("Dataset:", dataset_name)
    print("File:", npz_file)
    print("===================================")



    write_log(
        "START: " + npz_file
    )



    try:


        data = np.load(
            npz_file,
            allow_pickle=True
        )


        poses = data["poses"]

        betas = data["betas"]


        frames = poses.shape[0]


        print(
            "Frames:",
            frames
        )


        print(
            "Pose:",
            poses.shape
        )



        joints_all = []



        beta_tensor = torch.tensor(

            betas[:16],

            dtype=torch.float32

        ).reshape(
            1,
            16
        )



        # ==========================================
        # SMPL-X FORWARD
        # ==========================================


        for frame in tqdm(
            range(frames)
        ):


            pose = poses[frame]



            global_orient = torch.tensor(

                pose[:3],

                dtype=torch.float32

            ).reshape(
                1,
                3
            )



            body_pose = torch.tensor(

                pose[3:66],

                dtype=torch.float32

            ).reshape(
                1,
                63
            )



            left_hand_pose = torch.tensor(

                pose[66:111],

                dtype=torch.float32

            ).reshape(
                1,
                45
            )



            right_hand_pose = torch.tensor(

                pose[111:156],

                dtype=torch.float32

            ).reshape(
                1,
                45
            )



            with torch.no_grad():


                output = model(

                    betas=beta_tensor,

                    global_orient=global_orient,

                    body_pose=body_pose,

                    left_hand_pose=left_hand_pose,

                    right_hand_pose=right_hand_pose

                )



            joints_all.append(

                output.joints[0]

                .cpu()

                .numpy()

            )



        joints_all = np.array(
            joints_all
        )



        # ==========================================
        # FEATURE EXTRACTION
        # ==========================================


        velocity = np.zeros_like(
            joints_all
        )


        velocity[1:] = (

            joints_all[1:]

            -

            joints_all[:-1]

        )



        acceleration = np.zeros_like(
            velocity
        )


        acceleration[1:] = (

            velocity[1:]

            -

            velocity[:-1]

        )



        energy = np.sum(

            velocity ** 2,

            axis=(1,2)

        )



        # ==========================================
        # SAVE FEATURES
        # ==========================================


        np.savez(

            feature_file,

            joints=joints_all,

            velocity=velocity,

            acceleration=acceleration,

            energy=energy,

            fps=float(
                data["mocap_framerate"]
            )

        )



        print(
            "\nFeatures saved:"
        )

        print(
            feature_file
        )


        write_log(
            "DONE: " + feature_file
        )



    except Exception as e:


        print(
            "\nERROR:"
        )

        print(
            e
        )


        write_log(

            "ERROR: "

            + npz_file

            + " | "

            + str(e)

        )





# =====================================================
# FIND DATASETS
# =====================================================


datasets = [

    d for d in os.listdir(
        AMASS_PATH
    )

    if os.path.isdir(

        os.path.join(
            AMASS_PATH,
            d
        )

    )

]



print(
    "\nDatasets found:"
)


for d in datasets:

    print(
        "-",
        d
    )



# =====================================================
# PROCESS ALL DATASETS
# =====================================================


for dataset in datasets:


    dataset_path = os.path.join(

        AMASS_PATH,

        dataset

    )



    motion_files = []



    for root, dirs, files in os.walk(
        dataset_path
    ):


        for file in files:


            if file.endswith(
                "_poses.npz"
            ):


                motion_files.append(

                    os.path.join(
                        root,
                        file
                    )

                )



    print("\n")
    print("==============================")
    print(dataset)
    print(
        "motions:",
        len(motion_files)
    )
    print("==============================")



    write_log(

        "DATASET: "

        + dataset

        + " TOTAL: "

        + str(len(motion_files))

    )



    for motion in motion_files:


        process_file(

            motion,

            dataset

        )



print("\n\n================================")
print("ALL AMASS FEATURE EXTRACTION FINISHED")
print("================================")


write_log(
    "ALL FINISHED"
)