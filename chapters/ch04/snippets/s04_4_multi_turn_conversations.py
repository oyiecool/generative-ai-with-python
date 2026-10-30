history = []

def ask(text: str) -> str:
    history.append({"role": "user", "content": text})
    msg = client.messages.create(
        model=s.chat_model, max_tokens=400, system="You are a helpful SRE.", messages=history
    )
    reply = "".join(b.text for b in msg.content if b.type == "text")
    history.append({"role": "assistant", "content": reply})
    return reply

print(ask("Our nightly backup job failed with exit code 23. What does that usually mean for rsync?"))
print(ask("How do I see which files caused it?"))   # 'it' resolves from history
