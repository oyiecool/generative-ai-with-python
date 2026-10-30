#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
uv run uvicorn pi_projects.kiosk.app:app --host 127.0.0.1 --port 8000
chromium-browser --kiosk --noerrdialogs --disable-infobars http://127.0.0.1:8000
