# src/aikit/judge.py
from pydantic import BaseModel, Field

from aikit.structured import extract

JUDGE_SYSTEM = """You are a strict evaluator of answers produced by a policy assistant.
Score each criterion from 1 (poor) to 5 (excellent) using the rubric. Quote evidence.

Faithfulness: 5 = every claim is supported by the sources; 1 = contains unsupported claims.
Completeness: 5 = fully answers the question; 1 = misses the main point.
Clarity: 5 = concise and easy for a non-specialist; 1 = confusing or padded.

Judge only against the sources shown. Do not use outside knowledge."""


class Verdict(BaseModel):
    faithfulness: int = Field(ge=1, le=5)
    completeness: int = Field(ge=1, le=5)
    clarity: int = Field(ge=1, le=5)
    unsupported_claims: list[str]
    rationale: str = Field(max_length=600)


def judge(question: str, sources: str, answer: str, judge_llm) -> Verdict:
    payload = f"<question>{question}</question>\n<sources>{sources}</sources>\n<answer>{answer}</answer>"
    return extract(judge_llm, Verdict, payload, JUDGE_SYSTEM)
