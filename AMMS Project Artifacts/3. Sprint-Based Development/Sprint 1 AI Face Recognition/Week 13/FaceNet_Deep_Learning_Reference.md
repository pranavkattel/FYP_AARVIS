# FaceNet: Deep Facial Embedding for Recognition
**Sprint 1 | Week 13 | Phase 3: Sprint-Based Development**
**Date Range:** 23 – 27 December 2024**

---

## 1. Paper Overview

**Title:** *FaceNet: A Unified Embedding for Face Recognition and Clustering*  
**Authors:** Florian Schroff, Dmitry Kalenichenko, James Philbin (Google)  
**Year:** 2015  
**Conference:** CVPR 2015  
**LFW Accuracy:** 99.63%

---

## 2. Core Contribution

FaceNet learns a **direct mapping from face images to a compact Euclidean space** where distances directly correspond to face similarity. Unlike earlier systems (Eigenfaces, Fisherfaces, LBPH) that feed CNN feature maps into a classifier, FaceNet trains the entire pipeline end-to-end to produce a 128-dimensional embedding vector.

```
Face Image → Deep CNN (Inception v1/v3) → 128-d L2-normalized vector
```

Key insight: Once the embedding is learned, face recognition, verification, and clustering can be done using **simple distance thresholds** — no task-specific retraining needed.

---

## 3. Architecture

### 3.1 Backbone Options in Original Paper

| Backbone | Parameters | Speed | Accuracy |
|---------|-----------|-------|---------|
| Zeiler&Fergus (ZF) | 140M | Fast | Baseline |
| Inception v1 (GoogLeNet) | 6.6M | **Fast** | Near-SOTA |
| Inception v3 | 23.8M | Slow | SOTA |

FaceNet's key innovation was showing Inception v1 (fewer params) could approach SOTA with the right training objective — critical for edge deployment.

### 3.2 L2 Normalisation

The final embedding layer normalises the output to a unit hypersphere:

$$f(x) = \frac{g(x)}{||g(x)||_2}$$

This ensures all embeddings lie on the unit sphere in $\mathbb{R}^{128}$, making Euclidean distance equivalent to angular distance (cosine similarity).

---

## 4. Triplet Loss Function

The core training objective is **triplet loss**. For each training step, the network receives:

- **Anchor** $x^a$ — reference face image
- **Positive** $x^p$ — different image of same person
- **Negative** $x^n$ — image of different person

The loss forces:

$$||f(x^a) - f(x^p)||_2^2 + \alpha < ||f(x^a) - f(x^n)||_2^2$$

Where $\alpha$ is a margin (typically 0.2).

**Full loss function:**

$$\mathcal{L} = \sum_{i=1}^{N} \left[ ||f(x^a_i) - f(x^p_i)||_2^2 - ||f(x^a_i) - f(x^n_i)||_2^2 + \alpha \right]_+$$

The $[\cdot]_+$ notation means $\max(0, \cdot)$ — loss is only computed when the triplet constraint is violated.

### 4.1 Triplet Mining

Training on random triplets converges slowly. FaceNet uses **semi-hard negative mining**:

- Select negatives where $||f(a) - f(n)||_2 > ||f(a) - f(p)||_2$ but still within the margin

This focuses learning on the challenging, informative examples.

---

## 5. Training Dataset

| Dataset | Faces | Subjects |
|---------|-------|---------|
| Google internal | 100–200M | 8M+ |
| MS-Celeb-1M (public) | 10M | 100K |
| LFW (evaluation only) | 13,233 | 5,749 |

The model used in `face_recognition` library was trained on labeled faces from a large-scale dataset by Davis King (dlib).

---

## 6. FaceNet vs. dlib's face_recognition

The `face_recognition` Python library is built on dlib's ResNet face recognition model, which was inspired by FaceNet principles:

| Attribute | FaceNet (Google) | dlib face_recognition |
|-----------|----------------|-----------------------|
| Architecture | Inception | ResNet-34 |
| Embedding dim | 128-d | 128-d |
| Training data | ~100M images | ~3.3M images |
| LFW accuracy | 99.63% | 99.38% |
| Inference speed (CPU) | Slow | **~89ms/face** |
| Availability | Not publicly released | **Open source** |
| Python ease of use | Moderate | **Very easy** |

→ AMMS uses `face_recognition` (dlib) for practical deployment; FaceNet principles inform why the 128-d embedding approach works.

---

## 7. Implementation Notes for AMMS

### 7.1 Expected Embedding Distances

| Comparison Type | Typical Distance |
|----------------|----------------|
| Same person, same lighting | 0.10 – 0.30 |
| Same person, different lighting | 0.25 – 0.45 |
| Same person, 6 months later | 0.30 – 0.50 |
| Different people | 0.55 – 1.00 |

AMMS threshold = 0.5 (conservative) with option to relax to 0.55 if false rejections are too frequent.

### 7.2 Averaging Encodings (AMMS Strategy)

```python
import numpy as np

# Collect N samples during enrollment
encodings = [get_encoding(frame) for frame in capture_frames(N=10)]

# Average = more stable representation
average_encoding = np.mean(encodings, axis=0)

# Normalise (optional, dlib output is already near unit norm)
average_encoding /= np.linalg.norm(average_encoding)
```

### 7.3 Cosine Similarity Alternative

For highly variable lighting conditions, cosine similarity may outperform Euclidean:

$$\text{cosine\_sim}(e_1, e_2) = \frac{e_1 \cdot e_2}{||e_1|| \cdot ||e_2||}$$

Since dlib normalises to unit norm, cosine sim $\approx$ dot product. Threshold: sim > 0.9 for match.

---

## 8. Face Clustering Extension

FaceNet's embedding space enables **unsupervised face clustering** using algorithms like DBSCAN:

```python
from sklearn.cluster import DBSCAN

# Cluster unlabeled face encodings
clusters = DBSCAN(metric='euclidean', eps=0.5, min_samples=3)
cluster_labels = clusters.fit_predict(all_encodings)
```

AMMS Future Use: Group unrecognised faces from security footage for manual admin review.

---

## 9. References

1. Schroff, F., Kalenichenko, D., Philbin, J. (2015). "FaceNet: A Unified Embedding for Face Recognition and Clustering." *CVPR 2015*, 815-823.
2. King, D. E. (2015). *Dlib-ml face recognition blog*. dlib.net.
3. Taigman, Y. et al. (2014). "DeepFace: Closing the Gap to Human-Level Performance." *CVPR 2014*.
4. He, K. et al. (2016). "Deep Residual Learning for Image Recognition." *CVPR 2016*.
5. Huang, G.B. et al. (2007). "Labeled Faces in the Wild: A Database for Studying Face Recognition." *UMass Amherst*.
