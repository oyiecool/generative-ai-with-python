#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
uv add vllm   # Linux with a supported GPU
vllm serve Qwen/Qwen2.5-7B-Instruct --max-model-len 16384 --api-key "$VLLM_KEY"
