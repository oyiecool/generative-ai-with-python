CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE kb_chunks (
    id          text PRIMARY KEY,
    source      text NOT NULL,
    heading     text,
    body        text NOT NULL,
    acl_group   text NOT NULL,          -- who may see this chunk
    embedding   vector(384) NOT NULL
);
CREATE INDEX ON kb_chunks USING hnsw (embedding vector_cosine_ops);

-- nearest neighbours the caller is allowed to see
SELECT id, body, 1 - (embedding <=> $1) AS score
FROM kb_chunks
WHERE acl_group = ANY($2)
ORDER BY embedding <=> $1
LIMIT 5;
