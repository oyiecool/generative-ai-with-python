# environment
uv sync                          # install exactly what uv.lock specifies
uv add <pkg> / uv remove <pkg>   # change dependencies (updates the lock)
uv lock --upgrade-package <pkg>  # deliberate upgrade of one package
uv run python <script.py>        # run inside the project environment

# local models
ollama pull <model>              # download
ollama list                      # installed models
ollama ps                        # models loaded in memory
ollama create <name> -f Modelfile

# quality and security
uv run ruff check . && uv run ruff format .
uv run pytest -m "not llm"       # fast tests
uv run pytest -m llm             # tests that call models (costs money)
pre-commit run --all-files       # includes the secret scanner

# services
uv run uvicorn aikit.api:app --reload
uv run streamlit run apps/policy_chat.py
docker compose up --build
