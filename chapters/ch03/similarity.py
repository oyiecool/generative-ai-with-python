# chapters/ch03/similarity.py
# uv add sentence-transformers
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
sentences = [
    "The database server ran out of disk space.",
    "Storage on the DB host is full.",
    "The quarterly sales meeting moved to Tuesday.",
]
vecs = model.encode(sentences, normalize_embeddings=True)
print(util.cos_sim(vecs, vecs))
