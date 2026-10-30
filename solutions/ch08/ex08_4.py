def delete(self, source: str) -> int:
    keep = [i for i, m in enumerate(self.metas) if m.get("source") != source]
    removed = len(self.ids) - len(keep)
    self.ids = [self.ids[i] for i in keep]
    self.texts = [self.texts[i] for i in keep]
    self.metas = [self.metas[i] for i in keep]
    self.vectors = self.vectors[keep] if keep else None
    return removed
