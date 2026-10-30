# src/aikit/ingest.py
import hashlib
import json
from pathlib import Path

from aikit.chunking import chunk_markdown
from aikit.loaders import load_text

STATE = Path("data/ingest_state.json")


def ingest_folder(folder: Path, index, acl_group: str) -> dict:
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    seen, stats = set(), {"added": 0, "skipped": 0, "removed": 0}
    for path in sorted(folder.rglob("*")):
        if path.suffix.lower() not in {".md", ".txt", ".pdf", ".docx"}:
            continue
        key = str(path.relative_to(folder))
        seen.add(key)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if state.get(key) == digest:
            stats["skipped"] += 1
            continue
        index.delete(source=key)                           # replace old chunks
        chunks = chunk_markdown(load_text(path), source=key)
        index.add([f"{key}#{i}" for i in range(len(chunks))], [c.text for c in chunks],
                  [{**c.meta, "acl_group": acl_group} for c in chunks])
        state[key] = digest
        stats["added"] += 1
    for gone in set(state) - seen:
        index.delete(source=gone)
        del state[gone]
        stats["removed"] += 1
    STATE.write_text(json.dumps(state, indent=2))
    return stats
