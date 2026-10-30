from pydantic import BaseModel


class Facts(BaseModel):
    start_time: str | None
    systems: list[str]
    users_affected: int | None
    customer_facing: bool
    summary: str


class Severity(BaseModel):
    level: str          # SEV1..SEV4
    reason: str


usage = []


def logged(llm, *a, step, **kw):
    r = llm.chat(*a, **kw)
    usage.append({"step": step, "in": r.input_tokens, "out": r.output_tokens, "s": round(r.latency_s, 2)})
    return r


facts = extract(fast, Facts, report, "Extract incident facts.")
sev = extract(fast, Severity, facts.model_dump_json(),
              "Classify severity: SEV1 = customer-facing outage, SEV2 = major internal outage, "
              "SEV3 = degraded service, SEV4 = minor.")
notice = logged(strong, f"Facts: {facts.model_dump_json()}\nSeverity: {sev.level}",
                system="Draft a 100-word stakeholder notification. Use only the facts given.",
                step="draft").text
print(notice, usage)
