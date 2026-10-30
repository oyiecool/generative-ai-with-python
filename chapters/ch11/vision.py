# chapters/ch11/vision.py
import base64
import mimetypes
from pathlib import Path

import anthropic
from openai import OpenAI


def b64(path: Path) -> tuple[str, str]:
    media = mimetypes.guess_type(path)[0] or "image/png"
    return media, base64.standard_b64encode(path.read_bytes()).decode()


def describe_claude(path: Path, question: str, model: str) -> str:
    media, data = b64(path)
    msg = anthropic.Anthropic().messages.create(
        model=model, max_tokens=600,
        messages=[{"role": "user", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": media, "data": data}},
            {"type": "text", "text": question},
        ]}],
    )
    return "".join(b.text for b in msg.content if b.type == "text")


def describe_openai(path: Path, question: str, model: str) -> str:
    media, data = b64(path)
    r = OpenAI().chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": [
            {"type": "text", "text": question},
            {"type": "image_url", "image_url": {"url": f"data:{media};base64,{data}"}},
        ]}],
    )
    return r.choices[0].message.content


print(describe_claude(Path("data/grafana_cpu.png"),
                      "Which host has the highest CPU in this dashboard, and when did it spike?",
                      model=s.chat_model))
