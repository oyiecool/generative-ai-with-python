#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
uv tool install pre-commit && pre-commit install
# The fake key is assembled at run time so this repository itself contains no key-shaped string.
FAKE="sk-test-$(printf '1234567890abcdef%.0s' 1 2)"
echo "OPENAI_API_KEY=\"$FAKE\"" > leak.py
git add leak.py && git commit -m "test"
# gitleaks reports the secret and the commit is blocked
git restore --staged leak.py && rm leak.py
