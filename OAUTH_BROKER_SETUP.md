# OAuth Broker Setup (VPS)

Use this when you want Google sign-in on phone via VPS, while face recognition and heavy features stay on your local device.

## 1) Run broker on VPS

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python oauth_broker_server.py
```

For production, run behind HTTPS reverse proxy (Caddy/Nginx).

## 2) Broker environment (VPS)

Set these env vars on VPS:

- `PUBLIC_BASE_URL=https://auth.yourdomain.com`
- `GOOGLE_OAUTH_REDIRECT_URI=https://auth.yourdomain.com/auth/google/callback`
- `OAUTH_PAIR_TTL_SECONDS=600` (optional)

In Google Cloud Console (OAuth Web client), add:

- `https://auth.yourdomain.com/auth/google/callback`

## 3) Local app environment (your device)

Set this env var in your local app `.env`:

- `OAUTH_BROKER_BASE_URL=https://auth.yourdomain.com`

When this variable is set, local `/register` and `/login` will create pair tokens on broker and show broker QR URLs.

## 4) Flow

1. Local UI creates pair on broker.
2. Phone scans QR and signs in via broker.
3. Local app polls broker status through local `/api/pair-status/{pair}`.
4. Local app claims profile/tokens one time and creates local session.
5. Local app continues face setup locally.
