#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
uv add faster-whisper piper-tts sounddevice numpy
python -m piper.download_voices en_US-lessac-medium     # downloads a voice model
