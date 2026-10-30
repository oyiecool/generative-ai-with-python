#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
uv init aikit --package --python 3.13 && cd aikit
uv add ollama openai pydantic pydantic-settings httpx rich psutil
