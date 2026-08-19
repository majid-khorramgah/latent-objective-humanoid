# Stage 04 — Feature Definition Question

## Current Motion Representation

```text
                         STAGE 04
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
     DIRECT               DERIVED           NOT DEFINED
       │                    │                    │
   127 Joint positions   Joint velocity    Contact probability
   22 Body-core joints   Acceleration      Contact labels
   40 Hand joints        Foot velocity     Motion phase
   59 Face joints        Geometric angles  Semantic labels
   Root position         Distances
   Root motion            Body velocity
   Body scale
```

## Question

Which motion features should we extract for the **latent objective learning** stage?

In particular:

* Which derived features would be most useful?
* Should contact information be included?
* Should motion-phase information be included?
* Are there specific motion features you recommend for humanoid control and latent objective learning?

## What We Want

We want to define the feature extraction stage based on your recommendation before implementing:

```text
05_extract_features.py
```

The goal is to avoid extracting unnecessary features while ensuring that the resulting motion representation is sufficiently informative for the subsequent **latent objective learning** and **humanoid control** stages.
