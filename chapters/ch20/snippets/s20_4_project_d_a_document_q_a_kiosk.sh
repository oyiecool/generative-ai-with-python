#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
ollama pull nomic-embed-text
ollama pull qwen2.5:1.5b
uv add ollama numpy fastapi "uvicorn[standard]"
