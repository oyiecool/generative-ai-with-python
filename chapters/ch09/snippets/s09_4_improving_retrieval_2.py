from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank(query: str, hits, top_n: int = 6):
    scores = reranker.predict([(query, h.text) for h in hits])
    ranked = sorted(zip(scores, hits), key=lambda t: t[0], reverse=True)
    return [h for _, h in ranked[:top_n]]
