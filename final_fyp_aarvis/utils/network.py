"""Network helpers."""

from __future__ import annotations

import socket


def detect_lan_ip() -> str:
    """Detect LAN IP address."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        lan_ip = sock.getsockname()[0]
        sock.close()
        return lan_ip
    except Exception:
        return "<could not detect>"
