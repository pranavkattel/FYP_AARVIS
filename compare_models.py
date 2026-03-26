import os
import cv2
import numpy as np
import random
import torch
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt

# Attempt to import sklearn, install if missing
try:
    from sklearn.metrics import roc_curve, auc
except ImportError:
    import subprocess
    import sys
    print("Installing scikit-learn for metric calculation...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "scikit-learn"])
    from sklearn.metrics import roc_curve, auc

from insightface.app import FaceAnalysis

# Import your custom architecture
from test_training import FaceEmbeddingModel

# --- Configuration ---
DATA_DIR = 'Dataset/Dataset'
PAIRS_PER_TYPE = 400  # Will test 400 SAME pairs and 400 DIFFERENT pairs

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"[*] Using device: {device}")

# --- Initialize Models ---
print("[*] Loading InsightFace (Default)...")
face_app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=-1, det_size=(640, 640))

print("[*] Loading Custom Nepali Model...")
custom_model = FaceEmbeddingModel(embedding_size=512).to(device)
custom_model.load_state_dict(torch.load('face_embedding_backbone.pth', map_location=device))
custom_model.eval()

transform = transforms.Compose([
    transforms.Resize((112, 112)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# --- Helper Functions ---
def get_embeddings(img_path):
    """Returns (insightface_emb, custom_emb) for a given image path."""
    frame = cv2.imread(img_path)
    if frame is None:
        return None, None
        
    faces = face_app.get(frame)
    if len(faces) == 0:
        return None, None
        
    face = faces[0]
    
    # 1. Default InsightFace Embedding
    emb_default = face.embedding / np.linalg.norm(face.embedding)
    
    # 2. Custom Model Embedding
    try:
        x1, y1, x2, y2 = face.bbox.astype(int)
        h, w = frame.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        face_crop = frame[y1:y2, x1:x2]
        face_pil = Image.fromarray(cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB))
        
        img_t = transform(face_pil).unsqueeze(0).to(device)
        with torch.no_grad():
            emb_custom = custom_model(img_t).cpu().numpy().squeeze()
            
        return emb_default, emb_custom
    except Exception as e:
        print(f"Error processing custom crop for {img_path}: {e}")
        return emb_default, None

def cosine_sim(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# --- Data Preparation ---
print("\n[*] Indexing dataset...")
identity_dict = {}
for identity in os.listdir(DATA_DIR):
    id_path = os.path.join(DATA_DIR, identity)
    if os.path.isdir(id_path):
        images = [os.path.join(id_path, img) for img in os.listdir(id_path) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if len(images) >= 2:  # Need at least 2 images to form a positive pair
            identity_dict[identity] = images

identities = list(identity_dict.keys())
print(f"[*] Found {len(identities)} identities with multiple images.")

if len(identities) < 2:
    print("Not enough data to run comparison!")
    exit()

# Generate Pairs
positive_pairs = []
negative_pairs = []

# Positive Pairs (Same Person)
print("[*] Generating testing pairs...")
for _ in range(PAIRS_PER_TYPE):
    identity = random.choice(identities)
    img1, img2 = random.sample(identity_dict[identity], 2)
    positive_pairs.append((img1, img2, 1))

# Negative Pairs (Different People)
for _ in range(PAIRS_PER_TYPE):
    id1, id2 = random.sample(identities, 2)
    img1 = random.choice(identity_dict[id1])
    img2 = random.choice(identity_dict[id2])
    negative_pairs.append((img1, img2, 0))

all_pairs = positive_pairs + negative_pairs
random.shuffle(all_pairs)

# --- Evaluation ---
print(f"[*] Extracting embeddings and computing similarities for {len(all_pairs)} pairs...")

labels = []
default_sims = []
custom_sims = []

processed_count = 0
for img1_path, img2_path, label in all_pairs:
    def_emb1, cust_emb1 = get_embeddings(img1_path)
    if def_emb1 is None: continue
    
    def_emb2, cust_emb2 = get_embeddings(img2_path)
    if def_emb2 is None: continue
    
    # Calculate similarities
    sim_def = cosine_sim(def_emb1, def_emb2)
    default_sims.append(sim_def)
    
    if cust_emb1 is not None and cust_emb2 is not None:
        sim_cust = cosine_sim(cust_emb1, cust_emb2)
        custom_sims.append(sim_cust)
    else:
        custom_sims.append(-1.0) # Fail safeguard
        
    labels.append(label)
    processed_count += 1
    
    if processed_count % 100 == 0:
        print(f"    Processed {processed_count}/{len(all_pairs)} pairs...")

# --- Analysis & Metrics ---
print("\n[*] Calculating comparative metrics...")
labels = np.array(labels)
default_sims = np.array(default_sims)
custom_sims = np.array(custom_sims)

# ROC and AUC Calculation
fpr_def, tpr_def, thresholds_def = roc_curve(labels, default_sims)
auc_def = auc(fpr_def, tpr_def)

fpr_cust, tpr_cust, thresholds_cust = roc_curve(labels, custom_sims)
auc_cust = auc(fpr_cust, tpr_cust)

# Find optimal accuracy threshold algorithmically
def find_best_acc(labels, sims, thresholds):
    best_acc = 0
    best_thresh = 0
    for thresh in thresholds:
        preds = (sims >= thresh).astype(int)
        acc = np.mean(preds == labels)
        if acc > best_acc:
            best_acc = acc
            best_thresh = thresh
    return best_acc, best_thresh

acc_def, thresh_def = find_best_acc(labels, default_sims, thresholds_def)
acc_cust, thresh_cust = find_best_acc(labels, custom_sims, thresholds_cust)

# --- Print Results ---
print("\n" + "="*50)
print(f"| {'METRIC':<20} | {'DEFAULT (buffalo_sc)':<10} | {'CUSTOM NEPALI':<10} |")
print("="*50)
print(f"| {'Model AUC (Area)':<20} | {auc_def:.4f}           | {auc_cust:.4f}        |")
print(f"| {'Best Accuracy':<20} | {acc_def*100:.2f}%          | {acc_cust*100:.2f}%       |")
print(f"| {'Optimal Threshold':<20} | {thresh_def:.2f}             | {thresh_cust:.2f}          |")
print("="*50)

# --- Plot ROC Curve ---
plt.figure(figsize=(8, 6))
plt.plot(fpr_def, tpr_def, color='darkorange', lw=2, label=f'Default InsightFace (AUC = {auc_def:.3f})')
plt.plot(fpr_cust, tpr_cust, color='green', lw=2, label=f'Custom Nepali Model (AUC = {auc_cust:.3f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate (Incorrect Matches)')
plt.ylabel('True Positive Rate (Correct Matches)')
plt.title('Receiver Operating Characteristic (ROC) Comparison')
plt.legend(loc="lower right")
plt.grid(alpha=0.3)

plot_path = "model_comparison_roc.png"
plt.savefig(plot_path, dpi=200, bbox_inches='tight')
print(f"\n[SUCCESS] ROC Graph saved as '{plot_path}'")
print("[INFO] High AUC and High Accuracy indicate a better model.")
