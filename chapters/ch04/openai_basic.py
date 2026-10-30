# chapters/ch04/openai_basic.py
from openai import OpenAI

from aikit.settings import get_settings

s = get_settings()
client = OpenAI()   # reads OPENAI_API_KEY

resp = client.chat.completions.create(
    model=s.chat_model,
    max_completion_tokens=400,
    messages=[
        {"role": "system", "content": "You are a senior Unix administrator. Answer concisely."},
        {"role": "user", "content": "How do I find which process is listening on port 8443?"},
    ],
)
choice = resp.choices[0]
print(choice.message.content)
print(choice.finish_reason, resp.usage.prompt_tokens, resp.usage.completion_tokens)

# The same client talking to a local Ollama server:
local = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")  # key is ignored
