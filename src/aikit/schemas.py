# src/aikit/schemas.py
from enum import Enum

from pydantic import BaseModel, Field


class Priority(str, Enum):
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class TicketTriage(BaseModel):
    """Structured triage of an IT support ticket."""

    category: str = Field(description="One of: network, database, identity, endpoint, application, other")
    priority: Priority
    affected_users: int | None = Field(None, ge=0, description="Number stated in the ticket, else null")
    summary: str = Field(max_length=200)
    needs_human: bool = Field(description="True if the ticket mentions security, data loss or legal issues")


print(TicketTriage.model_json_schema())
