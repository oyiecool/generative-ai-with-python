# chapters/ch07/tools_demo.py
import json
import subprocess

import anthropic
from pydantic import BaseModel, Field


class DiskUsageArgs(BaseModel):
    path: str = Field(description="Absolute path to check, e.g. /var")


class ServiceStatusArgs(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z0-9_.@-]+$", description="systemd unit name")


ALLOWED_PATHS = {"/", "/var", "/home", "/tmp"}


def disk_usage(args: DiskUsageArgs) -> dict:
    if args.path not in ALLOWED_PATHS:
        return {"error": f"path not permitted: {args.path}"}
    out = subprocess.run(["df", "-h", args.path], capture_output=True, text=True, timeout=5)
    return {"output": out.stdout}


def service_status(args: ServiceStatusArgs) -> dict:
    out = subprocess.run(["systemctl", "is-active", args.name],
                         capture_output=True, text=True, timeout=5)
    return {"active": out.stdout.strip()}


TOOLS = {
    "disk_usage": (DiskUsageArgs, disk_usage, "Show disk usage for an allowed path."),
    "service_status": (ServiceStatusArgs, service_status, "Check whether a systemd service is active."),
}
TOOL_SPECS = [
    {"name": n, "description": d, "input_schema": a.model_json_schema()}
    for n, (a, _, d) in TOOLS.items()
]


def run(question: str, model: str, max_steps: int = 6) -> str:
    client = anthropic.Anthropic()
    messages = [{"role": "user", "content": question}]
    for _ in range(max_steps):
        msg = client.messages.create(model=model, max_tokens=800, tools=TOOL_SPECS,
                                     system="You are a read-only server diagnostics assistant.",
                                     messages=messages)
        messages.append({"role": "assistant", "content": msg.content})
        if msg.stop_reason != "tool_use":
            return "".join(b.text for b in msg.content if b.type == "text")
        results = []
        for block in msg.content:
            if block.type != "tool_use":
                continue
            args_model, fn, _ = TOOLS[block.name]
            try:
                output = fn(args_model.model_validate(block.input))
            except Exception as e:           # validation or execution failure
                output = {"error": str(e)}
            results.append({"type": "tool_result", "tool_use_id": block.id,
                            "content": json.dumps(output)})
        messages.append({"role": "user", "content": results})
    return "Stopped: step limit reached."


if __name__ == "__main__":
    print(run("Is nginx running, and is /var close to full?", model=s.chat_model))
