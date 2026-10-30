FEW_SHOT = [
    {"role": "user", "content": "<ticket>VPN drops every 10 minutes since this morning</ticket>"},
    {"role": "assistant", "content": '{"category": "network", "priority": "P3"}'},
    {"role": "user", "content": "<ticket>Payroll database is down for all users</ticket>"},
    {"role": "assistant", "content": '{"category": "database", "priority": "P1"}'},
]

def classify(ticket: str) -> str:
    msgs = [Message(m["role"], m["content"]) for m in FEW_SHOT]
    msgs.append(Message("user", f"<ticket>{ticket}</ticket>"))
    return llm.chat(msgs, system="Classify IT tickets. Reply with JSON only.", temperature=0).text
