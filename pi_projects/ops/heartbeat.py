# pi_projects/ops/heartbeat.py — run every 5 minutes from a systemd timer
import json
import os
import platform
import shutil
import socket
import subprocess
from datetime import datetime, timezone

import httpx

COLLECTOR = os.environ["HEARTBEAT_URL"]          # internal HTTPS endpoint
TOKEN = open(os.environ["CREDENTIALS_DIRECTORY"] + "/heartbeat-token").read().strip()


def sh(*cmd: str) -> str:
    return subprocess.run(cmd, capture_output=True, text=True).stdout.strip()


models = [m.split()[0] for m in sh("ollama", "list").splitlines()[1:]]
du = shutil.disk_usage("/")
payload = {
    "device": socket.gethostname(),
    "ts": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    "kernel": platform.release(),
    "temp": sh("vcgencmd", "measure_temp"),
    "throttled": sh("vcgencmd", "get_throttled"),
    "disk_used_pct": round(du.used / du.total * 100, 1),
    "models": models,
    "services": {s: sh("systemctl", "is-active", s) for s in ("ollama", "voice-assistant")},
}
httpx.post(COLLECTOR, json=payload, headers={"Authorization": f"Bearer {TOKEN}"}, timeout=10)
