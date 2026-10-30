def search_reranked(q: str, k: int = 5) -> list[str]:
    candidates = idx.search(q, k=30)
    return [h.id for h in rerank(q, candidates, top_n=k)]

print("vector:", recall_at_k(labelled, lambda q, k: [h.id for h in idx.search(q, k)]))
print("reranked:", recall_at_k(labelled, search_reranked))
