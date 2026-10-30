# pi_projects/opsagent/agent.py
import json
import shutil
import socket
import subprocess
from datetime import datetime
from pathlib import Path

import ollama

MODEL = "qwen2.5:3b"           # better tool use; slower but this runs unattended
HOSTS = {"nas": "192.168.1.20", "router": "192.168.1.1", "printer": "192.168.1.30"}
SERVICES = {"ollama", "ssh", "docker"}
PORTS = {("nas", 445), ("nas", 22), ("router", 443)}


def ping_host(name: str) -> str:
    """Ping a known host by name (nas, router or printer) and report if it is reachable."""
    ip = HOSTS.get(name)
    if not ip:
        return f"unknown host {name}"
    ok = subprocess.run(["ping", "-c", "2", "-W", "2", ip], capture_output=True).returncode == 0
    return f"{name} ({ip}) is {'reachable' if ok else 'UNREACHABLE'}"


def check_port(name: str, port: int) -> str:
    """Check whether an allowed TCP port on a known host accepts connections."""
    if (name, int(port)) not in PORTS:
        return "port check not permitted"
    try:
        with socket.create_connection((HOSTS[name], int(port)), timeout=3):
            return f"{name}:{port} open"
    except OSError:
        return f"{name}:{port} CLOSED"


def service_status(name: str) -> str:
    """Report whether an allowed systemd service on this Pi is active."""
    if name not in SERVICES:
        return "service not permitted"
    out = subprocess.run(["systemctl", "is-active", name], capture_output=True, text=True)
    return f"{name}: {out.stdout.strip()}"


def local_health() -> str:
    """Report this Pi's temperature, throttling flags and disk usage."""
    t = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True).stdout.strip()
    th = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True, text=True).stdout.strip()
    du = shutil.disk_usage("/")
    return f"{t}; {th}; disk {du.used / du.total:.0%} used"


TOOLS = {f.__name__: f for f in (ping_host, check_port, service_status, local_health)}
SYSTEM = ("You are a read-only home-lab monitoring agent. Use the tools to check every host, "
          "allowed port and service, then write a status report in Markdown with sections "
          "OK, Problems and Suggested next steps. Only report results returned by tools.")


def run(max_steps: int = 15) -> tuple[str, list[dict]]:
    messages = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": f"Hosts: {list(HOSTS)}; ports: {sorted(PORTS)}; "
                                            f"services: {sorted(SERVICES)}. Produce today's report."}]
    trace = []
    for _ in range(max_steps):
        r = ollama.chat(model=MODEL, messages=messages, tools=list(TOOLS.values()),
                        options={"temperature": 0})
        messages.append(r.message)
        if not r.message.tool_calls:
            return r.message.content, trace
        for call in r.message.tool_calls:
            fn = TOOLS.get(call.function.name)
            try:
                result = fn(**call.function.arguments) if fn else "unknown tool"
            except TypeError as e:
                result = f"bad arguments: {e}"
            trace.append({"tool": call.function.name, "args": call.function.arguments, "result": result})
            messages.append({"role": "tool", "content": result, "tool_name": call.function.name})
    return "Stopped: step limit reached.", trace


if __name__ == "__main__":
    report, trace = run()
    day = datetime.now().strftime("%Y-%m-%d")
    out = Path("/var/lib/opsagent"); out.mkdir(parents=True, exist_ok=True)
    (out / f"{day}.md").write_text(report)
    (out / f"{day}.trace.json").write_text(json.dumps(trace, indent=2))
    print(report)
