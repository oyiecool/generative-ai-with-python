import sqlite3
from typing import Literal

fb = sqlite3.connect("data/feedback.db", check_same_thread=False)
fb.execute("""CREATE TABLE IF NOT EXISTS feedback (
    trace_id TEXT, user_id TEXT, score INTEGER, comment TEXT,
    created TEXT DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY (trace_id, user_id))""")


class Feedback(BaseModel):
    trace_id: str = Field(pattern=r"^[0-9a-f]{32}$")
    score: Literal[-1, 1]
    comment: str | None = Field(None, max_length=1000)


@app.post("/v1/feedback", status_code=204)
def feedback(f: Feedback, user: User = Depends(authenticate)):
    fb.execute("INSERT OR REPLACE INTO feedback (trace_id, user_id, score, comment) VALUES (?,?,?,?)",
               (f.trace_id, user.id, f.score, f.comment))
    fb.commit()
