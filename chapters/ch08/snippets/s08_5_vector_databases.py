# uv add chromadb
import chromadb

client = chromadb.PersistentClient(path="data/chroma")
col = client.get_or_create_collection(
    "kb", metadata={"hnsw:space": "cosine", "embed_model": "all-MiniLM-L6-v2"}
)
emb = LocalEmbedder()
chunks = chunk_markdown(open("data/kb/identity.md").read(), source="identity.md")
col.add(
    ids=[f"identity.md#{i}" for i in range(len(chunks))],
    documents=[c.text for c in chunks],
    metadatas=[c.meta for c in chunks],
    embeddings=emb.embed([c.text for c in chunks]).tolist(),
)
res = col.query(query_embeddings=emb.embed(["lost authenticator"]).tolist(), n_results=3,
                where={"source": "identity.md"})
