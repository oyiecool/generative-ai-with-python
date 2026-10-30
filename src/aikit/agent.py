# src/aikit/agent.py
from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from typing import Callable

import anthropic
from pydantic import BaseModel


@dataclass
class Tool:
    name: str
    description: str
    args: type[BaseModel]
    fn: Callable[[BaseModel], dict]
    risk: str = "read"            # "read" | "write" | "external"


@dataclass
class Budget:
    max_steps: int = 10
    max_tokens: int = 50_000
    max_seconds: float = 120.0


@dataclass
class Trace:
    run_id: str = field(default_factory=lambda: uuid.uuid4().hex[:12])
    events: list[dict] = field(default_factory=list)

    def log(self, kind: str, **data):
        self.events.append({"t": round(time.time(), 3), "kind": kind, **data})


class Agent:
    def __init__(self, model: str, system: str, tools: list[Tool], budget: Budget | None = None,
                 approve: Callable[[str, dict], bool] | None = None):
        self.client = anthropic.Anthropic()
        self.model, self.system = model, system
        self.tools = {t.name: t for t in tools}
        self.budget = budget or Budget()
        self.approve = approve or (lambda name, args: False)   # default: deny risky actions

    def _specs(self):
        return [{"name": t.name, "description": t.description,
                 "input_schema": t.args.model_json_schema()} for t in self.tools.values()]

    def _execute(self, name: str, raw_args: dict, trace: Trace) -> dict:
        tool = self.tools.get(name)
        if tool is None:
            return {"error": f"unknown tool {name}"}
        try:
            args = tool.args.model_validate(raw_args)
        except Exception as e:
            trace.log("tool_rejected", tool=name, reason="invalid_args")
            return {"error": f"invalid arguments: {e}"}
        if tool.risk != "read" and not self.approve(name, args.model_dump()):
            trace.log("tool_denied", tool=name, args=args.model_dump())
            return {"error": "action not approved by a human operator"}
        try:
            result = tool.fn(args)
            trace.log("tool_ok", tool=name, args=args.model_dump())
            return result
        except Exception as e:
            trace.log("tool_error", tool=name, error=type(e).__name__)
            return {"error": "tool failed"}

    def run(self, goal: str) -> tuple[str, Trace]:
        trace, start, used = Trace(), time.time(), 0
        trace.log("start", goal=goal, model=self.model)
        messages = [{"role": "user", "content": goal}]
        for step in range(self.budget.max_steps):
            if time.time() - start > self.budget.max_seconds or used > self.budget.max_tokens:
                trace.log("stop", reason="budget")
                return "Stopped: budget exhausted. Partial findings are in the trace.", trace
            msg = self.client.messages.create(model=self.model, max_tokens=1500, system=self.system,
                                              tools=self._specs(), messages=messages)
            used += msg.usage.input_tokens + msg.usage.output_tokens
            messages.append({"role": "assistant", "content": msg.content})
            if msg.stop_reason != "tool_use":
                final = "".join(b.text for b in msg.content if b.type == "text")
                trace.log("finish", steps=step + 1, tokens=used)
                return final, trace
            results = [
                {"type": "tool_result", "tool_use_id": b.id,
                 "content": json.dumps(self._execute(b.name, b.input, trace))}
                for b in msg.content if b.type == "tool_use"
            ]
            messages.append({"role": "user", "content": results})
        trace.log("stop", reason="max_steps")
        return "Stopped: step limit reached.", trace
