# src/aikit/structured.py
import json
import re
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from aikit.llm import LLM, Message

T = TypeVar("T", bound=BaseModel)


class ExtractionError(RuntimeError):
    pass


def _first_json_object(text: str) -> str:
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        raise ValueError("no JSON object found")
    return m.group(0)


def extract(llm: LLM, schema: type[T], text: str, instructions: str, max_attempts: int = 3) -> T:
    system = (
        f"{instructions}\nReturn ONLY a JSON object that matches this JSON Schema:\n"
        f"{json.dumps(schema.model_json_schema())}"
    )
    messages = [Message("user", f"<input>\n{text}\n</input>")]
    last_error = ""
    for attempt in range(1, max_attempts + 1):
        r = llm.chat(messages, system=system, temperature=0)
        try:
            return schema.model_validate_json(_first_json_object(r.text))
        except (ValueError, ValidationError) as e:
            last_error = str(e)
            messages += [
                Message("assistant", r.text),
                Message("user", f"That output was invalid:\n{last_error}\nReturn corrected JSON only."),
            ]
    raise ExtractionError(f"failed after {max_attempts} attempts: {last_error}")
