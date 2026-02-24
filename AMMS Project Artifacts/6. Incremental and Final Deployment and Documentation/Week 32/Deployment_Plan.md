# AMMS Deployment Plan
**Week 32 | Phase 6: Incremental and Final Deployment and Documentation**
**Date Range:** 28 April – 2 May 2025**

---

## 1. Deployment Strategy

AMMS follows an **Incremental Deployment** approach aligned with Agile principles:

| Phase | Scope | Status |
|-------|-------|--------|
| Sprint 1 Deploy | Face recognition running on RPi4 | ✅ Week 14 |
| Sprint 2 Deploy | Emotion detection added to live system | ✅ Week 17 |
| Sprint 3 Deploy | Ollama LLM + AURA voice active | ✅ Week 19 |
| Sprint 4 Deploy | WhatsApp/Gmail integrated | ✅ Week 21 |
| Sprint 5 Deploy | Full dashboard live with all widgets | ✅ Week 22 |
| Sprint 6 Deploy | Hardware assembled; systemd auto-start | ✅ Week 23 |
| **Final Deploy** | **Production-ready + documentation** | **← Week 32** |

---

## 2. Production Environment

| Component | Specification |
|-----------|-------------|
| Hardware | Raspberry Pi 4 (8GB) in custom mirror frame |
| OS | Raspberry Pi OS 64-bit Bookworm |
| Python | 3.11.x in virtualenv |
| LLM Server | Ollama → llama3:8b-q4_K_M |
| Web App | Flask 3.x + Flask-SocketIO |
| Database | SQLite 3 (amms.db) |
| Camera | USB 1080p webcam |
| Audio | USB mic + BT speaker |
| Network | Wi-Fi (LAN access) |

---

## 3. Deployment Checklist

### 3.1 Pre-Deployment

- [x] All unit tests passing (37/37)
- [x] All integration tests passing (23/23)
- [x] Functional test coverage confirmed (all FR-01 to FR-12)
- [x] UAT signed off by all 3 participants
- [x] SUS score ≥ 68 (achieved: 75.8)
- [x] No open Severity-1 defects
- [x] Python requirements.txt frozen with exact versions
- [x] Environment variables documented in `.env.example`

### 3.2 Deployment Steps

```bash
# 1. Final pull from git
cd /home/pi/amms
git pull origin main

# 2. Activate virtualenv and install/update deps
source ~/amms-env/bin/activate
pip install -r requirements.txt

# 3. Verify Ollama model available
ollama list | grep llama3

# 4. Run database migrations (if any)
python manage.py db upgrade

# 5. Run full test suite
pytest tests/ -v --tb=short

# 6. Restart services
sudo systemctl restart ollama
sudo systemctl restart amms

# 7. Verify system running
sudo systemctl status amms
curl http://localhost:5000/health
# → {"status": "ok", "version": "1.0.0", "uptime": "0:00:12"}
```

---

## 4. Environment Variables (.env.example)

```ini
# .env.example — copy to .env and fill in values
# NEVER commit .env to version control

# External APIs
OWM_API_KEY=your_openweathermap_key_here
NEWS_API_KEY=your_newsapi_key_here
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Gmail OAuth (paths to credentials)
GOOGLE_CREDENTIALS_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json

# App settings
FLASK_SECRET_KEY=generate_with_python_secrets_token_hex_32
OLLAMA_MODEL=llama3:8b-q4_K_M
OLLAMA_HOST=http://localhost:11434

# Hardware
CAMERA_INDEX=0
AUDIO_DEVICE_INDEX=1
```

---

## 5. Rollback Plan

| Issue | Rollback Strategy |
|-------|-----------------|
| New version breaks face recognition | `git checkout v0.9.0 -b hotfix` |
| Ollama model corrupted | `ollama pull llama3:8b-q4_K_M` (re-download) |
| Database migration goes wrong | Restore from daily backup: `cp amms.db.bak amms.db` |
| SystemD service crashes repeatedly | Check logs: `journalctl -u amms -n 100` |

---

## 6. Monitoring Plan

```bash
# System health check (run manually or via cron)
#!/bin/bash

echo "=== AMMS Health Check ==="
echo "Uptime: $(uptime)"
echo "CPU Temp: $(vcgencmd measure_temp)"
echo "Disk: $(df -h / | tail -1)"
echo "Memory: $(free -m | grep Mem)"
echo "Ollama: $(curl -s http://localhost:11434/api/tags | python3 -c 'import sys,json; d=json.load(sys.stdin); print(len(d["models"]),"models loaded")')"
echo "AMMS service: $(systemctl is-active amms)"
echo "Last login: $(sqlite3 amms.db "SELECT name, last_login FROM users ORDER BY last_login DESC LIMIT 1;")"
```

---

## 7. Backup Strategy

```bash
# Daily backup script (cron: 0 2 * * *)
#!/bin/bash
BACKUP_DIR="/home/pi/backups"
DATE=$(date +%Y%m%d)
cp /home/pi/amms/amms.db "$BACKUP_DIR/amms_$DATE.db"
cp /home/pi/amms/face_encodings.pkl "$BACKUP_DIR/encodings_$DATE.pkl"
# Keep last 7 days
find "$BACKUP_DIR" -name "*.db" -mtime +7 -delete
find "$BACKUP_DIR" -name "*.pkl" -mtime +7 -delete
```

---

## 8. References

1. Kim, G. et al. (2016). *The DevOps Handbook.* IT Revolution Press.
2. Humble, J. & Farley, D. (2010). *Continuous Delivery.* Addison-Wesley.
3. Raspberry Pi Foundation (2024). *Raspberry Pi OS Administration Guide.* raspberrypi.com.
