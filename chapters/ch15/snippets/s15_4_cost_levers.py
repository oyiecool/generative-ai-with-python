msg = client.messages.create(
    model=s.chat_model,
    max_tokens=500,
    system=[{
        "type": "text",
        "text": LONG_POLICY_HANDBOOK + RAG_SYSTEM,         # identical on every call
        "cache_control": {"type": "ephemeral"},
    }],
    messages=[{"role": "user", "content": question}],
)
print(msg.usage.cache_creation_input_tokens, msg.usage.cache_read_input_tokens)
