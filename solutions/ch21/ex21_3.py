from datetime import datetime, timedelta, timezone

APPROVED_MODELS = {"qwen2.5:1.5b", "nomic-embed-text:latest"}


def alerts(latest: dict[str, dict], history: dict[str, list[dict]]) -> list[str]:
    out, now = [], datetime.now(timezone.utc)
    for device, hb in latest.items():
        if now - datetime.fromisoformat(hb["ts"]) > timedelta(minutes=15):
            out.append(f"{device}: no heartbeat for 15 min")
        recent = history[device][-6:]                         # last 30 min
        if len(recent) == 6 and all(h["throttled"] != "throttled=0x0" for h in recent):
            out.append(f"{device}: throttled for 30 min")
        if hb["disk_used_pct"] > 85:
            out.append(f"{device}: disk {hb['disk_used_pct']}%")
        unknown = set(hb["models"]) - APPROVED_MODELS
        if unknown:
            out.append(f"{device}: unregistered models {sorted(unknown)}")
        down = [s for s, st in hb["services"].items() if st != "active"]
        if down:
            out.append(f"{device}: services not active {down}")
    return out
