# Stage 04 — Feature Definition Question

## Current Motion Representation

The current normalized motion data contains the following information:

| Category | Currently Available | Status |
|---|---|---|
| **Direct** | 127 Joint positions | Available |
| **Direct** | 22 Body-core joints | Available |
| **Direct** | 40 Hand joints | Available |
| **Direct** | 59 Face joints | Available |
| **Direct** | Root position | Available |
| **Direct** | Root motion | Available |
| **Direct** | Body scale | Available |
| **Derived** | Joint velocity | Can be extracted |
| **Derived** | Joint acceleration | Can be extracted |
| **Derived** | Foot velocity | Can be extracted |
| **Derived** | Geometric angles | Can be extracted |
| **Derived** | Joint/segment distances | Can be extracted |
| **Derived** | Body-part velocity | Can be extracted |
| **Not defined** | Contact probability | Not currently defined |
| **Not defined** | Contact labels | Not currently defined |
| **Not defined** | Motion phase | Not currently defined |
| **Not defined** | Semantic labels | Not currently defined |

---

## Question

**Which motion features should we extract for the latent objective learning stage?**

In particular:

1. Which derived features would be most useful?
2. Should contact information be included?
3. Should motion-phase information be included?
4. Are there specific motion features you recommend for humanoid control and latent objective learning?

---

## What We Want

Before implementing `05_extract_features.py`, we would like to define the feature set based on your recommendation.

The goal is to:

- extract only useful motion features,
- avoid unnecessary features,
- keep the representation suitable for latent objective learning,
- and make the resulting dataset useful for the subsequent humanoid control stages.

**We would appreciate your recommendation on the feature definition for Stage 04.**