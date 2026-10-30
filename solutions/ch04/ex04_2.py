import anthropic
import openai


class ContextTooLongError(ValueError):
    pass


_LENGTH_HINTS = ("prompt is too long", "context length", "maximum context", "too many tokens")


def _raise_if_too_long(exc: Exception) -> None:
    if any(h in str(exc).lower() for h in _LENGTH_HINTS):
        raise ContextTooLongError(str(exc)) from exc
    raise exc

# inside chat():
try:
    r = self._client.messages.create(**kwargs)
except (anthropic.BadRequestError, openai.BadRequestError) as e:
    _raise_if_too_long(e)
