REQUIRED = {"name", "version"}


def load_prompt(name: str, version: int | None = None) -> Prompt:
    ...
    meta = yaml.safe_load(front) or {}
    missing = REQUIRED - meta.keys()
    if missing:
        raise ValueError(f"{files[-1].name}: front matter missing {sorted(missing)}")
    if not isinstance(meta["version"], int):
        raise ValueError(f"{files[-1].name}: version must be an integer")
    if meta["name"] != name:
        raise ValueError(f"{files[-1].name}: name {meta['name']!r} does not match file name")
    return Prompt(meta["name"], meta["version"], meta, body.lstrip())
