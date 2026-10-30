# chapters/ch04/claude_basic.py
import anthropic

from aikit.settings import get_settings

s = get_settings()
client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY

msg = client.messages.create(
    model=s.chat_model,
    max_tokens=400,
    temperature=0.2,
    system="You are a senior Unix administrator. Answer concisely and flag risky commands.",
    messages=[
        {"role": "user", "content": "How do I find which process is listening on port 8443?"}
    ],
)

for block in msg.content:
    if block.type == "text":
        print(block.text)
print(msg.stop_reason, msg.usage.input_tokens, msg.usage.output_tokens)
