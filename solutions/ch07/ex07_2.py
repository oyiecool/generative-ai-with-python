from collections import Counter

attempts = Counter()
for ticket in tickets:                     # 50 real or synthetic tickets
    try:
        _, n = extract_with_count(llm, TicketTriage, ticket, "Triage the IT ticket.")
        attempts[n] += 1
    except ExtractionError:
        attempts["failed"] += 1
print(attempts)
