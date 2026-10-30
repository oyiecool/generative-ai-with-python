import argparse

from aikit.settings import Settings

parser = argparse.ArgumentParser()
parser.add_argument("--provider", choices=["anthropic", "openai", "ollama"])
parser.add_argument("--model")
args = parser.parse_args()

overrides = {k: v for k, v in {"provider": args.provider, "chat_model": args.model}.items() if v}
s = Settings(**overrides)          # explicit arguments take priority over environment variables
text, usage = RUNNERS[s.provider](s.chat_model)
