#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
ollama pull llama3.2        # or any small instruction-tuned model in the Ollama library
ollama pull nomic-embed-text  # a local embedding model for Chapter 8
ollama list
ollama run llama3.2 "In one sentence, what is a change advisory board?"
