# src/aikit/changepack.py
import json
from datetime import datetime, timezone
from pathlib import Path


def evidence_pack(system_id: str, change: str, baseline: Path, candidate: Path,
                  redteam: Path, rollback: str) -> str:
    b, c, r = (json.loads(p.read_text()) for p in (baseline, candidate, redteam))
    rows = []
    for tag in sorted(set(b["by_tag"]) | set(c["by_tag"])):
        old, new = b["by_tag"].get(tag, 0), c["by_tag"].get(tag, 0)
        flag = " ⚠" if new < old - 0.02 else ""
        rows.append(f"| {tag} | {old:.0%} | {new:.0%} | {new - old:+.0%}{flag} |")
    return "\n".join([
        f"# Change evidence — {system_id}",
        f"Generated {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC",
        f"\n**Change:** {change}",
        f"\n**Overall pass rate:** {b['pass_rate']:.0%} → {c['pass_rate']:.0%}",
        f"**Mean cost per request:** ${b['cost_per_req']:.4f} → ${c['cost_per_req']:.4f}",
        f"**p95 latency:** {b['p95_ms']} ms → {c['p95_ms']} ms",
        "\n| Category | Baseline | Candidate | Change |\n| --- | --- | --- | --- |",
        *rows,
        f"\n**Red-team:** {r['passed']}/{r['total']} passed; critical failures: {r['critical_failures']}",
        f"\n**Rollback plan:** {rollback}",
    ])
