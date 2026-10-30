# src/aikit/vectorindex.py
from dataclasses import dataclass, field

import numpy as np


@dataclass
class Hit:
    id: str
    score: float
    text: str
    meta: dict


@dataclass
class VectorIndex:
    embedder: object
    ids: list[str] = field(default_factory=list)
    texts: list[str] = field(default_factory=list)
    metas: list[dict] = field(default_factory=list)
    vectors: np.ndarray | None = None

    def add(self, ids, texts, metas=None):
        vecs = self.embedder.embed(texts)
        self.vectors = vecs if self.vectors is None else np.vstack([self.vectors, vecs])
        self.ids += ids
        self.texts += texts
        self.metas += metas or [{} for _ in texts]

    def search(self, query: str, k: int = 5, where: dict | None = None) -> list[Hit]:
        q = self.embedder.embed([query])[0]
        scores = self.vectors @ q                       # cosine, since vectors are normalised
        if where:                                        # simple metadata filter
            mask = np.array([all(m.get(k2) == v for k2, v in where.items()) for m in self.metas])
            scores = np.where(mask, scores, -np.inf)
        top = np.argsort(-scores)[:k]
        return [Hit(self.ids[i], float(scores[i]), self.texts[i], self.metas[i])
                for i in top if np.isfinite(scores[i])]
