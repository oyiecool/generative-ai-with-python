def sample_settings(logits: torch.Tensor, temperature: float, top_p: float) -> torch.Tensor:
    if temperature == 0:
        return logits.argmax()
    probs = torch.softmax(logits / temperature, dim=-1)
    sorted_p, sorted_i = torch.sort(probs, descending=True)
    keep = torch.cumsum(sorted_p, dim=-1) - sorted_p < top_p   # nucleus
    sorted_p[~keep] = 0
    sorted_p /= sorted_p.sum()
    return sorted_i[torch.multinomial(sorted_p, 1)]

for t in (0, 0.7, 1.5):
    picks = [tok.decode(sample_settings(logits, t, 0.9)) for _ in range(8)]
    print(t, picks)
