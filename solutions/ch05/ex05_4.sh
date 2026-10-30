#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
ollama serve &                       # if the desktop app is not running
AIKIT_PROVIDER=ollama AIKIT_CHAT_MODEL=llama3.2 uv run python chapters/ch02/smoke_test.py
