resp = ollama.chat(model="llama3.2", messages=[...], format=TicketTriage.model_json_schema())
triage = TicketTriage.model_validate_json(resp["message"]["content"])
