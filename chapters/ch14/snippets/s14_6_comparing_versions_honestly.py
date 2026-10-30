import numpy as np

def bootstrap_diff(a: list[float], b: list[float], n: int = 10_000, seed: int = 0):
    """95% CI for mean(b) - mean(a) on paired per-case scores."""
    rng = np.random.default_rng(seed)
    d = np.array(b) - np.array(a)
    samples = rng.choice(d, size=(n, len(d)), replace=True).mean(axis=1)
    return d.mean(), np.percentile(samples, [2.5, 97.5])

mean, (lo, hi) = bootstrap_diff(scores_v1, scores_v2)
print(f"v2 - v1 = {mean:+.3f}  (95% CI {lo:+.3f} to {hi:+.3f})")
