TOKENS_PER_HOUR = 50_000
_usage: dict[str, deque] = defaultdict(deque)      # (timestamp, tokens)


def token_budget(user: User = Depends(authenticate)):
    now, q = time.time(), _usage[user.id]
    while q and now - q[0][0] > 3600:
        q.popleft()
    if sum(t for _, t in q) >= TOKENS_PER_HOUR:
        raise HTTPException(429, "hourly token budget exhausted", headers={"Retry-After": "600"})
    return q


@app.post("/v1/ask")
def ask(req: AskRequest, user: User = Depends(authenticate), usage=Depends(token_budget)):
    result = answer(...)
    usage.append((time.time(), result["input_tokens"] + result["output_tokens"]))
    ...
