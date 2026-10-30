from io import BytesIO
from pathlib import Path

from PIL import Image


def resized_copy(path: Path, width: int) -> Path:
    img = Image.open(path)
    img.thumbnail((width, width * 10))            # keep aspect ratio
    out = path.with_name(f"{path.stem}_{width}.png")
    img.save(out)
    return out

for p in (Path("data/dashboard.png"), resized_copy(Path("data/dashboard.png"), 1024)):
    msg = describe_claude_raw(p, "Which host has the highest CPU and when did it spike?")
    print(p.name, msg.usage.input_tokens, msg.content[0].text[:120])
