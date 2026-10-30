#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
python - <<'EOF'
# output: import hashlib, json, pathlib
# output: files = {}
# output: for p in pathlib.Path("/usr/share/ollama/.ollama/models/blobs").glob("sha256-*"):
# output:     files[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
# output: pathlib.Path("/etc/aikit/model-hashes.json").write_text(json.dumps(files, indent=2))
# output: EOF
sudo systemctl edit voice-assistant      # add: ExecStartPre=/opt/aikit/.venv/bin/python /opt/aikit/pi_projects/ops/verify_models.py
sudo cp blob blob.bak && echo x | sudo tee -a blob >/dev/null    # corrupt a copy under test
sudo systemctl restart voice-assistant; systemctl status voice-assistant
# status shows ExecStartPre failed: "MODEL INTEGRITY FAILURE"
sudo mv blob.bak blob && sudo systemctl restart voice-assistant
