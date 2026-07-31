# ============================================================
# 32_multibranch_motion_foundation_encoder.py
#
# Multi-Branch Motion Foundation Encoder
#
# Temporal Latent + Physics Latent
#
# AMASS Physics-Aware Learning
#
# ============================================================


import os
import json
import math
import random

import torch
import torch.nn as nn
import torch.nn.functional as F

from torch.utils.data import Dataset, DataLoader, Sampler

from tqdm import tqdm





# ============================================================
# DEVICE
# ============================================================


DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)











# ============================================================
# PATHS
# ============================================================


DATASET_ROOT = (
    r"D:\majid\foundation_motion_dataset_v2"
)



CHUNK_DIR = os.path.join(

    DATASET_ROOT,

    "chunks"

)



CHECKPOINT_DIR = (

    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\checkpoints"

)



LOG_DIR = (

    r"C:\latent-objective-humanoid"
    r"\04_latent_objective_learning"
    r"\logs"

)



os.makedirs(

    CHECKPOINT_DIR,

    exist_ok=True

)


os.makedirs(

    LOG_DIR,

    exist_ok=True

)






# ============================================================
# TRAINING CONFIG
# ============================================================



SEED = 42



BATCH_SIZE = 256


NUM_EPOCHS = 100



LEARNING_RATE = 1e-4



WEIGHT_DECAY = 1e-5



NUM_WORKERS = 1

PERSISTENT_WORKERS = False



PIN_MEMORY = True



PREFETCH_FACTOR = None






# ============================================================
# DATA DIMENSIONS
# ============================================================



SEQ_LEN = 100



JOINT_DIM = 381


DYNAMIC_DIM = 762


ENERGY_DIM = 1



MOTION_DIM = 1144







# ============================================================
# LATENT DIMENSIONS
# ============================================================



TEMPORAL_TOKEN_DIM = 1024


TEMPORAL_TOKENS = 32



PHYSICS_TOKEN_DIM = 256


PHYSICS_TOKENS = 8



FUSION_DIM = 512







# ============================================================
# RANDOM SEED
# ============================================================



def set_seed(seed):


    random.seed(seed)


    torch.manual_seed(seed)


    torch.cuda.manual_seed_all(seed)



set_seed(SEED)







# ============================================================
# CHUNK DATASET
# ============================================================



class FoundationMotionDataset(Dataset):


    """
    
    Memory safe dataset.

    Loads only one chunk file at a time.

    Chunk:

    {
        motion:
        [B,100,1144]

        joints:
        [B,100,381]

        velocity:
        [B,100,381]

        acceleration:
        [B,100,381]

        energy:
        [B,100,1]
    }

    """



    def __init__(

            self,

            chunk_dir

    ):


        self.chunk_files = sorted(

            [

                os.path.join(

                    chunk_dir,

                    x

                )

                for x in os.listdir(chunk_dir)

                if x.endswith(".pt")

            ]

        )



        self.samples = []



        print(

            "Chunks found:",

            len(self.chunk_files)

        )



        # build index

        for chunk_id,path in enumerate(

                self.chunk_files

        ):



            data=torch.load(

                path,

                map_location="cpu",

                weights_only=True

            )



            n=data["motion"].shape[0]



            for i in range(n):


                self.samples.append(

                    (

                    chunk_id,

                    i

                    )

                )



            del data





        print(

            "Total samples:",

            len(self.samples)

        )



        self.current_chunk = None

        self.current_chunk_id = -1





    def load_chunk(self,chunk_id):



        if self.current_chunk_id != chunk_id:


            path=self.chunk_files[chunk_id]


            self.current_chunk=torch.load(

                path,

                map_location="cpu",

                weights_only=True

            )


            self.current_chunk_id=chunk_id





    def __len__(self):


        return len(self.samples)






    def __getitem__(self,index):


        chunk_id,sample_id = self.samples[index]



        self.load_chunk(

            chunk_id

        )



        data=self.current_chunk



        return {


            "joints":

                data["joints"][sample_id],



            "velocity":

                data["velocity"][sample_id],



            "acceleration":

                data["acceleration"][sample_id],



            "energy":

                data["energy"][sample_id],



            "motion":

                data["motion"][sample_id]


        }

# ============================================================
# CHUNK-AWARE BATCH SAMPLER
# ============================================================


class ChunkBatchSampler(Sampler):

    """
    Creates batches from only one chunk at a time.

    Randomization happens at two levels:

    1. Shuffle chunk order
    2. Shuffle samples inside each chunk

    This prevents random disk access between many chunks.
    """

    def __init__(
        self,
        dataset,
        batch_size,
        drop_last=False,
        seed=42
    ):

        self.dataset = dataset
        self.batch_size = batch_size
        self.drop_last = drop_last
        self.seed = seed
        self.epoch = 0

        self.chunk_to_indices = {}

        # Group global sample indices by chunk
        for global_index, sample_info in enumerate(
            self.dataset.samples
        ):

            chunk_id, sample_id = sample_info

            if chunk_id not in self.chunk_to_indices:
                self.chunk_to_indices[chunk_id] = []

            self.chunk_to_indices[chunk_id].append(
                global_index
            )

    def set_epoch(self, epoch):

        self.epoch = epoch

    def __iter__(self):

        # Different but reproducible shuffle every epoch
        rng = random.Random(
            self.seed + self.epoch
        )

        chunk_ids = list(
            self.chunk_to_indices.keys()
        )

        # Shuffle order of chunks
        rng.shuffle(chunk_ids)

        for chunk_id in chunk_ids:

            indices = self.chunk_to_indices[
                chunk_id
            ].copy()

            # Shuffle samples inside this chunk
            rng.shuffle(indices)

            for start in range(
                0,
                len(indices),
                self.batch_size
            ):

                batch_indices = indices[
                    start:start + self.batch_size
                ]

                if self.drop_last:

                    if len(batch_indices) == self.batch_size:
                        yield batch_indices

                else:

                    yield batch_indices

    def __len__(self):

        total_batches = 0

        for indices in self.chunk_to_indices.values():

            if self.drop_last:

                total_batches += (
                    len(indices) // self.batch_size
                )

            else:

                total_batches += math.ceil(
                    len(indices) / self.batch_size
                )

        return total_batches

# ============================================================
# PART 2/6
#
# Feature Branch Encoders
#
# Pose
# Dynamics
# Energy
#
# ============================================================




# ============================================================
# POSE ENCODER
# ============================================================


class PoseEncoder(nn.Module):


    """
    
    Encode human body geometry.

    Input:

        [B,T,381]


    Output:

        [B,T,256]

    """



    def __init__(self):


        super().__init__()



        self.encoder = nn.Sequential(


            nn.Linear(

                JOINT_DIM,

                512

            ),


            nn.LayerNorm(

                512

            ),


            nn.GELU(),



            nn.Dropout(

                0.1

            ),



            nn.Linear(

                512,

                256

            ),



            nn.LayerNorm(

                256

            )

        )





    def forward(self,x):


        B,T,D=x.shape



        x=x.reshape(

            B*T,

            D

        )


        x=self.encoder(x)



        x=x.reshape(

            B,

            T,

            256

        )



        return x







# ============================================================
# DYNAMICS ENCODER
# ============================================================


class DynamicsEncoder(nn.Module):


    """

    Encode velocity + acceleration.

    Input:

        [B,T,762]


    Output:

        [B,T,256]


    """



    def __init__(self):


        super().__init__()



        self.encoder=nn.Sequential(



            nn.Linear(

                DYNAMIC_DIM,

                1024

            ),



            nn.LayerNorm(

                1024

            ),



            nn.GELU(),



            nn.Dropout(

                0.1

            ),



            nn.Linear(

                1024,

                256

            ),



            nn.LayerNorm(

                256

            )

        )






    def forward(self,x):


        B,T,D=x.shape



        x=x.reshape(

            B*T,

            D

        )



        x=self.encoder(x)



        x=x.reshape(

            B,

            T,

            256

        )


        return x








# ============================================================
# ENERGY ENCODER
# ============================================================


class EnergyEncoder(nn.Module):


    """

    Encode physical effort.

    Input:

        [B,T,1]


    Output:

        [B,T,128]


    """



    def __init__(self):


        super().__init__()



        self.encoder=nn.Sequential(



            nn.Linear(

                ENERGY_DIM,

                64

            ),



            nn.GELU(),



            nn.Linear(

                64,

                128

            ),



            nn.LayerNorm(

                128

            )

        )






    def forward(self,x):


        B,T,D=x.shape



        x=x.reshape(

            B*T,

            D

        )



        x=self.encoder(x)



        x=x.reshape(

            B,

            T,

            128

        )


        return x







# ============================================================
# FEATURE FUSION PROJECTION
# ============================================================



class FeatureFusionProjection(nn.Module):


    """

    Combine:

    Pose
    +
    Dynamics
    +
    Energy


    256+256+128=640


    Project to foundation dimension


    """



    def __init__(self):


        super().__init__()



        self.projection=nn.Sequential(



            nn.Linear(

                640,

                1024

            ),



            nn.LayerNorm(

                1024

            ),



            nn.GELU(),



            nn.Dropout(

                0.1

            )

        )






    def forward(

            self,

            pose,

            dynamics,

            energy

    ):



        x=torch.cat(

            [

                pose,

                dynamics,

                energy

            ],

            dim=-1

        )



        return self.projection(x)

# ============================================================
# PART 3/6
#
# Temporal Foundation Encoder
#
# Input:
#
# [B,100,1024]
#
#
# Output:
#
# Temporal Latent
#
# [B,32,1024]
#
# ============================================================




# ============================================================
# TEMPORAL POSITION ENCODING
# ============================================================


class TemporalPositionalEncoding(nn.Module):


    """

    Learnable temporal position.

    Unlike fixed sinusoidal encoding,
    this allows motion-specific temporal learning.


    Input:

        [B,T,D]


    Output:

        [B,T,D]

    """



    def __init__(

            self,

            max_length=100,

            dim=1024

    ):


        super().__init__()



        self.position_embedding = nn.Parameter(


            torch.randn(

                1,

                max_length,

                dim

            )

            *

            0.02

        )






    def forward(self,x):


        T=x.size(1)



        return (

            x +

            self.position_embedding[:,:T]

        )







# ============================================================
# TEMPORAL TRANSFORMER
# ============================================================



class TemporalTransformerEncoder(nn.Module):


    """

    Foundation temporal understanding.


    Input:

        [B,100,1024]


    Output:

        [B,100,1024]



    """



    def __init__(self):


        super().__init__()



        encoder_layer = nn.TransformerEncoderLayer(



            d_model=TEMPORAL_TOKEN_DIM,



            nhead=16,



            dim_feedforward=4096,



            dropout=0.1,



            activation="gelu",



            batch_first=True,



            norm_first=True

        )




        self.transformer = nn.TransformerEncoder(


            encoder_layer,


            num_layers=8,


            enable_nested_tensor=False

        )





        self.norm=nn.LayerNorm(

            TEMPORAL_TOKEN_DIM

        )






    def forward(self,x):


        x=self.transformer(x)



        x=self.norm(x)



        return x







# ============================================================
# TEMPORAL TOKENIZER
# ============================================================



class TemporalTokenExtractor(nn.Module):


    """

    Converts:

        100 frame representation


    into:


        32 temporal tokens



    Similar idea to:

        Perceiver / TokenLearner


    """



    def __init__(self):


        super().__init__()



        self.attention = nn.Sequential(



            nn.Linear(

                TEMPORAL_TOKEN_DIM,

                256

            ),



            nn.GELU(),



            nn.Linear(

                256,

                TEMPORAL_TOKENS

            )

        )






        self.softmax=nn.Softmax(

            dim=1

        )






    def forward(self,x):


        """

        x:

        [B,100,1024]


        """


        B,T,D=x.shape



        weights=self.attention(x)



        # [B,100,32]



        weights=self.softmax(

            weights,

        )



        weights=weights.permute(

            0,

            2,

            1

        )



        # [B,32,100]



        tokens=torch.matmul(

            weights,

            x

        )



        # [B,32,1024]


        return tokens







# ============================================================
# TEMPORAL BRANCH COMPLETE
# ============================================================



class TemporalBranch(nn.Module):


    """

    Complete temporal pipeline:



    Fusion features

        |

    Positional encoding

        |

    Transformer

        |

    Token extractor

        |

    Temporal Latent



    """



    def __init__(self):


        super().__init__()



        self.position = TemporalPositionalEncoding(


            max_length=SEQ_LEN,


            dim=TEMPORAL_TOKEN_DIM

        )



        self.encoder = TemporalTransformerEncoder()



        self.tokenizer = TemporalTokenExtractor()






    def forward(self,x):


        x=self.position(x)



        x=self.encoder(x)



        tokens=self.tokenizer(x)



        return tokens

# ============================================================
# PART 4/6
#
# Physics Latent Encoder
#
# Input:
#
# [B,100,1024]
#
# Output:
#
# Physics Latent
#
# [B,8,256]
#
# ============================================================






# ============================================================
# PHYSICS PROJECTION
# ============================================================


class PhysicsProjection(nn.Module):


    """
    
    Convert temporal fusion representation
    into physics feature space.


    Input:

        [B,T,1024]


    Output:

        [B,T,256]

    """



    def __init__(self):

        super().__init__()



        self.projector = nn.Sequential(



            nn.Linear(

                TEMPORAL_TOKEN_DIM,

                512

            ),



            nn.LayerNorm(

                512

            ),



            nn.GELU(),



            nn.Dropout(

                0.1

            ),



            nn.Linear(

                512,

                PHYSICS_TOKEN_DIM

            ),



            nn.LayerNorm(

                PHYSICS_TOKEN_DIM

            )

        )




    def forward(self,x):


        B,T,D=x.shape


        x=x.reshape(

            B*T,

            D

        )


        x=self.projector(x)


        x=x.reshape(

            B,

            T,

            PHYSICS_TOKEN_DIM

        )


        return x







# ============================================================
# PHYSICS TRANSFORMER
# ============================================================



class PhysicsTransformer(nn.Module):


    """

    Learns physical relationships over time.


    Input:

        [B,100,256]


    Output:

        [B,100,256]



    """



    def __init__(self):


        super().__init__()



        layer=nn.TransformerEncoderLayer(



            d_model=PHYSICS_TOKEN_DIM,


            nhead=8,


            dim_feedforward=1024,


            dropout=0.1,


            activation="gelu",


            batch_first=True,


            norm_first=True

        )



        self.encoder=nn.TransformerEncoder(



            layer,


            num_layers=4,


            enable_nested_tensor=False

        )



        self.norm=nn.LayerNorm(

            PHYSICS_TOKEN_DIM

        )






    def forward(self,x):


        x=self.encoder(x)


        x=self.norm(x)


        return x







# ============================================================
# PHYSICS TOKEN EXTRACTOR
# ============================================================



class PhysicsTokenExtractor(nn.Module):


    """

    Convert:

        100 physics states


    into:


        8 physics tokens



    """



    def __init__(self):


        super().__init__()



        self.attention=nn.Sequential(



            nn.Linear(

                PHYSICS_TOKEN_DIM,

                128

            ),



            nn.GELU(),



            nn.Linear(

                128,

                PHYSICS_TOKENS

            )

        )



        self.softmax=nn.Softmax(

            dim=1

        )







    def forward(self,x):


        """

        x:

        [B,100,256]

        """



        weights=self.attention(x)


        # [B,100,8]



        weights=self.softmax(

            weights

        )



        weights=weights.permute(

            0,

            2,

            1

        )


        # [B,8,100]



        tokens=torch.matmul(

            weights,

            x

        )



        # [B,8,256]


        return tokens







# ============================================================
# PHYSICS BRANCH
# ============================================================



class PhysicsBranch(nn.Module):


    """

    Complete physics pipeline:


    Temporal Fusion

          |

    Projection

          |

    Physics Transformer

          |

    Token Extractor

          |

    Physics Latent



    """



    def __init__(self):


        super().__init__()



        self.projection=PhysicsProjection()



        self.encoder=PhysicsTransformer()



        self.tokenizer=PhysicsTokenExtractor()






    def forward(self,x):


        x=self.projection(x)



        x=self.encoder(x)



        tokens=self.tokenizer(x)



        return tokens

# ============================================================
# PART 5/6
#
# Complete Multi-Branch Foundation Encoder
#
# ============================================================





# ============================================================
# FUSION LATENT HEAD
# ============================================================



class FusionLatentHead(nn.Module):


    """
    
    Combine:

    Temporal Latent
    +
    Physics Latent


    Output:

    Global Motion Representation


    """



    def __init__(self):

        super().__init__()



        self.temporal_pool = nn.AdaptiveAvgPool1d(1)



        self.physics_pool = nn.AdaptiveAvgPool1d(1)





        self.fusion = nn.Sequential(



            nn.Linear(

                TEMPORAL_TOKEN_DIM

                +

                PHYSICS_TOKEN_DIM,

                1024

            ),



            nn.LayerNorm(

                1024

            ),



            nn.GELU(),



            nn.Dropout(

                0.1

            ),



            nn.Linear(

                1024,

                FUSION_DIM

            ),



            nn.LayerNorm(

                FUSION_DIM

            )

        )






    def forward(

            self,

            temporal_latent,

            physics_latent

    ):



        """

        temporal:

        [B,32,1024]


        physics:

        [B,8,256]

        """



        temporal_global = temporal_latent.mean(

            dim=1

        )


        physics_global = physics_latent.mean(

            dim=1

        )



        x=torch.cat(

            [

                temporal_global,

                physics_global

            ],

            dim=-1

        )



        x=self.fusion(x)



        return x







# ============================================================
# MAIN MODEL
# ============================================================



class MultiBranchMotionFoundationEncoder(nn.Module):


    """

    Complete Human Motion Foundation Model.



    Input:


        joints

        [B,100,381]



        velocity

        [B,100,381]



        acceleration

        [B,100,381]



        energy

        [B,100,1]





    Output:



        Temporal Latent

        [B,32,1024]



        Physics Latent

        [B,8,256]



        Fusion Latent

        [B,512]



    """





    def __init__(self):


        super().__init__()



        print(

            "Initializing Multi-Branch Encoder..."

        )



        # Feature branches


        self.pose_encoder = PoseEncoder()



        self.dynamics_encoder = DynamicsEncoder()



        self.energy_encoder = EnergyEncoder()





        # Fusion


        self.feature_fusion = FeatureFusionProjection()





        # Temporal


        self.temporal_branch = TemporalBranch()





        # Physics


        self.physics_branch = PhysicsBranch()





        # Final representation


        self.fusion_head = FusionLatentHead()







    def forward(

            self,

            joints,

            velocity,

            acceleration,

            energy

    ):



        # ==================================
        # Feature Encoding
        # ==================================


        pose_feature = self.pose_encoder(

            joints

        )



        dynamics_input=torch.cat(

            [

                velocity,

                acceleration

            ],

            dim=-1

        )



        dynamics_feature=self.dynamics_encoder(

            dynamics_input

        )



        energy_feature=self.energy_encoder(

            energy

        )





        # ==================================
        # Feature Fusion
        # ==================================


        fused=self.feature_fusion(

            pose_feature,

            dynamics_feature,

            energy_feature

        )



        # fused:

        # [B,100,1024]





        # ==================================
        # Temporal Representation
        # ==================================


        temporal_latent=self.temporal_branch(

            fused

        )



        # [B,32,1024]







        # ==================================
        # Physics Representation
        # ==================================


        physics_latent=self.physics_branch(

            fused

        )



        # [B,8,256]







        # ==================================
        # Global Fusion
        # ==================================


        fusion_latent=self.fusion_head(

            temporal_latent,

            physics_latent

        )



        # [B,512]






        return {


            "temporal_latent":

                temporal_latent,



            "physics_latent":

                physics_latent,



            "fusion_latent":

                fusion_latent

        }

# ============================================================
# PART 6/6
#
# Training Components
#
# ============================================================


# ============================================================
# RECONSTRUCTION DECODER
# ============================================================


class MotionDecoder(nn.Module):


    """
    
    Decode fusion latent back to motion.

    Used only for representation learning.

    """


    def __init__(self):

        super().__init__()


        self.decoder = nn.Sequential(

            nn.Linear(

                FUSION_DIM,

                1024

            ),

            nn.GELU(),


            nn.Linear(

                1024,

                SEQ_LEN * MOTION_DIM

            )

        )



    def forward(self,x):


        x=self.decoder(x)


        x=x.reshape(

            -1,

            SEQ_LEN,

            MOTION_DIM

        )


        return x







# ============================================================
# LOSS FUNCTION
# ============================================================


class FoundationLoss(nn.Module):


    def __init__(self):

        super().__init__()

        self.physics_projection = nn.Linear(
            256,
            1024
        )


        self.reconstruction_weight = 1.0


        self.physics_weight = 0.2


        self.separation_weight = 0.05





    def forward(

            self,

            output,

            motion

    ):



        losses={}



        # Reconstruction


        losses["reconstruction"] = F.mse_loss(

            output["reconstruction"],

            motion

        )




        # Physics regularization


        physics = output["physics_latent"]



        losses["physics"] = torch.mean(

            physics ** 2

        )





        # Temporal / Physics separation


        temporal = output["temporal_latent"].mean(

            dim=1

        )


        physics = output["physics_latent"].mean(

            dim=1

        )


        physics = self.physics_projection(

            physics
        )

        cosine = F.cosine_similarity(

            temporal,

            physics,

            dim=-1

        )



        losses["separation"] = torch.abs(

            cosine

        ).mean()






        total=(


            self.reconstruction_weight

            *

            losses["reconstruction"]


            +

            self.physics_weight

            *

            losses["physics"]


            +

            self.separation_weight

            *

            losses["separation"]

        )



        return total, losses







# ============================================================
# COMPLETE TRAINING MODEL
# ============================================================



class FoundationTrainingModel(nn.Module):


    def __init__(self):

        super().__init__()


        self.encoder = MultiBranchMotionFoundationEncoder()


        self.decoder = MotionDecoder()




    def forward(

            self,

            joints,

            velocity,

            acceleration,

            energy,

            motion

    ):


        latent=self.encoder(

            joints,

            velocity,

            acceleration,

            energy

        )



        reconstruction=self.decoder(

            latent["fusion_latent"]

        )


        latent["reconstruction"]=reconstruction



        return latent







# ============================================================
# TRAINING SETUP
# ============================================================


def main():

    print("="*80)

    print("MULTI-BRANCH MOTION FOUNDATION ENCODER")

    print("="*80)


    print(
        "Device:",
        DEVICE
    )

    dataset = FoundationMotionDataset(
        CHUNK_DIR
    )


    batch_sampler = ChunkBatchSampler(
        dataset=dataset,
        batch_size=BATCH_SIZE,
        drop_last=False,
        seed=SEED
    )


    loader = DataLoader(
        dataset,
        batch_sampler=batch_sampler,
        num_workers=NUM_WORKERS,
        pin_memory=PIN_MEMORY,
        persistent_workers=PERSISTENT_WORKERS,
        prefetch_factor=PREFETCH_FACTOR
    )





    model=FoundationTrainingModel().to(

        DEVICE

    )





    print("\nModel parameters:")


    print(

        sum(

            p.numel()

            for p in model.parameters()

            if p.requires_grad

        )

        /

        1e6,

        "Million"

    )







    criterion=FoundationLoss().to(

        DEVICE

    )





    optimizer=torch.optim.AdamW(

        model.parameters(),

        lr=LEARNING_RATE,

        weight_decay=WEIGHT_DECAY

    )





    scheduler=torch.optim.lr_scheduler.CosineAnnealingLR(

        optimizer,

        T_max=NUM_EPOCHS

    )





    scaler = torch.amp.GradScaler(
        "cuda",
        enabled=(DEVICE.type == "cuda")
    )






    # ============================================================
    # TRAIN LOOP
    # ============================================================



    best_loss=float("inf")





    for epoch in range(NUM_EPOCHS):


        batch_sampler.set_epoch(epoch)


        model.train()



        running_loss=0



        print("\n")

        print("="*60)

        print(

            f"Epoch {epoch+1}/{NUM_EPOCHS}"

        )

        print("="*60)





        for batch in tqdm(loader):



            joints=batch["joints"].to(

                DEVICE,

                non_blocking=True

            )


            velocity=batch["velocity"].to(

                DEVICE,

                non_blocking=True

            )


            acceleration=batch["acceleration"].to(

                DEVICE,

                non_blocking=True

            )


            energy=batch["energy"].to(

                DEVICE,

                non_blocking=True

            )


            motion=batch["motion"].to(

                DEVICE,

                non_blocking=True

            )





            optimizer.zero_grad()





            with torch.amp.autocast(
                device_type=DEVICE.type,
                enabled=(DEVICE.type == "cuda")
            ):



                output=model(

                    joints,

                    velocity,

                    acceleration,

                    energy,

                    motion

                )



                loss,loss_dict=criterion(

                    output,

                    motion

                )





            scaler.scale(loss).backward()



            torch.nn.utils.clip_grad_norm_(

                model.parameters(),

                1.0

            )



            scaler.step(

                optimizer

            )


            scaler.update()



            running_loss += loss.item()





        scheduler.step()





        epoch_loss = running_loss / len(loader)





        print(

            "Loss:",

            epoch_loss

        )





        # SAVE BEST


        if epoch_loss < best_loss:


            best_loss=epoch_loss



            torch.save(

                {

                "epoch":epoch,

                "model":

                    model.state_dict(),

                "loss":

                    best_loss

                },


                os.path.join(

                    CHECKPOINT_DIR,

                    "foundation_encoder_best.pt"

                )

            )



            print(

                "Best checkpoint saved"

            )





    print("\nTRAINING COMPLETE")

    print(

        "Best loss:",

        best_loss

    )

if __name__ == "__main__":

    import multiprocessing

    multiprocessing.freeze_support()

    main()