#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
hailo-ollama &
curl -s http://localhost:8000/hailo/v1/list
curl -s http://localhost:8000/api/pull -H 'Content-Type: application/json' \
       -d '{"model": "qwen2:1.5b", "stream": true}'
