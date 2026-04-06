import whisper
import os
from datetime import datetime

# ===== SETTINGS =====
MODEL_NAME = "large-v3"
LANGUAGE = "ne"
INPUT_FILE = "Kamal Marg.m4a.mp4"
OUTPUT_DIR = "transcripts"

# ===== LOAD MODEL =====
print("🔄 Loading Whisper model (large-v3)...")
model = whisper.load_model(MODEL_NAME)
print("✅ Model loaded\n")

# ===== CHECK FILE =====
if not os.path.exists(INPUT_FILE):
    print(f"❌ File not found: {INPUT_FILE}")
    exit()

# ===== CREATE OUTPUT FOLDER =====
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===== TRANSCRIBE =====
print(f"🎧 Transcribing: {INPUT_FILE}")
start_time = datetime.now()

result = model.transcribe(
    INPUT_FILE,
    language=LANGUAGE,
    task="transcribe",
    verbose=True  # shows progress
)

# ===== SAVE OUTPUT =====
base_name = os.path.splitext(os.path.basename(INPUT_FILE))[0]
output_file = os.path.join(OUTPUT_DIR, f"{base_name}.txt")

with open(output_file, "w", encoding="utf-8") as f:
    f.write(result["text"])

end_time = datetime.now()

# ===== DONE =====
print("\n✅ Transcription complete!")
print(f"📄 Saved as: {output_file}")
print(f"⏱️ Time taken: {end_time - start_time}")