from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta, timezone
import secrets
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from services.google_oauth import build_auth_url, exchange_code_for_tokens

app = FastAPI(title="AARVIS OAuth Broker")

PAIR_TTL_SECONDS = int(os.getenv("OAUTH_PAIR_TTL_SECONDS", "600"))

# ── Auto-select OAuth broker configuration based on OAUTH_METHOD ──
OAUTH_METHOD = os.getenv("OAUTH_METHOD", "vps").lower().strip()
if OAUTH_METHOD == "ngrok":
    PUBLIC_BASE_URL = os.getenv("NGROK_OAUTH_BROKER_URL", "").strip().rstrip("/")
    GOOGLE_OAUTH_REDIRECT_URI = os.getenv("NGROK_OAUTH_REDIRECT_URI", "").strip()
elif OAUTH_METHOD == "vps":
    PUBLIC_BASE_URL = os.getenv("VPS_OAUTH_BROKER_URL", "").strip().rstrip("/")
    GOOGLE_OAUTH_REDIRECT_URI = os.getenv("VPS_OAUTH_REDIRECT_URI", "").strip()
else:
    PUBLIC_BASE_URL = ""
    GOOGLE_OAUTH_REDIRECT_URI = ""

print(f"[OAuth Broker Config] Method: {OAUTH_METHOD} | Public Base: {PUBLIC_BASE_URL}")

# {pair_token: {status, intent, expires_at, profile, tokens, claimed}}
pair_sessions: dict[str, dict] = {}
# {state: pair_token}
state_index: dict[str, str] = {}


class PairCreateRequest(BaseModel):
    intent: str = "register"


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat()


def _cleanup_expired() -> None:
    now = _utc_now()
    dead = [token for token, entry in pair_sessions.items() if entry.get("expires_at") and entry["expires_at"] < now]
    for token in dead:
        pair_sessions.pop(token, None)


def _resolve_public_base(request: Request) -> str:
    if PUBLIC_BASE_URL:
        return PUBLIC_BASE_URL

    forwarded_proto = request.headers.get("x-forwarded-proto")
    forwarded_host = request.headers.get("x-forwarded-host")
    scheme = forwarded_proto or request.url.scheme
    host = forwarded_host or request.url.netloc
    return f"{scheme}://{host}"


def _redirect_uri(request: Request) -> str:
    # Check module-level GOOGLE_OAUTH_REDIRECT_URI first (set from OAUTH_METHOD)
    if GOOGLE_OAUTH_REDIRECT_URI:
        return GOOGLE_OAUTH_REDIRECT_URI
    
    # Fallback to env var if not set via OAUTH_METHOD
    forced = os.getenv("GOOGLE_OAUTH_REDIRECT_URI", "").strip()
    if forced:
        return forced
    return f"{_resolve_public_base(request)}/auth/google/callback"


@app.get("/healthz")
async def healthz():
    return {"ok": True}


@app.post("/pair/create")
async def pair_create(body: PairCreateRequest, request: Request):
    _cleanup_expired()

    intent = body.intent if body.intent in ("register", "login") else "register"
    pair = secrets.token_urlsafe(24)
    expires_at = _utc_now() + timedelta(seconds=PAIR_TTL_SECONDS)

    pair_sessions[pair] = {
        "status": "pending",
        "intent": intent,
        "expires_at": expires_at,
        "profile": None,
        "tokens": None,
        "claimed": False,
    }

    base = _resolve_public_base(request)
    mobile_url = f"{base}/mobile-connect?pair={pair}"
    return {
        "pair": pair,
        "mobile_url": mobile_url,
        "expires_at": _iso(expires_at),
    }


@app.get("/mobile-connect", response_class=HTMLResponse)
async def mobile_connect(request: Request, pair: str = ""):
    _cleanup_expired()
    entry = pair_sessions.get(pair)
    if not pair or not entry:
        return HTMLResponse("<h3 style='font-family:sans-serif;padding:40px'>QR code expired. Please refresh on your main device and scan again.</h3>")

    intent = entry.get("intent", "register")
    html = f"""
<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Continue with Google</title>
<style>
body {{ font-family: Arial, sans-serif; padding: 28px; background: #0f172a; color: #e2e8f0; }}
.card {{ max-width: 420px; margin: 40px auto; background: #111827; padding: 24px; border-radius: 12px; border: 1px solid #334155; }}
.btn {{ display: block; width: 100%; text-align: center; text-decoration: none; background: #2563eb; color: white; padding: 12px; border-radius: 8px; font-weight: 600; }}
.small {{ margin-top: 12px; color: #94a3b8; font-size: 13px; line-height: 1.6; }}
</style>
</head>
<body>
  <div class='card'>
    <h2 style='margin-top:0'>Google sign-in</h2>
    <p>Continue Google sign-in from your phone.</p>
    <a class='btn' href='/auth/google/start?pair={pair}&intent={intent}'>Continue with Google</a>
    <p class='small'>After success, go back to your mirror device and continue face setup there.</p>
  </div>
</body>
</html>
"""
    return HTMLResponse(html)


@app.get("/auth/google/start")
async def auth_google_start(request: Request, pair: str = "", intent: str = "register"):
    _cleanup_expired()
    entry = pair_sessions.get(pair)
    if not entry:
        raise HTTPException(status_code=404, detail="Pair token expired")

    if entry.get("status") == "complete":
        return RedirectResponse(url="/pair-complete", status_code=302)

    if intent not in ("register", "login"):
        intent = entry.get("intent", "register")

    state = secrets.token_urlsafe(24)
    state_index[state] = pair
    redirect_uri = _redirect_uri(request)

    auth_url = build_auth_url(state=state, redirect_uri=redirect_uri)
    return RedirectResponse(url=auth_url)


@app.get("/auth/google/callback")
async def auth_google_callback(
    request: Request,
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
):
    _cleanup_expired()

    if error:
        return JSONResponse({"error": error}, status_code=400)

    if not code or not state:
        return JSONResponse({"error": "missing_code_or_state"}, status_code=400)

    pair = state_index.pop(state, "")
    entry = pair_sessions.get(pair)
    if not pair or not entry:
        return JSONResponse({"error": "pair_expired"}, status_code=400)

    try:
        tokens, profile = exchange_code_for_tokens(code, redirect_uri=_redirect_uri(request))
    except Exception as exc:
        return JSONResponse({"error": f"token_exchange_failed: {exc}"}, status_code=400)

    entry["tokens"] = tokens
    entry["profile"] = profile
    entry["status"] = "complete"

    html = """
<!doctype html>
<html>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1'>
<title>Success</title>
<style>
body { font-family: Arial, sans-serif; padding: 28px; background: #0f172a; color: #e2e8f0; }
.card { max-width: 420px; margin: 40px auto; background: #111827; padding: 24px; border-radius: 12px; border: 1px solid #334155; text-align: center; }
</style>
</head>
<body>
  <div class='card'>
    <h2 style='margin-top:0'>Done</h2>
    <p>Google sign-in completed.</p>
    <p>You can return to your mirror device now.</p>
  </div>
</body>
</html>
"""
    return HTMLResponse(html)


@app.get("/pair/status/{pair}")
async def pair_status(pair: str):
    _cleanup_expired()
    entry = pair_sessions.get(pair)
    if not entry:
        return {"status": "expired"}
    return {
        "status": entry.get("status", "pending"),
        "intent": entry.get("intent", "register"),
        "expires_at": _iso(entry["expires_at"]),
    }


@app.post("/pair/claim/{pair}")
async def pair_claim(pair: str):
    _cleanup_expired()
    entry = pair_sessions.get(pair)
    if not entry:
        raise HTTPException(status_code=404, detail="pair_expired")

    if entry.get("status") != "complete":
        raise HTTPException(status_code=409, detail="pair_not_ready")

    if entry.get("claimed"):
        raise HTTPException(status_code=409, detail="pair_already_claimed")

    profile = entry.get("profile")
    tokens = entry.get("tokens")
    if not profile or not tokens:
        raise HTTPException(status_code=500, detail="claim_payload_missing")

    entry["claimed"] = True
    pair_sessions.pop(pair, None)

    return {
        "profile": profile,
        "tokens": tokens,
    }


@app.get("/pair-complete", response_class=HTMLResponse)
async def pair_complete():
    return HTMLResponse("<h3 style='font-family:Arial,sans-serif;padding:40px'>Sign-in complete. You can return to your mirror device.</h3>")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8010")))
