pending = None


def handle(text: str) -> str:
    global pending
    if pending and text.lower().strip(" .!") in {"yes", "yes please", "go ahead"}:
        q, pending = pending, None
        return hosted.chat(q, max_tokens=120).text
    pending = None
    reply, route_used = route(text, user_approved_cloud=False)
    if route_used == "needs approval":
        pending = text
        return "I'm sending that to the cloud model. Say yes to confirm."
    return reply
