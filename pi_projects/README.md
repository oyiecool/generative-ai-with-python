# Raspberry Pi projects (Part VI)

Offline generative AI projects for a Raspberry Pi 5 (8 GB recommended) running 64-bit Raspberry Pi OS. See Chapters 19–21 of the book for hardware, setup and explanations.

| Folder | Project | Chapter |
| --- | --- | --- |
| `voice/` | Push-to-talk offline voice assistant (faster-whisper, Qwen2.5 1.5B via Ollama, Piper TTS, GPIO button and LED) | 20.1 |
| `camera/` | Camera monitor that describes changes with a small vision-language model | 20.2 |
| `opsagent/` | Read-only home-lab monitoring agent with an allow-listed tool set | 20.3 |
| `kiosk/` | Offline document Q&A kiosk (local embeddings, SQLite, FastAPI) | 20.4 |
| `ops/` | Hardening script, model-hash verification, heartbeat and Ansible rollout playbook | 21 |
| `systemd/` | Unit and timer files for running the projects as services | 20–21 |

## Quick setup on the Pi

```bash
sudo apt update && sudo apt full-upgrade -y
curl -fsSL https://ollama.com/install.sh | sh        # or install from your vetted mirror
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text
cd generative-ai-with-python
uv sync --extra pi
uv run python chapters/ch19/pibench.py               # benchmark your board first
```

The camera monitor uses the system `python3-picamera2` package; create its virtual environment with `--system-site-packages`.

## Before deploying

- Run `ops/harden.sh` on each device and change the management subnet in it to yours.
- Keep AI services bound to `127.0.0.1`, run them under an unprivileged service account, and record every device in your AI system register (Chapter 21.6).
- Put a visible notice next to any device with a microphone or camera.
