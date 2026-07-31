# ============================================================
# 33.3_real_amass_linear_probe_v2.py
#
# Real Chunk-Level Linear Probe
#
# Uses:
#   - learned latent representations
#   - chunk_metadata labels
#
# ============================================================


import os
import json
import torch
import numpy as np


from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)




# ============================================================
# PATHS
# ============================================================


LATENT_DIR = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\latent_outputs"
)



METADATA_FILE = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\data"
    r"\chunk_metadata.pt"
)



OUTPUT_FILE = (
    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\latent_outputs"
    r"\real_linear_probe_results.json"
)



# ============================================================
# SETTINGS
# ============================================================


MIN_SAMPLES_PER_CLASS = 20


TEST_SIZE = 0.2


RANDOM_STATE = 42


MAX_ITER = 2000




# ============================================================
# LOAD METADATA
# ============================================================


def load_metadata():


    print("\nLoading metadata")

    metadata=torch.load(

        METADATA_FILE,

        map_location="cpu"

    )


    print(

        "Metadata samples:",

        len(metadata)

    )


    return metadata




# ============================================================
# CREATE LABELS
# ============================================================


def create_labels(metadata):


    actions=[

        x["action"]

        for x in metadata

    ]



    # count classes

    counts={}


    for a in actions:

        counts[a]=counts.get(a,0)+1



    print("\nAction distribution")


    for k,v in sorted(
        counts.items(),
        key=lambda x:x[1],
        reverse=True
    )[:30]:

        print(
            k,
            ":",
            v
        )



    # remove rare classes

    valid=[

        k

        for k,v in counts.items()

        if v>=MIN_SAMPLES_PER_CLASS

    ]



    print(

        "\nValid classes:",

        len(valid)

    )



    label_map={

        name:i

        for i,name in enumerate(valid)

    }



    labels=[]

    keep=[]



    for idx,a in enumerate(actions):


        if a in label_map:


            labels.append(

                label_map[a]

            )


            keep.append(idx)



    labels=np.array(labels)



    print(

        "Samples after filtering:",

        len(labels)

    )



    return labels,np.array(keep),label_map





# ============================================================
# LOAD LATENT
# ============================================================


def load_latent(name):


    path=os.path.join(

        LATENT_DIR,

        name+"_latents.pt"

    )


    print("\nLoading latent")

    print(path)



    latent=torch.load(

        path,

        map_location="cpu",

        weights_only=True

    )



    print(

        "Original:",

        latent.shape

    )



    # temporal tokens

    if latent.ndim==3:


        latent=latent.mean(

            dim=1

        )



    print(

        "After pooling:",

        latent.shape

    )



    return latent.numpy()




# ============================================================
# LINEAR PROBE
# ============================================================


def run_probe(

        name,

        X,

        y

):


    print("\n")

    print("="*70)

    print(

        "Testing:",

        name

    )

    print("="*70)



    X_train,X_test,y_train,y_test=train_test_split(

        X,

        y,

        test_size=TEST_SIZE,

        random_state=RANDOM_STATE,

        stratify=y

    )



    model=Pipeline(

        [

            (

            "scaler",

            StandardScaler()

            ),


            (

            "classifier",

            LogisticRegression(

                max_iter=MAX_ITER,

                n_jobs=-1,

                solver="lbfgs"

            )

            )

        ]

    )



    print("Training linear classifier...")



    model.fit(

        X_train,

        y_train

    )



    pred=model.predict(

        X_test

    )



    acc=accuracy_score(

        y_test,

        pred

    )



    print(

        "\nAccuracy:",

        acc

    )



    report=classification_report(

        y_test,

        pred,

        output_dict=True

    )



    print(

        classification_report(

            y_test,

            pred

        )

    )



    cm=confusion_matrix(

        y_test,

        pred

    )



    return {

        "accuracy":float(acc),

        "classification_report":report,

        "confusion_matrix":cm.tolist()

    }





# ============================================================
# MAIN
# ============================================================


print("="*80)

print(

"REAL AMASS CHUNK LEVEL LINEAR PROBE"

)

print("="*80)




metadata=load_metadata()



labels,indices,label_map=create_labels(

    metadata

)




results={}



for latent_name in [

    "fusion",

    "temporal",

    "physics"

]:


    X=load_latent(

        latent_name

    )



    # align with metadata

    X=X[indices]



    print(

        "Aligned:",

        X.shape,

        labels.shape

    )



    result=run_probe(

        latent_name,

        X,

        labels

    )


    results[latent_name]=result




results["label_mapping"]=label_map



# ============================================================
# SAVE
# ============================================================


with open(

    OUTPUT_FILE,

    "w",

    encoding="utf-8"

) as f:


    json.dump(

        results,

        f,

        indent=4

    )



print("\n")

print("="*80)

print("DONE")

print(

OUTPUT_FILE

)

print("="*80)