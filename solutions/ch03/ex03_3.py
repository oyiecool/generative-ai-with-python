import matplotlib.pyplot as plt

results = {}
for t in (0.2, 1.0, 2.0):
    picks = {tok.decode(sample_settings(logits, t, top_p=1.0)) for _ in range(100)}
    results[t] = len(picks)

plt.bar([str(t) for t in results], results.values())
plt.xlabel("temperature"); plt.ylabel("distinct tokens in 100 samples")
plt.savefig("distinct_tokens.png", dpi=150)
