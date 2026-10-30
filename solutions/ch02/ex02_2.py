import anthropic

try:
    text, usage = run_anthropic(s.chat_model)
except anthropic.AuthenticationError:
    raise SystemExit("Authentication failed: check that ANTHROPIC_API_KEY is set and active.")
