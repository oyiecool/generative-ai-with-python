# chapters/ch02/smoke_test.py
import time

from rich import print

from aikit.settings import get_settings

PROMPT = "Reply with exactly: workbench ready"


def run_anthropic(model: str) -> tuple[str, dict]:
    import anthropic

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=model,
        max_tokens=50,
        messages=[{"role": "user", "content": PROMPT}],
    )
    text = "".join(b.text for b in msg.content if b.type == "text")
    return text, {"in": msg.usage.input_tokens, "out": msg.usage.output_tokens}


def run_openai(model: str) -> tuple[str, dict]:
    from openai import OpenAI

    client = OpenAI()
    resp = client.chat.completions.create(
        model=model,
        max_tokens=50,
        messages=[{"role": "user", "content": PROMPT}],
    )
    u = resp.usage
    return resp.choices[0].message.content, {"in": u.prompt_tokens, "out": u.completion_tokens}


def run_ollama(model: str) -> tuple[str, dict]:
    import ollama

    resp = ollama.chat(model=model, messages=[{"role": "user", "content": PROMPT}])
    return resp["message"]["content"], {
        "in": resp.get("prompt_eval_count"),
        "out": resp.get("eval_count"),
    }


RUNNERS = {"anthropic": run_anthropic, "openai": run_openai, "ollama": run_ollama}

if __name__ == "__main__":
    s = get_settings()
    start = time.perf_counter()
    text, usage = RUNNERS[s.provider](s.chat_model)
    elapsed = time.perf_counter() - start
    print(f"[bold]{s.provider}[/] / {s.chat_model}")
    print(f"answer : {text!r}")
    print(f"tokens : {usage}")
    print(f"latency: {elapsed:.2f}s")
