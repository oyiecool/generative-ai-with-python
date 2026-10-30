# ch01/markov_n.py
import random
from collections import Counter, defaultdict


def train(words: list[str], n: int) -> dict[tuple[str, ...], Counter]:
    model: dict[tuple[str, ...], Counter] = defaultdict(Counter)
    for i in range(len(words) - n):
        model[tuple(words[i:i + n])][words[i + n]] += 1
    return model


def generate(model, start: tuple[str, ...], length=12, seed=None, temperature=1.0) -> str:
    rng, out, n = random.Random(seed), list(start), len(start)
    for _ in range(length):
        options = model.get(tuple(out[-n:]))
        if not options:
            break
        words, counts = zip(*options.items())
        weights = [c ** (1 / temperature) for c in counts]     # exercise 1.2
        out.append(rng.choices(words, weights=weights)[0])
    return " ".join(out)


model3 = train(corpus, n=3)
print(generate(model3, ("the", "patch", "was"), seed=1))
