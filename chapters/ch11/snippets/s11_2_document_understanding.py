from pydantic import BaseModel


class Invoice(BaseModel):
    vendor: str
    invoice_number: str
    date: str | None
    currency: str | None
    total: float | None
    line_items: list[dict]


# Send the image plus the Invoice schema as a forced tool call (Chapter 7),
# then validate. Check totals in code: sum(line_items) should equal total.
