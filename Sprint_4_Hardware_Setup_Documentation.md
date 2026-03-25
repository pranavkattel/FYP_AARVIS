# Sprint 4: Hardware Setup Implementation Documentation

## Sprint Summary
- Sprint ID: 1.3.4
- Sprint Title: Hardware Setup
- Start Date: 2025-01-14
- End Date: 2025-01-27
- Goal: Prepare and validate the physical smart mirror deployment platform so the software stack can run reliably in real-world use.
- Milestone: M6 - Hardware Ready (2025-01-27)

## Sprint Objective
This sprint focused on creating a stable hardware foundation for the AARVIS smart mirror system. The implementation covered device preparation, physical installation, connectivity checks, and network validation to ensure the platform was ready for voice assistant, camera-based recognition, and dashboard rendering workflows.

---

## 1.3.4.1 Set up Raspberry Pi (2025-01-14 to 2025-01-16)

### Implementation Steps
- Prepared Raspberry Pi hardware with:
  - microSD image flashing and OS installation.
  - system package updates and firmware updates.
  - timezone, locale, and keyboard settings.
- Enabled required interfaces:
  - camera interface.
  - SSH for remote maintenance.
  - audio output stack for TTS playback.
- Installed runtime dependencies for project execution:
  - Python environment.
  - OpenCV-compatible camera stack.
  - web server dependencies for FastAPI-based services.
- Configured auto-start policy for application startup at boot.

### Sample Setup Commands
```bash
sudo apt update && sudo apt upgrade -y
sudo raspi-config
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Deliverable
- Raspberry Pi configured and boot-stable with project runtime prerequisites installed.

---

## 1.3.4.2 Mount monitor and camera (2025-01-17 to 2025-01-19)

### Implementation Steps
- Mounted display unit behind one-way mirror panel with alignment for full UI visibility.
- Positioned camera module at eye-level framing zone for robust face capture.
- Performed cable routing and strain relief for:
  - display cable.
  - camera cable.
  - power lines.
  - audio output path.
- Verified thermal and ventilation clearances to avoid throttling during continuous operation.

### Engineering Considerations
- Minimized camera tilt to reduce recognition errors from perspective distortion.
- Reduced reflective glare on the camera path by adjusting monitor brightness and angle.
- Secured components with vibration-safe mounting to avoid image instability.

### Deliverable
- Complete physical assembly with safe cable management and stable camera-monitor alignment.

---

## 1.3.4.3 Test basic connections (2025-01-20 to 2025-01-22)

### Implementation Steps
- Validated power-on sequence and clean shutdown behavior.
- Tested monitor output:
  - correct resolution.
  - refresh stability.
  - fullscreen dashboard rendering.
- Tested camera stream continuity using sample capture scripts.
- Tested microphone and speaker path for voice interaction.
- Confirmed peripheral detection after reboot cycles.

### Sample Verification Commands
```bash
# Camera test
libcamera-hello

# Audio device check
arecord -l
aplay -l

# Python camera probe
python -c "import cv2; cap=cv2.VideoCapture(0); print('camera_ok', cap.isOpened()); cap.release()"
```

### Deliverable
- Hardware I/O verified for display, camera, and audio channels under repeated startup conditions.

---

## 1.3.4.4 Ensure network connectivity (2025-01-23 to 2025-01-26)

### Implementation Steps
- Connected device to target network (Wi-Fi/Ethernet).
- Assigned stable network identity for local access.
- Validated outbound internet access for external APIs used by the project:
  - Google OAuth and Google APIs.
  - weather data API.
  - news data API.
- Validated inbound access for local smart mirror UI from browser clients.
- Performed connection-loss and reconnect tests to check recovery behavior.

### Sample Network Checks
```bash
ip a
ping -c 4 8.8.8.8
ping -c 4 google.com
curl -I http://localhost:8000
```

### Deliverable
- Reliable LAN and internet connectivity confirmed for both local UI access and cloud API integrations.

---

## 1.3.4.5 M6: Hardware Ready (2025-01-27)

### Exit Criteria
- Raspberry Pi fully configured and stable.
- Monitor and camera physically mounted and calibrated.
- Display, camera, microphone, and speaker validated.
- Network reliability and API reachability confirmed.
- Device ready for next sprint software integration tasks.

### Milestone Outcome
- Sprint 4 completed with hardware baseline established for AI assistant deployment.

---

## Validation Checklist
- [x] Device boots consistently without manual intervention.
- [x] Smart mirror UI renders on mounted monitor.
- [x] Camera feed is available for recognition pipeline.
- [x] Audio input/output operational for speech workflows.
- [x] Local network access and internet connectivity validated.
- [x] Platform accepted for subsequent calendar, email, and voice-control sprint work.

## Risks Identified and Mitigation
- Risk: Network instability can break API-dependent features.
  - Mitigation: Added connectivity checks and restart procedures.
- Risk: Camera angle misalignment can reduce recognition quality.
  - Mitigation: Added fixed mounting guides and framing tests.
- Risk: Thermal load during prolonged runtime.
  - Mitigation: Improved airflow clearance and monitored sustained operation.

## Sprint 4 to Sprint 5 Handover Notes
- Hardware environment is prepared for voice-controlled scheduling implementation.
- Remaining work transitions to software-first integration and UX refinement on top of verified hardware.
