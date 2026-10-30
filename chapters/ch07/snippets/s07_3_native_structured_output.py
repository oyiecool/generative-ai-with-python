from openai import OpenAI

client = OpenAI()
completion = client.chat.completions.parse(      # older SDKs: client.beta.chat.completions.parse
    model=s.chat_model,
    messages=[
        {"role": "system", "content": "Triage the IT ticket."},
        {"role": "user", "content": ticket_text},
    ],
    response_format=TicketTriage,
)
triage: TicketTriage = completion.choices[0].message.parsed
