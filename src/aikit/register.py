# src/aikit/register.py
from datetime import date
from enum import Enum

from pydantic import BaseModel, Field, model_validator


class Tier(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PROHIBITED = "prohibited"


class ModelRef(BaseModel):
    provider: str
    model: str                      # exact version or snapshot where available
    hosting: str                    # hosted-api | self-hosted | local
    data_terms: str                 # e.g. "no training on inputs; 30-day retention"


class AISystem(BaseModel):
    id: str = Field(pattern=r"^AI-\d{4}$")
    name: str
    purpose: str
    business_owner: str
    technical_owner: str
    tier: Tier
    users: str                      # who uses it, and how many
    affected_people: str            # who is affected by its outputs
    data_categories: list[str]      # e.g. ["internal", "personal", "sensitive-personal"]
    models: list[ModelRef]
    tools_with_side_effects: list[str] = []
    human_oversight: str
    pia_reference: str | None = None
    last_evaluation: date | None = None
    next_review: date
    status: str = "proposed"        # proposed | approved | live | suspended | retired

    @model_validator(mode="after")
    def tier_requirements(self):
        personal = any("personal" in c for c in self.data_categories)
        if personal and not self.pia_reference:
            raise ValueError("systems processing personal data need a PIA reference")
        if self.tier == Tier.HIGH and self.status == "live" and not self.last_evaluation:
            raise ValueError("high-risk live systems need a recorded evaluation")
        if self.tools_with_side_effects and self.tier == Tier.LOW:
            raise ValueError("systems that take actions cannot be tiered low")
        return self
