# src/aikit/llm.py
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Iterator, Literal

from aikit.settings import get_settings

Role = Literal["user", "assistant"]


@dataclass
class Message:
    role: Role
    content: str


@dataclass
class ChatResult:
    text: str
    model: str
    provider: str
    input_tokens: int | None
    output_tokens: int | None
    stop_reason: str | None
    latency_s: float
    raw: object = field(repr=False, default=None)


class LLM:
    def __init__(self, provider: str | None = None, model: str | None = None):
        s = get_settings()
        self.provider = provider or s.provider
        self.model = model or s.chat_model
        self.max_tokens = s.max_output_tokens
        self.temperature = s.temperature
        self.timeout = s.request_timeout_s
        self._client = self._make_client()

    def _make_client(self):
        if self.provider == "anthropic":
            import anthropic
            return anthropic.Anthropic(timeout=self.timeout, max_retries=3)
        from openai import OpenAI
        if self.provider == "ollama":
            import os
            host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
            return OpenAI(base_url=f"{host}/v1", api_key="ollama", timeout=self.timeout)
        return OpenAI(timeout=self.timeout, max_retries=3)

    def chat(
        self,
        messages: list[Message] | str,
        system: str | None = None,
        *,
        max_tokens: int | None = None,
        temperature: float | None = None,
    ) -> ChatResult:
        if isinstance(messages, str):
            messages = [Message("user", messages)]
        max_tokens = max_tokens or self.max_tokens
        temperature = self.temperature if temperature is None else temperature
        start = time.perf_counter()

        if self.provider == "anthropic":
            kwargs = dict(
                model=self.model, max_tokens=max_tokens, temperature=temperature,
                messages=[{"role": m.role, "content": m.content} for m in messages],
            )
            if system:
                kwargs["system"] = system
            r = self._client.messages.create(**kwargs)
            text = "".join(b.text for b in r.content if b.type == "text")
            return ChatResult(text, self.model, self.provider, r.usage.input_tokens,
                              r.usage.output_tokens, r.stop_reason,
                              time.perf_counter() - start, r)

        msgs = ([{"role": "system", "content": system}] if system else []) + [
            {"role": m.role, "content": m.content} for m in messages
        ]
        token_arg = "max_tokens" if self.provider == "ollama" else "max_completion_tokens"
        r = self._client.chat.completions.create(
            model=self.model, messages=msgs, temperature=temperature, **{token_arg: max_tokens}
        )
        u = r.usage
        return ChatResult(r.choices[0].message.content or "", self.model, self.provider,
                          u.prompt_tokens if u else None, u.completion_tokens if u else None,
                          r.choices[0].finish_reason, time.perf_counter() - start, r)

    def stream(self, prompt: str, system: str | None = None) -> Iterator[str]:
        if self.provider == "anthropic":
            kw = {"system": system} if system else {}
            with self._client.messages.stream(
                model=self.model, max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}], **kw,
            ) as st:
                yield from st.text_stream
            return
        msgs = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": prompt}
        ]
        for ch in self._client.chat.completions.create(
            model=self.model, messages=msgs, stream=True
        ):
            if ch.choices and ch.choices[0].delta.content:
                yield ch.choices[0].delta.content
