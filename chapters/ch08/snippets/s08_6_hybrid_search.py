# uv add rank-bm25
from rank_bm25 import BM25Okapi


def rrf(rankings: list[list[str]], k: int = 60) -> list[str]:
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking):
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)


bm25 = BM25Okapi([t.lower().split() for t in idx.texts])


def hybrid_search(query: str, k: int = 5) -> list[str]:
    kw = bm25.get_scores(query.lower().split())
    kw_rank = [idx.ids[i] for i in kw.argsort()[::-1][:20]]
    vec_rank = [h.id for h in idx.search(query, k=20)]
    return rrf([kw_rank, vec_rank])[:k]
