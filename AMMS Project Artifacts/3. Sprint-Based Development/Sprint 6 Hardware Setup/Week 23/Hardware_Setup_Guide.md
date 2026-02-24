# Sprint 6 – Hardware Setup Guide: Raspberry Pi 4 Smart Mirror
**Sprint 6 | Week 23 | Phase 3: Sprint-Based Development**
**Sprint Goal:** Complete hardware assembly, OS setup, and all-module integration
**Date Range:** 24 – 28 February 2025

---

## 1. Hardware Bill of Materials (BOM)

| Component | Specification | Source | Unit Cost (MYR) |
|-----------|-------------|--------|---------------|
| Raspberry Pi 4 Model B | 8GB RAM | Cytron Malaysia | RM 340 |
| 27" IPS Monitor | 1920×1080, HDMI, 60Hz | Lazada | RM 420 |
| USB Webcam | 1080p, 30fps, wide-angle | Shopee | RM 75 |
| USB Omnidirectional Mic | Cardioid, 360° pickup | Shopee | RM 45 |
| USB/BT Speaker | 10W stereo | Shopee | RM 80 |
| Two-Way Mirror Glass | 600mm × 400mm, 30/70 reflectance | Custom Glass | RM 120 |
| Mirror Frame | Wooden, 680mm × 480mm | DIY | RM 60 |
| MicroSD Card | SanDisk 64GB A2 U3 | Shopee | RM 35 |
| RPi Official Power Supply | 5V/3A USB-C | Cytron | RM 35 |
| HDMI Cable | Ultra-thin, 0.5m | Lazada | RM 12 |
| **Total Estimated Cost** | | | **RM 1,222** |

---

## 2. Raspberry Pi 4 OS Setup

### 2.1 Raspberry Pi OS (64-bit Bookworm)

```bash
# Flash using Raspberry Pi Imager
# Select: Raspberry Pi OS (64-bit) — Bookworm Lite (no desktop for headless)
# Or: Full Desktop if using GUI debugging

# Boot settings (pre-config in Imager):
# - SSH: Enabled
# - WiFi: Your SSID + password
# - Hostname: amms.local
# - Username: pi
```

### 2.2 Post-Install Configuration

```bash
sudo raspi-config
# → Interface Options:
#    • Camera: Enable (for legacy camera if using CSI module)
#    • SSH: Enable
#    • VNC: Enable (remote access)
# → Display: Headless Resolution → 1920×1080

# → System Options:
#    • Boot to CLI (saves RAM vs desktop)

sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-pip python3-venv \
    libatlas-base-dev libjasper-dev libqtgui4 \
    libhdf5-dev libhdf5-serial-dev ffmpeg libsm6 libxext6 \
    cmake libboost-all-dev libssl-dev mpg123
```

### 2.3 Python Virtual Environment

```bash
python3 -m venv ~/amms-env
source ~/amms-env/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

## 3. Camera Configuration

### 3.1 USB Webcam (Recommended for AMMS)

```bash
# Verify camera detected
lsusb
# → Bus 001 Device 002: Logitech C920

ls /dev/video*
# → /dev/video0

# Test capture
python3 -c "import cv2; cap=cv2.VideoCapture(0); ret,f=cap.read(); cv2.imwrite('test.jpg',f); cap.release(); print('Camera OK:', ret)"
```

### 3.2 Camera Mounting Position

```
┌──────────────────────────────────────────────┐
│           MIRROR (front view)                │
│                    ▲                         │
│              [Camera here]                   │
│           (top center, behind glass)         │
│                                              │
│                 [Mirror]                     │
│                                              │
│         (Raspberry Pi + peripherals          │
│          mounted behind frame)              │
└──────────────────────────────────────────────┘
```

Camera is positioned above the mirror face center, ~3cm recessed behind the frame. The two-way mirror allows the camera to see through while the user sees their reflection.

---

## 4. Audio Configuration

### 4.1 Microphone Setup

```bash
# List audio input devices
arecord -l
# → **** List of CAPTURE Hardware Devices ****
# → card 1: USB Audio Device [USB Audio Device], device 0: ...

# Set USB mic as default capture device
nano ~/.asoundrc
```

```
~/.asoundrc:
pcm.!default {
    type asym
    capture.pcm "mic"
    playback.pcm "speaker"
}
pcm.mic {
    type plug
    slave { pcm "hw:1,0" }
}
pcm.speaker {
    type plug
    slave { pcm "hw:0,0" }
}
```

### 4.2 Test Audio

```bash
# Record 5 seconds
arecord -d 5 -f cd test.wav

# Play back
aplay test.wav

# Also test with Python (for Whisper)
python3 -c "import speech_recognition as sr; r=sr.Recognizer(); print('Mic OK')"
```

---

## 5. Ollama Installation on Raspberry Pi

```bash
# Install Ollama (ARM64 build for RPi4)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull LLaMA 3 8B quantised model (~4.7GB download)
ollama pull llama3:8b-q4_K_M

# Start Ollama server (background)
ollama serve &

# Verify
curl http://localhost:11434/api/tags
# → {"models":[{"name":"llama3..."}]}

# Configure Ollama to start on boot
sudo systemctl enable ollama
sudo systemctl start ollama
```

---

## 6. Physical Assembly Guide

### 6.1 Monitor Prep

1. Remove monitor stand; keep VESA mount holes
2. Test display with RPi4 via HDMI — verify 1920×1080 output
3. Rotate monitor 90° if vertical layout preferred (some mirror designs)

### 6.2 Two-Way Mirror Mounting

```
Side view:
[Wooden Frame]
  |
  ├── [Two-Way Mirror Glass] ← reflective side faces USER
  |        (30% reflection / 70% transmission)
  |
  ├── [Air gap: ~2cm]
  |
  ├── [Monitor screen] ← faces INWARD (emits light through glass)
  |
  └── [Mounting brackets]
```

### 6.3 Cable Management

- Use ultra-thin HDMI (0.5m) to connect RPi to monitor
- Route USB cables (camera, mic, speaker) through frame corners
- Power strip mounted at bottom of frame (1 outlet RPi, 1 monitor)

---

## 7. Auto-Start on Boot

```bash
# Create systemd service
sudo nano /etc/systemd/system/amms.service
```

```ini
[Unit]
Description=AMMS Smart Mirror Application
After=network.target ollama.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/amms
Environment="PATH=/home/pi/amms-env/bin"
ExecStart=/home/pi/amms-env/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable amms
sudo systemctl start amms
sudo systemctl status amms
```

---

## 8. System Performance Benchmarks (Final)

| Component | Usage | Notes |
|-----------|-------|-------|
| Idle (dashboard only) | CPU: 6%, RAM: 1.8GB | Stable |
| Face recognition active | CPU: 45%, RAM: 2.1GB | 123ms latency |
| Emotion detection + FR | CPU: 65%, RAM: 2.4GB | Throttled |
| Ollama generating | CPU: 87%, RAM: 6.9GB | Hot; fan required |
| All modules running | CPU: 92%, RAM: 7.2GB | ⚠️ Near limit |

> **Temperature note:** RPi4 may thermal-throttle (>80°C) during Ollama. Install a heatsink + 30mm fan inside the frame.

---

## 9. Sprint 6 Final Integration Checklist

- [x] All 6 software sprints integrated in `main.py`
- [x] Face recognition service operational (3 users enrolled)
- [x] Emotion detection active with WebSocket dashboard push
- [x] AURA LLM responding with context (Ollama running)
- [x] WhatsApp/Gmail send confirmed
- [x] Weather/Calendar/News widgets live
- [x] TTS speaking AURA responses aloud
- [x] Auto-boot via systemd
- [x] Mirror physically assembled and operational

---

## 10. References

1. Upton, E. & Halfacree, G. (2016). *Raspberry Pi User Guide.* Wiley.
2. Raspberry Pi Foundation (2024). *Raspberry Pi 4 Datasheet.* raspberrypi.com.
3. MagicMirror² (2024). *Installation Documentation.* magicmirror.builders/getting-started.
4. Mennicken, S. et al. (2016). "From today's augmented houses to tomorrow's smart homes." *UbiComp 2016.*
