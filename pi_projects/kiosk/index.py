# pi_projects/kiosk/index.py — build the index once, or when documents change
import sqlite3
import sys
from pathlib import Path

import numpy as np
import ollama

from aikit.chunking import chunk_markdown          # Chapter 8

DB = Path("/var/lib/kiosk/index.db")
EMBED = "nomic-embed-text"


def build(folder: Path) -> None:
    DB.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB)
    con.execute("DROP TABLE IF EXISTS chunks")
    con.execute("CREATE TABLE chunks (id TEXT PRIMARY KEY, source TEXT, heading TEXT, body TEXT, vec BLOB)")
    for path in sorted(folder.glob("*.md")):
        chunks = chunk_markdown(path.read_text(encoding="utf-8"), source=path.name, max_chars=1200)
        vecs = ollama.embed(model=EMBED, input=["search_document: " + c.text for c in chunks])["embeddings"]
        for i, (c, v) in enumerate(zip(chunks, vecs)):
            v = np.asarray(v, dtype=np.float32)
            con.execute("INSERT INTO chunks VALUES (?,?,?,?,?)",
                        (f"{path.name}#{i}", c.meta["source"], c.meta["heading"], c.text,
                         (v / np.linalg.norm(v)).tobytes()))
    con.commit()


if __name__ == "__main__":
    build(Path(sys.argv[1]))
