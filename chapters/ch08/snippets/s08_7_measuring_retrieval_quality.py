def recall_at_k(queries: list[tuple[str, set[str]]], search, k: int = 5) -> float:
    hits = sum(1 for q, relevant in queries if relevant & set(search(q, k)))
    return hits / len(queries)
