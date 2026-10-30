import yaml


def read_front_matter(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return yaml.safe_load(fm) or {}, body
    return {}, text

fm, body = read_front_matter(load_text(path))
chunks = chunk_markdown(body, source=key)
metas = [{**c.meta, "status": fm.get("status", "draft"), "acl_group": acl_group} for c in chunks]

# at query time
hits = index.search(question, k=k, where={"status": "current", "acl_group": user_groups})
