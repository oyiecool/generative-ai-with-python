#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
sudo apt install -y git cmake build-essential
git clone https://github.com/ggml-org/llama.cpp && cd llama.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release && cmake --build build -j4
./build/bin/llama-server -m ~/models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
      -c 4096 -t 4 --host 127.0.0.1 --port 8081
