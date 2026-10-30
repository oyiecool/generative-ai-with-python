SSS = re.compile(r"\b\d{2}-\d{7}-\d\b")
TIN = re.compile(r"\b\d{3}-\d{3}-\d{3}(?:-\d{3,5})?\b")


def scrub(text: str) -> tuple[str, int]:
    text, n1 = SSS.subn("<SSS>", text)
    text, n2 = TIN.subn("<TIN>", text)
    text = IPV4.sub("<IP>", EMAIL.sub("<EMAIL>", text))
    return text, n1 + n2

changed = sum(1 for r in rows if scrub(json.dumps(r))[1] > 0)
print(f"{changed} of {len(rows)} records contained an ID number")
