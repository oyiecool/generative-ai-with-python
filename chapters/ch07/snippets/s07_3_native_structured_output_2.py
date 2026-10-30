import anthropic

client = anthropic.Anthropic()
msg = client.messages.create(
    model=s.chat_model,
    max_tokens=500,
    system="Triage the IT ticket.",
    tools=[{
        "name": "record_triage",
        "description": "Record the triage result.",
        "input_schema": TicketTriage.model_json_schema(),
    }],
    tool_choice={"type": "tool", "name": "record_triage"},
    messages=[{"role": "user", "content": ticket_text}],
)
block = next(b for b in msg.content if b.type == "tool_use")
triage = TicketTriage.model_validate(block.input)
