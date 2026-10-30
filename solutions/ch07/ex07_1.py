from typing import Literal


class TicketTriage(BaseModel):
    ...
    escalate_to: Literal["network-team", "dba-team", "service-desk"] | None = Field(
        None, description="Team to escalate to, or null if none of these fits")
