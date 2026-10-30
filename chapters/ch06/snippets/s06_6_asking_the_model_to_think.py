SYSTEM = """Diagnose the incident from the log excerpt.
First think step by step inside <analysis> tags.
Then give the most likely root cause and one next action inside <answer> tags."""

import re

def extract(tag: str, text: str) -> str | None:
    m = re.search(fr"<{tag}>(.*?)</{tag}>", text, re.S)
    return m.group(1).strip() if m else None

r = llm.chat(f"<logs>{log_excerpt}</logs>", system=SYSTEM, max_tokens=1200)
print(extract("answer", r.text))
