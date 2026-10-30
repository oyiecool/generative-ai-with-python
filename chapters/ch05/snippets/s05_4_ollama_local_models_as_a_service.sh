#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
ollama create servicedesk -f Modelfile
ollama run servicedesk "How do I reset my VPN token?"
