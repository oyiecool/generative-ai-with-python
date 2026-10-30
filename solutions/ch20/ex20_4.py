CASES = [
    ("What should I do if a chemical spills?", True), ("Who can use the laser cutter?", True),
    ("When does the lab close?", True), ("Do I need goggles for soldering?", True),
    ("How do I report an injury?", True), ("Can I bring food into the lab?", True),
    ("Where is the first aid kit?", True),
    ("What is the Wi-Fi password?", False), ("Who won the football yesterday?", False),
    ("What is my exam grade?", False),
]
for th in (0.35, 0.40, 0.45, 0.50, 0.55):
    correct = 0
    for q, answerable in CASES:
        v = embed_query(q)                                  # as in app.py
        top = float((matrix @ v).max())
        correct += (top >= th) == answerable
    print(th, f"{correct}/{len(CASES)}")
