# Generative AI with Python — companion code

Supplemental code and exercise scripts for the book **_Generative AI with Python: Build, Deploy and Govern Intelligent Applications_** by Ronald Allan V. Tomimbang.

Every code listing in the book is here, organised by chapter, together with the worked exercise solutions from Appendix D and the Raspberry Pi projects from Part VI.

## Repository layout

| Path | What it holds |
| --- | --- |
| `src/aikit/` | The reusable library built up through the book: settings, the provider-agnostic LLM client, prompts, structured output, embeddings, retrieval, RAG, agents, the API service, evaluation, telemetry, security and governance helpers |
| `chapters/chNN/` | Runnable chapter scripts named as in the book (for example `chapters/ch02/smoke_test.py`) |
| `chapters/chNN/snippets/` | Shorter listings, named after the book section they come from (for example `s04_5_streaming.py`). Many build on earlier code in the chapter, so read them alongside the text |
| `solutions/chNN/` | Worked solutions from Appendix D, named `exCC_N` for chapter CC, exercise N |
| `apps/` | Streamlit and Gradio front ends (Chapter 12) |
| `prompts/` | Versioned prompt templates (Chapter 6) |
| `evals/` | Evaluation and red-team sets (Chapters 14 and 16) |
| `tests/` | Prompt tests run with pytest (Chapter 14) |
| `governance/` | AI system register entries (Chapter 17) |
| `pi_projects/` | Raspberry Pi 5 projects and fleet tooling (Chapters 20 and 21) — see [`pi_projects/README.md`](pi_projects/README.md) |
| `Dockerfile`, `.github/workflows/eval.yml`, `.pre-commit-config.yaml`, `.env.example` | Packaging, CI evaluation gate, secret scanning and configuration (Chapters 2, 12 and 14) |

## Chapter map

| Part | Chapters | Main code |
| --- | --- | --- |
| I. Foundations | 1–3 | `chapters/ch01/markov.py`, `chapters/ch02/smoke_test.py`, `src/aikit/settings.py`, `chapters/ch03/*` |
| II. Working with Models | 4–7 | `src/aikit/llm.py`, `chapters/ch05/*`, `src/aikit/prompts.py`, `src/aikit/structured.py`, `chapters/ch07/tools_demo.py` |
| III. Building Applications | 8–13 | `src/aikit/{embed,vectorindex,chunking,loaders,ingest,rag,agent,api,security}.py`, `chapters/ch11/vision.py`, `chapters/ch13/*` |
| IV. Production | 14–15 | `tests/`, `src/aikit/{judge,evalgate,failover,telemetry}.py` |
| V. Governance and Responsible AI | 16–18 | `src/aikit/{injection,register,changepack}.py`, `evals/redteam.yaml`, `chapters/ch18/counterfactual.py` |
| VI. Generative AI at the Edge with Raspberry Pi | 19–21 | `chapters/ch19/pibench.py`, `pi_projects/*` |

## Getting started

```bash
# Python 3.12+ and uv (https://docs.astral.sh/uv/)
git clone https://github.com/oyiecool/generative-ai-with-python
cd generative-ai-with-python
uv sync                       # core dependencies
uv sync --extra rag --extra api   # add extras as you reach later chapters
cp .env.example .env          # then fill in keys and model names — never commit .env
uv run python chapters/ch02/smoke_test.py
```

Extras: `models`, `rag`, `multimodal`, `api`, `finetune`, `ops`, `security`, `mcp` and `pi` (install the last one on the Raspberry Pi).

Model names are never hard-coded: set `AIKIT_PROVIDER` and `AIKIT_CHAT_MODEL` in `.env` to your provider's current recommended model, or to a local Ollama model such as `llama3.2` or `qwen2.5:1.5b`.

## Notes

- **Shell listings** that appear in the book as terminal sessions (`$ command`) are stored as `.sh` files with the prompts removed and command output commented out. Read and run them one command at a time rather than executing a whole file.
- **Some modules are completed by the chapter projects.** For example `aikit.rag.stream_answer`, `aikit.router` and `aikit.evalrun` are project exercises; the book describes what they must do.
- **Tests marked `llm`** call real models and cost money. Run them deliberately with `uv run pytest -m llm`; the default suite is `uv run pytest -m "not llm"`.
- **Security.** Keep API keys in `.env` or a secrets manager. The pre-commit configuration runs gitleaks to catch accidental commits of secrets.
