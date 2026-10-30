import json

import httpx

with httpx.stream("POST", "http://localhost:8000/v1/ask/stream", json={"question": q},
                  headers={"Authorization": f"Bearer {token}"}, timeout=None) as r:
    event = None
    for line in r.iter_lines():
        if line.startswith("event:"):
            event = line.split(":", 1)[1].strip()
        elif line.startswith("data:"):
            data = json.loads(line.split(":", 1)[1])
            if event == "token":
                print(data["text"], end="", flush=True)
            elif event == "done":
                break
