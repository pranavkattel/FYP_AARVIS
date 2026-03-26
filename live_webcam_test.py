import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from PIL import Image

from insightface.app import FaceAnalysis
from test_training import FaceEmbeddingModel

print("[*] Initializing system...")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

print("[*] Loading Default InsightFace Model...")
face_app = FaceAnalysis(name='buffalo_sc', providers=['CPUExecutionProvider'])
face_app.prepare(ctx_id=-1, det_size=(640, 640))

print("[*] Loading Custom Nepali Face Model...")
custom_model = FaceEmbeddingModel(embedding_size=512).to(device)
custom_model.load_state_dict(torch.load('face_embedding_backbone.pth', map_location=device))
custom_model.eval()

transform = transforms.Compose([
    transforms.Resize((112, 112)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

def get_insightface_emb(face):
    """InsightFace natively normalized math"""
    return face.embedding / np.linalg.norm(face.embedding)

def get_custom_emb(frame, face):
    """Custom PyTorch math"""
    x1, y1, x2, y2 = face.bbox.astype(int)
    h, w = frame.shape[:2]
    cx1, cy1 = max(0, x1), max(0, y1)
    cx2, cy2 = min(w, x2), min(h, y2)
    face_crop = frame[cy1:cy2, cx1:cx2]
    
    # Catch weird crop errors if face is offscreen completely
    if face_crop.size == 0:
        return np.zeros(512)
        
    face_pil = Image.fromarray(cv2.cvtColor(face_crop, cv2.COLOR_BGR2RGB))
    img_t = transform(face_pil).unsqueeze(0).to(device)
    with torch.no_grad():
        test_emb = custom_model(img_t).cpu().numpy().squeeze()
    return test_emb

cap = cv2.VideoCapture(0)

# We hold onto these references after you press "r"
insight_ref = None
custom_ref = None

print("\n" + "="*60)
print(" LIVE WEBCAM: SIDE-BY-SIDE MODEL COMPARISON")
print(" 1. Look at the camera and press 'r' on your keyboard")
print("    to capture your base face parameters.")
print(" 2. Move your head so you can see how both models react in real-time.")
print(" 3. Press 'q' to quit.")
print("="*60 + "\n")

while True:
    ret, frame = cap.read()
    if not ret: break

    faces = face_app.get(frame)
    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
        
    for face in faces:
        x1, y1, x2, y2 = face.bbox.astype(int)
        
        # --- Capture Reference Embeddings ---
        if key == ord('r'):
            insight_ref = get_insightface_emb(face)
            custom_ref = get_custom_emb(frame, face)
            print("\n[*] LIVE REFERENCE FACE CAPTURED!")
            print("[*] Now showing similarity scores against that capture...")
            
        # Draw base box
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
        
        # --- If we have a reference, calc similarities! ---
        if insight_ref is not None and custom_ref is not None:
            insight_live = get_insightface_emb(face)
            custom_live = get_custom_emb(frame, face)
            
            # Simple Cosine Similarity
            sim_insight = np.dot(insight_ref, insight_live)
            sim_custom = np.dot(custom_ref, custom_live)
            
            text_i = f"InsightFace: {sim_insight*100:.1f}%"
            text_c = f"Custom Mdl : {sim_custom*100:.1f}%"
            
            # InsightFace Background (Blue Box)
            cv2.rectangle(frame, (x1, y1 - 50), (x2, y1 - 25), (255, 0, 0), cv2.FILLED)
            cv2.putText(frame, text_i, (x1 + 5, y1 - 32), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            
            # Custom Background (Green Box)
            cv2.rectangle(frame, (x1, y1 - 25), (x2, y1), (0, 200, 0), cv2.FILLED)
            cv2.putText(frame, text_c, (x1 + 5, y1 - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
        else:
            # Prompt user
            cv2.putText(frame, "PRESS 'r' TO CAPTURE REFERENCE FACE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 3)

    cv2.imshow("Model Comparison", frame)

cap.release()
cv2.destroyAllWindows()