#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
sudo apt install -y python3-picamera2          # system package; create the venv with --system-site-packages
ollama pull moondream                          # ~1.8B vision-language model
uv add ollama pydantic
