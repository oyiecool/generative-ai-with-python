mean, (lo, hi) = bootstrap_diff(scores_v1, scores_v2)
print(f"v2 - v1 = {mean:+.3f}, 95% CI [{lo:+.3f}, {hi:+.3f}]")
flipped_bad = [c for c, a, b in zip(cases, scores_v1, scores_v2) if a > b]
print("regressions:", [c["id"] for c in flipped_bad])
