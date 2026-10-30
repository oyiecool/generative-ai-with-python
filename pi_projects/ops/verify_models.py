# pi_projects/ops/verify_models.py — run at boot before AI services start
import hashlib
import json
import sys
from pathlib import Path

ALLOWED = json.loads(Path("/etc/aikit/model-hashes.json").read_text())   # {"path": "sha256"}

bad = []
for path, expected in ALLOWED.items():
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    if h.hexdigest() != expected:
        bad.append(path)

if bad:
    print("MODEL INTEGRITY FAILURE:", bad, file=sys.stderr)
    sys.exit(1)        # a systemd ExecStartPre failure stops the AI service from starting
print("All model files verified.")
