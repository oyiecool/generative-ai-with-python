# src/aikit/prompts.py
from dataclasses import dataclass
from pathlib import Path

import yaml
from jinja2 import Environment, StrictUndefined

PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts"
_env = Environment(undefined=StrictUndefined, autoescape=False, keep_trailing_newline=True)


@dataclass
class Prompt:
    name: str
    version: int
    meta: dict
    template: str

    def render(self, **values) -> str:
        return _env.from_string(self.template).render(**values)


def load_prompt(name: str, version: int | None = None) -> Prompt:
    files = sorted(PROMPT_DIR.glob(f"{name}.v*.jinja"),
                   key=lambda p: int(p.stem.split(".v")[-1]))
    if version is not None:
        files = [f for f in files if f.stem.endswith(f".v{version}")]
    if not files:
        raise FileNotFoundError(f"No prompt {name} v{version}")
    raw = files[-1].read_text(encoding="utf-8")
    _, front, body = raw.split("---", 2)
    meta = yaml.safe_load(front)
    return Prompt(meta["name"], meta["version"], meta, body.lstrip())
