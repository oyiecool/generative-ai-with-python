# chapters/ch13/prepare.py
import hashlib
import json
import random
import re
from pathlib import Path

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")


def scrub(text: str) -> str:
    return IPV4.sub("<IP>", EMAIL.sub("<EMAIL>", text))


def load(path: Path) -> list[dict]:
    rows, seen = [], set()
    for line in path.read_text(encoding="utf-8").splitlines():
        ex = json.loads(line)
        for m in ex["messages"]:
            m["content"] = scrub(m["content"]).strip()
        key = hashlib.sha1(json.dumps(ex["messages"][1:], sort_keys=True).encode()).hexdigest()
        if key in seen or not ex["messages"][-1]["content"]:
            continue
        seen.add(key)
        rows.append(ex)
    return rows


rows = load(Path("data/cab_examples.jsonl"))
random.Random(7).shuffle(rows)
cut = int(len(rows) * 0.9)
for name, part in (("train", rows[:cut]), ("eval", rows[cut:])):
    Path(f"data/cab_{name}.jsonl").write_text("\n".join(json.dumps(r) for r in part), encoding="utf-8")
print(f"{cut} train / {len(rows) - cut} eval")
