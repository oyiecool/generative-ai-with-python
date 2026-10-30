import hashlib
import json


def cache_key(prompt_name: str, prompt_version: int, model: str, groups: list[str],
              question: str, kb_version: str) -> str:
    blob = json.dumps([prompt_name, prompt_version, model, sorted(groups),
                       question.strip().lower(), kb_version])
    return hashlib.sha256(blob.encode()).hexdigest()
