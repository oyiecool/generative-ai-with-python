from pydantic import BaseModel, model_validator


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    amount: float


class Invoice(BaseModel):
    vendor: str
    invoice_number: str
    total: float
    line_items: list[LineItem]

    @model_validator(mode="after")
    def reconcile(self):
        s = round(sum(i.amount for i in self.line_items), 2)
        if abs(s - self.total) > 0.01:
            raise ValueError(f"line items sum to {s} but total is {self.total}")
        return self
