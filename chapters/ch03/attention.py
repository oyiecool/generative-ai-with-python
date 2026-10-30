# chapters/ch03/attention.py
import numpy as np

rng = np.random.default_rng(0)
seq_len, d_model, d_k = 5, 16, 8
x = rng.normal(size=(seq_len, d_model))          # 5 token vectors

W_q, W_k, W_v = (rng.normal(size=(d_model, d_k)) for _ in range(3))
Q, K, V = x @ W_q, x @ W_k, x @ W_v

scores = Q @ K.T / np.sqrt(d_k)
mask = np.triu(np.ones((seq_len, seq_len)), k=1) * -1e9  # hide the future
scores = scores + mask

weights = np.exp(scores - scores.max(axis=1, keepdims=True))
weights /= weights.sum(axis=1, keepdims=True)    # softmax per row

out = weights @ V
print(np.round(weights, 2))   # row i: how much token i attends to tokens 0..i
