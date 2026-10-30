#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
uv add faster-whisper piper-tts sounddevice numpy gpiozero ollama
ollama pull qwen2.5:1.5b          # supports tool calling
