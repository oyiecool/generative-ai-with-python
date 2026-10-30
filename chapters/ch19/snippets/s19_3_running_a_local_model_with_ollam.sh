#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
curl -fsSL https://ollama.com/install.sh | sh     # or install from your vetted mirror
ollama pull gemma3:1b
ollama pull qwen2.5:1.5b
ollama run qwen2.5:1.5b "Explain swap memory in two sentences."
