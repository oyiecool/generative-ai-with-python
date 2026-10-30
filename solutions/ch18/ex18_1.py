import numpy as np


def bootstrap_unpaired(a, b, n=10_000, seed=0):
    rng = np.random.default_rng(seed)
    a, b = np.asarray(a, float), np.asarray(b, float)
    diffs = [rng.choice(b, len(b)).mean() - rng.choice(a, len(a)).mean() for _ in range(n)]
    return b.mean() - a.mean(), np.percentile(diffs, [2.5, 97.5])


for name, llm in {"hosted": LLM(), "local": LLM(provider="ollama", model="qwen2.5:7b")}.items():
    s = run(llm, repeats=5)
    mean, (lo, hi) = bootstrap_unpaired(s["group_a"], s["group_b"])
    print(f"{name}: gap {mean:+.2f} (95% CI {lo:+.2f} to {hi:+.2f})")
