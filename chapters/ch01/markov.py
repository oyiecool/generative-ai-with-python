# ch01/markov.py — a tiny generative text model
import random
from collections import defaultdict, Counter

corpus = """
the server restarted after the patch was applied
the patch was tested before the change window
the change window opened after the backup finished
the backup finished before the server restarted
""".split()

# Learn: count what follows each pair of words
model: dict[tuple[str, str], Counter] = defaultdict(Counter)
for a, b, c in zip(corpus, corpus[1:], corpus[2:]):
    model[(a, b)][c] += 1

def generate(start: tuple[str, str], length: int = 12, seed: int | None = None) -> str:
    rng = random.Random(seed)
    words = list(start)
    for _ in range(length):
        options = model.get((words[-2], words[-1]))
        if not options:
            break
        choices, weights = zip(*options.items())
        words.append(rng.choices(choices, weights=weights)[0])
    return " ".join(words)

for s in range(3):
    print(generate(("the", "patch"), seed=s))
