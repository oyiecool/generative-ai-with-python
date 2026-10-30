import itertools

import numpy as np

from aikit.embed import LocalEmbedder

sentences = [...]                                     # 20 sentences from your domain
vecs = LocalEmbedder().embed(sentences)
sims = vecs @ vecs.T
np.fill_diagonal(sims, -1)
i, j = np.unravel_index(sims.argmax(), sims.shape)
print(f"{sims[i, j]:.3f}\n  {sentences[i]}\n  {sentences[j]}")

for a, b in sorted(itertools.combinations(range(len(sentences)), 2), key=lambda p: -sims[p])[:5]:
    print(f"{sims[a, b]:.2f}  {sentences[a][:50]} | {sentences[b][:50]}")
