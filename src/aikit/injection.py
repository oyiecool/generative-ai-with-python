# src/aikit/injection.py
import re

SUSPICIOUS = [
    r"ignore (all |any )?(previous|prior|above) (instructions|rules)",
    r"disregard (your|the) (system|previous) (prompt|instructions)",
    r"you are now\b",
    r"(reveal|print|show) (your|the) (system prompt|instructions)",
    r"<\s*/?\s*(system|assistant)\s*>",
    r"forward .{0,60} to [\w.+-]+@[\w-]+\.[\w.]+",
]
_patterns = [re.compile(p, re.I) for p in SUSPICIOUS]
INVISIBLE = re.compile("[\u200b-\u200f\u2060-\u2064\ufeff\U000e0000-\U000e007f]")


def screen(text: str) -> dict:
    hits = [p.pattern for p in _patterns if p.search(text)]
    hidden = len(INVISIBLE.findall(text))
    return {"suspicious": bool(hits) or hidden > 0, "patterns": hits, "hidden_chars": hidden}


def sanitise(text: str) -> str:
    """Remove invisible characters often used to hide instructions."""
    return INVISIBLE.sub("", text)
