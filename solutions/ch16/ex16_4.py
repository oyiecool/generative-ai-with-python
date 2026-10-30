from email.utils import parseaddr

ALLOWED = {"company.example", "partner.example"}


def email_allowed(recipient: str) -> bool:
    name, addr = parseaddr(recipient)
    if "@" not in addr or addr.count("@") != 1:
        return False
    domain = addr.rsplit("@", 1)[1].lower().rstrip(".")
    return domain in ALLOWED

tests = {
    "alice@company.example": True, "Bob <bob@partner.example>": True,
    "eve@attacker.example": False, "x@company.example.attacker.example": False,
    "x@sub.company.example": False, "x@COMPANY.EXAMPLE": True,
    "not-an-email": False, "a@b@company.example": False,
    "x@company.example.": True, "": False,
}
for addr, expected in tests.items():
    assert email_allowed(addr) == expected, addr
