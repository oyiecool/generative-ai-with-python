# src/aikit/loaders.py
from pathlib import Path


def load_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".pdf":
        from pypdf import PdfReader                       # uv add pypdf
        pages = PdfReader(path).pages
        return "\n\n".join(f"[page {i + 1}]\n{p.extract_text() or ''}" for i, p in enumerate(pages))
    if suffix == ".docx":
        from docx import Document                         # uv add python-docx
        doc = Document(path)
        lines = []
        for p in doc.paragraphs:
            style = p.style.name.lower()
            if style.startswith("heading"):
                level = int(style.split()[-1]) if style.split()[-1].isdigit() else 1
                lines.append("#" * level + " " + p.text)
            else:
                lines.append(p.text)
        return "\n\n".join(lines)
    raise ValueError(f"unsupported file type: {suffix}")
