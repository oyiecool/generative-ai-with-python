results = {}
for size in (500, 1500, 3000):
    idx = VectorIndex(LocalEmbedder())
    for path in docs:
        chunks = chunk_markdown(path.read_text(), source=path.name, max_chars=size, overlap=size // 8)
        idx.add([f"{path.name}#{k}" for k in range(len(chunks))], [c.text for c in chunks],
                [c.meta for c in chunks])
    search = lambda q, k: [h.meta["source"] + "|" + h.meta["heading"] for h in idx.search(q, k)]
    results[size] = recall_at_k(labelled, search, k=5)
print(results)
