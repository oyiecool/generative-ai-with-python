# src/aikit/chunking.py
import re
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    meta: dict


def chunk_markdown(doc: str, source: str, max_chars: int = 2400, overlap: int = 300) -> list[Chunk]:
    """Split Markdown by headings, then by paragraphs, carrying the heading path."""
    chunks, path = [], []
    for block in re.split(r"(?m)^(?=#{1,4} )", doc):
        if not block.strip():
            continue
        first = block.splitlines()[0]
        if first.startswith("#"):
            level = len(first) - len(first.lstrip("#"))
            path = path[: level - 1] + [first.lstrip("# ").strip()]
        heading = " > ".join(path)
        buf = ""
        for para in block.split("\n\n"):
            if len(buf) + len(para) > max_chars and buf:
                chunks.append(Chunk(f"{heading}\n\n{buf.strip()}", {"source": source, "heading": heading}))
                buf = buf[-overlap:]
            buf += para + "\n\n"
        if buf.strip():
            chunks.append(Chunk(f"{heading}\n\n{buf.strip()}", {"source": source, "heading": heading}))
    return chunks
