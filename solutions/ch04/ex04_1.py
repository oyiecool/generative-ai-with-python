def chat(self, messages, system=None, *, max_tokens=None, temperature=None,
         stop: list[str] | None = None) -> ChatResult:
    ...
    if self.provider == "anthropic":
        if stop:
            kwargs["stop_sequences"] = stop          # Anthropic name
        r = self._client.messages.create(**kwargs)
        ...
    extra = {"stop": stop} if stop else {}            # OpenAI-compatible name
    r = self._client.chat.completions.create(model=self.model, messages=msgs,
                                             temperature=temperature,
                                             **{token_arg: max_tokens}, **extra)
