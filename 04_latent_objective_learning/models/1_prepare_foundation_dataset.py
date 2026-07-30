# ============================================================
# prepare_foundation_dataset.py
#
# Multi-Branch Foundation Motion Dataset Builder
#
# AMASS -> Physics-aware chunks
#
# ============================================================


import os
import glob
import json
import numpy as np
import torch

from tqdm import tqdm



# ============================================================
# CONFIG
# ============================================================


FEATURE_ROOT = r"D:\results\features"


OUTPUT_ROOT = r"D:\foundation_motion_dataset"


CHUNK_DIR = os.path.join(
    OUTPUT_ROOT,
    "chunks"
)



SEQUENCE_LENGTH = 100


CHUNK_SIZE = 512


FEATURE_DIM = 1144



JOINT_DIM = 381


VELOCITY_DIM = 381


ACCELERATION_DIM = 381


ENERGY_DIM = 1




DEVICE = "cpu"



# ============================================================
# CREATE DIRECTORIES
# ============================================================


os.makedirs(
    CHUNK_DIR,
    exist_ok=True
)



print("="*80)

print("FOUNDATION DATASET BUILDER V2")

print("="*80)



print(
    "Input:",
    FEATURE_ROOT
)


print(
    "Output:",
    OUTPUT_ROOT
)






# ============================================================
# FIND FILES
# ============================================================



files = glob.glob(

    os.path.join(

        FEATURE_ROOT,

        "**",

        "*_features.npz"

    ),

    recursive=True

)



print()

print(
    "Feature files:",
    len(files)
)



if len(files)==0:

    raise RuntimeError(
        "No feature files found"
    )





# ============================================================
# FEATURE LOADER
# ============================================================


def load_feature(path):


    data=np.load(

        path,

        allow_pickle=True

    )


    joints=data["joints"].astype(
        np.float32
    )


    velocity=data["velocity"].astype(
        np.float32
    )


    acceleration=data["acceleration"].astype(
        np.float32
    )


    energy=data["energy"].astype(
        np.float32
    )



    return (
        joints,
        velocity,
        acceleration,
        energy
    )





# ============================================================
# FLATTEN COMPONENTS
# ============================================================


def prepare_sequence(
        joints,
        velocity,
        acceleration,
        energy
):


    T=joints.shape[0]



    joints=joints.reshape(
        T,
        -1
    )


    velocity=velocity.reshape(
        T,
        -1
    )


    acceleration=acceleration.reshape(
        T,
        -1
    )



    energy=energy.reshape(
        T,
        1
    )



    motion=np.concatenate(

        [
            joints,
            velocity,
            acceleration,
            energy
        ],

        axis=1

    )



    assert motion.shape[1]==FEATURE_DIM



    return (
        motion,
        joints,
        velocity,
        acceleration,
        energy
    )

# ============================================================
# SEQUENCE WINDOWING
# ============================================================


def split_sequence(
        motion,
        joints,
        velocity,
        acceleration,
        energy
):


    sequences=[]


    frames = motion.shape[0]


    for start in range(

        0,

        frames-SEQUENCE_LENGTH+1,

        SEQUENCE_LENGTH

    ):


        end=start+SEQUENCE_LENGTH


        sequences.append(

            {

            "motion":
                motion[start:end],


            "joints":
                joints[start:end],


            "velocity":
                velocity[start:end],


            "acceleration":
                acceleration[start:end],


            "energy":
                energy[start:end]

            }

        )


    return sequences






# ============================================================
# QUALITY CHECK
# ============================================================


def check_sequence(sample):


    for key,value in sample.items():


        if np.isnan(value).any():

            return False


        if np.isinf(value).any():

            return False



    return True







# ============================================================
# SAVE CHUNK
# ============================================================



def save_chunk(

        buffer,

        chunk_id

):


    print(
        f"\nSaving chunk {chunk_id}"
    )



    batch={}



    for key in buffer[0].keys():


        batch[key]=torch.tensor(

            np.stack(

                [

                x[key]

                for x in buffer

                ]

            ),

            dtype=torch.float32

        )



    path=os.path.join(

        CHUNK_DIR,

        f"chunk_{chunk_id:05d}.pt"

    )


    torch.save(

        batch,

        path

    )


    size=os.path.getsize(path)/1024**2



    print(

        f"Saved {path}"

    )


    print(

        f"Size: {size:.2f} MB"

    )




    return chunk_id+1





# ============================================================
# STREAMING PROCESS
# ============================================================



chunk_buffer=[]


chunk_id=0


total_sequences=0


invalid_sequences=0



print("\nStarting streaming conversion...")


for file in tqdm(files):


    try:


        (
            joints,
            velocity,
            acceleration,
            energy

        ) = load_feature(file)




        (
            motion,
            joints,
            velocity,
            acceleration,
            energy

        ) = prepare_sequence(

            joints,
            velocity,
            acceleration,
            energy

        )




        sequences=split_sequence(

            motion,
            joints,
            velocity,
            acceleration,
            energy

        )



        for seq in sequences:



            if not check_sequence(seq):


                invalid_sequences += 1


                continue



            chunk_buffer.append(seq)


            total_sequences += 1



            # ==========================
            # MEMORY CONTROL
            # ==========================


            if len(chunk_buffer)>=CHUNK_SIZE:


                chunk_id=save_chunk(

                    chunk_buffer,

                    chunk_id

                )


                # VERY IMPORTANT
                # release RAM


                chunk_buffer.clear()


                import gc

                gc.collect()







    except Exception as e:


        print("\nERROR:")

        print(file)

        print(e)







# ============================================================
# SAVE LAST SMALL CHUNK
# ============================================================


if len(chunk_buffer)>0:


    chunk_id=save_chunk(

        chunk_buffer,

        chunk_id

    )


    chunk_buffer.clear()



print("\n==============================")

print("STREAMING FINISHED")

print("==============================")



print(

"Total sequences:",

total_sequences

)


print(

"Invalid:",

invalid_sequences

)


print(

"Chunks:",

chunk_id

)

# ============================================================
# METADATA
# ============================================================


metadata = {


    "dataset_name":
        "AMASS_Physics_Aware_Foundation_Dataset_V2",


    "source":
        FEATURE_ROOT,


    "sequence_length":
        SEQUENCE_LENGTH,


    "chunk_size":
        CHUNK_SIZE,


    "feature_dimension":
        FEATURE_DIM,


    "components":

    {


        "joints":
            JOINT_DIM,


        "velocity":
            VELOCITY_DIM,


        "acceleration":
            ACCELERATION_DIM,


        "energy":
            ENERGY_DIM

    },


    "total_sequences":
        total_sequences,


    "invalid_sequences":
        invalid_sequences,


    "num_chunks":
        chunk_id

}






metadata_path=os.path.join(

    OUTPUT_ROOT,

    "metadata.json"

)



with open(

    metadata_path,

    "w",

    encoding="utf-8"

) as f:


    json.dump(

        metadata,

        f,

        indent=4

    )




print("\nMetadata saved:")

print(metadata_path)








# ============================================================
# DATASET STATISTICS
# ============================================================


print("\nComputing dataset statistics...")



statistics={


    "chunks_checked":

        0,


    "total_samples":

        0,


    "memory_MB":

        0

}




chunk_files=glob.glob(

    os.path.join(

        CHUNK_DIR,

        "*.pt"

    )

)






for path in tqdm(chunk_files):


    data=torch.load(

        path,

        map_location="cpu"

    )



    statistics["chunks_checked"] += 1



    samples=data["motion"].shape[0]


    statistics["total_samples"] += samples



    statistics["memory_MB"] += (

        os.path.getsize(path)

        /

        1024**2

    )



    del data



    import gc

    gc.collect()






statistics["memory_MB"]=round(

    statistics["memory_MB"],

    2

)





statistics_path=os.path.join(

    OUTPUT_ROOT,

    "statistics.json"

)



with open(

    statistics_path,

    "w",

    encoding="utf-8"

) as f:


    json.dump(

        statistics,

        f,

        indent=4

    )






print("\nStatistics saved:")

print(statistics_path)









# ============================================================
# FINAL VALIDATION
# ============================================================



print("\n================================")

print("FINAL VALIDATION")

print("================================")



if len(chunk_files)==0:


    raise RuntimeError(

        "No chunks created!"

    )




test_chunk=torch.load(

    chunk_files[0],

    map_location="cpu"

)





print("\nFirst chunk:")



for key,value in test_chunk.items():


    print(

        key,

        value.shape,

        value.dtype

    )







# ============================================================
# SHAPE CHECK
# ============================================================



assert test_chunk["motion"].shape[1:] == (

    SEQUENCE_LENGTH,

    FEATURE_DIM

)



assert test_chunk["joints"].shape[1:] == (

    SEQUENCE_LENGTH,

    JOINT_DIM

)



assert test_chunk["velocity"].shape[1:] == (

    SEQUENCE_LENGTH,

    VELOCITY_DIM

)



assert test_chunk["acceleration"].shape[1:] == (

    SEQUENCE_LENGTH,

    ACCELERATION_DIM

)



assert test_chunk["energy"].shape[1:] == (

    SEQUENCE_LENGTH,

    ENERGY_DIM

)





print("\n✓ All shapes correct")





print("""

============================================================

FOUNDATION DATASET V2 CREATED SUCCESSFULLY


Output:

D:\\majid\\foundation_motion_dataset_v2


Structure:


foundation_motion_dataset_v2

│

├── chunks

│     ├── chunk_00000.pt

│     ├── chunk_00001.pt

│     └── ...


├── metadata.json


└── statistics.json



Properties:


✓ Streaming conversion

✓ No full dataset loading

✓ RAM safe

✓ CPU safe

✓ Physics separated

✓ Multi-branch ready


Ready for:

32_multibranch_motion_foundation_encoder.py


============================================================

""")