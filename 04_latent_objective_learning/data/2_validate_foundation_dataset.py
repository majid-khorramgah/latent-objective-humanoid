# ============================================================
# 31.5_validate_foundation_dataset.py
#
# Validate Foundation Dataset V2
#
# ============================================================


import os
import glob
import json
import torch
import numpy as np
from tqdm import tqdm



DATASET_ROOT = r"D:\majid\foundation_motion_dataset_v2"


CHUNK_DIR = os.path.join(
    DATASET_ROOT,
    "chunks"
)



print("="*70)
print("FOUNDATION DATASET VALIDATION")
print("="*70)



chunks = glob.glob(
    os.path.join(
        CHUNK_DIR,
        "*.pt"
    )
)


print(
    "Chunks found:",
    len(chunks)
)



if len(chunks)==0:

    raise RuntimeError(
        "No chunks found"
    )



report = {


    "total_chunks": len(chunks),

    "total_samples":0,

    "errors":[],

    "shapes":{}

}





expected_shapes = {


    "motion":
        (100,1144),


    "joints":
        (100,381),


    "velocity":
        (100,381),


    "acceleration":
        (100,381),


    "energy":
        (100,1)

}




for idx,path in enumerate(tqdm(chunks)):


    try:


        data=torch.load(

            path,

            map_location="cpu"

        )


        samples=data["motion"].shape[0]


        report["total_samples"] += samples



        for key,shape in expected_shapes.items():


            if key not in data:


                raise Exception(

                    f"Missing key {key}"

                )



            actual=tuple(

                data[key].shape[1:]

            )



            if actual != shape:


                raise Exception(

                    f"{key} shape error {actual}"

                )



            if torch.isnan(data[key]).any():


                raise Exception(

                    f"{key} contains NaN"

                )



            if torch.isinf(data[key]).any():


                raise Exception(

                    f"{key} contains Inf"

                )



        del data




    except Exception as e:


        report["errors"].append({

            "file":path,

            "error":str(e)

        })





print("\n================================")

print("VALIDATION RESULT")

print("================================")



print(

"Samples:",

report["total_samples"]

)


print(

"Errors:",

len(report["errors"])

)





output=os.path.join(

    DATASET_ROOT,

    "validation_report.json"

)



with open(

    output,

    "w"

) as f:


    json.dump(

        report,

        f,

        indent=4

    )



if len(report["errors"])==0:


    print("\n✓ DATASET READY FOR MODEL TRAINING")


else:

    print("\n⚠ DATASET HAS ERRORS")



print("\nSaved:")

print(output)