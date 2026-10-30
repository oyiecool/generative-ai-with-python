from aikit.llm import LLM
from aikit.router import classify_sensitivity      # Chapter 5 project

local = LLM(provider="ollama", model="qwen2.5:1.5b")
hosted = LLM()                                      # only for approved, non-sensitive requests


def route(question: str, user_approved_cloud: bool) -> tuple[str, str]:
    if classify_sensitivity(question) != "public":
        return local.chat(question).text, "local (sensitive)"
    draft = local.chat(question + "\nIf you are not confident, reply only: ESCALATE").text
    if "ESCALATE" not in draft:
        return draft, "local"
    if not user_approved_cloud:
        return "I can only answer that with the cloud model. Approve sending it?", "needs approval"
    return hosted.chat(question).text, "hosted (approved)"
