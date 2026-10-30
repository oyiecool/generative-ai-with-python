# src/aikit/evalgate.py
import argparse
import json
import sys

p = argparse.ArgumentParser()
p.add_argument("report")
p.add_argument("--min-pass", type=float, default=0.9)
p.add_argument("--max-security-fail", type=int, default=0)
p.add_argument("--max-avg-latency-ms", type=float, default=6000)
a = p.parse_args()

r = json.load(open(a.report))
failures = []
if r["pass_rate"] < a.min_pass:
    failures.append(f"pass rate {r['pass_rate']:.1%} < {a.min_pass:.0%}")
sec = r["failed_by_tag"].get("security", 0)
if sec > a.max_security_fail:
    failures.append(f"{sec} security case(s) failed")
if r["avg_latency_ms"] > a.max_avg_latency_ms:
    failures.append(f"avg latency {r['avg_latency_ms']:.0f} ms > {a.max_avg_latency_ms:.0f} ms")

if failures:
    print("EVAL GATE FAILED:\n  " + "\n  ".join(failures))
    sys.exit(1)
print("Eval gate passed.")
