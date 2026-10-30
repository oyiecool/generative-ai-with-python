# src/aikit/failover.py
import logging

from aikit.llm import LLM, ChatResult

log = logging.getLogger(__name__)


class FailoverLLM:
    """Try models in order; each must have passed the same evaluation gate."""

    def __init__(self, chain: list[tuple[str, str]]):
        self.chain = [LLM(provider=p, model=m) for p, m in chain]

    def chat(self, *args, **kwargs) -> ChatResult:
        last_exc = None
        for llm in self.chain:
            try:
                return llm.chat(*args, **kwargs)
            except Exception as e:                       # narrow this to retryable errors
                log.warning("model failed, falling back",
                            extra={"provider": llm.provider, "model": llm.model,
                                   "error": type(e).__name__})
                last_exc = e
        raise RuntimeError("all models failed") from last_exc
