#!/usr/bin/env bash
# Commands from the book; run them one at a time and read each before running.
docker run -d --name jaeger -p 16686:16686 -p 4317:4317 jaegertracing/all-in-one:latest
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
export OTEL_EXPORTER_OTLP_INSECURE=true
uv run uvicorn aikit.api:app
# send a few questions, then open http://localhost:16686 and search service "policy-assistant"
