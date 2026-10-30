# Anthropic
with client.messages.stream(
    model=s.chat_model, max_tokens=600,
    messages=[{"role": "user", "content": "Explain RAID 6 to a new engineer."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
    final = stream.get_final_message()
print("\n", final.usage)

# OpenAI-compatible
for chunk in oa_client.chat.completions.create(
    model=s.chat_model, stream=True,
    messages=[{"role": "user", "content": "Explain RAID 6 to a new engineer."}],
):
    delta = chunk.choices[0].delta.content if chunk.choices else None
    if delta:
        print(delta, end="", flush=True)
