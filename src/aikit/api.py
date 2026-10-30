# src/aikit/api.py
import json
import time
import uuid

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from pydantic import BaseModel, Field
from sse_starlette.sse import EventSourceResponse

from aikit.rag import answer, stream_answer
from aikit.security import User, authenticate, rate_limit

app = FastAPI(title="Policy Assistant", version="1.0")


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=2000)
    conversation_id: str | None = None


class AskResponse(BaseModel):
    trace_id: str
    answerable: bool
    answer: str
    sources: list[dict]
    latency_ms: int


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.post("/v1/ask", response_model=AskResponse)
def ask(req: AskRequest, user: User = Depends(authenticate), _=Depends(rate_limit)):
    trace_id, start = uuid.uuid4().hex, time.perf_counter()
    result = answer(req.question, index=app.state.index, llm=app.state.llm,
                    user_groups=user.groups)
    latency = int((time.perf_counter() - start) * 1000)
    app.state.audit.write(trace_id=trace_id, user=user.id, latency_ms=latency,
                          answerable=result["answerable"],
                          sources=[s["file"] for s in result["sources"]])
    return AskResponse(trace_id=trace_id, latency_ms=latency, **result)


@app.post("/v1/ask/stream")
async def ask_stream(req: AskRequest, request: Request, user: User = Depends(authenticate),
                     _=Depends(rate_limit)):
    trace_id = uuid.uuid4().hex

    async def events():
        yield {"event": "meta", "data": json.dumps({"trace_id": trace_id})}
        async for kind, payload in stream_answer(req.question, app.state.index,
                                                 app.state.async_llm, user.groups):
            if await request.is_disconnected():          # stop paying for unread tokens
                break
            yield {"event": kind, "data": json.dumps(payload)}
        yield {"event": "done", "data": "{}"}

    return EventSourceResponse(events())
