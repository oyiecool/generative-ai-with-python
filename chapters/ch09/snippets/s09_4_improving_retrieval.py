REWRITE = """Rewrite the user's latest question as a standalone search query for a
corporate knowledge base. Expand acronyms you are sure of. Return only the query."""

def rewrite(history: list[Message], question: str, fast_llm) -> str:
    convo = "\n".join(f"{m.role}: {m.content}" for m in history[-6:])
    return fast_llm.chat(f"{convo}\nuser: {question}", system=REWRITE, temperature=0).text.strip()
