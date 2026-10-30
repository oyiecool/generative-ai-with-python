#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

uv --version
uv init aikit --package --python 3.12
cd aikit
