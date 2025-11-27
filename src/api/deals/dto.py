from datetime import datetime
from decimal import Decimal
from typing import Dict, Any

from pydantic import BaseModel, model_validator

from src.models.activity import ActivityType
from src.models.deal import DealCurrency, DealStatus, DealStage


class CreateDealRequest(BaseModel):
    contact_id: int
    title: str
    amount: Decimal
    currency: DealCurrency


class DealResponse(BaseModel):
    id: int
    organization_id: int
    contact_id: int
    owner_id: int
    title: str
    amount: Decimal
    currency: DealCurrency
    status: DealStatus
    stage: DealStage
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DealUpdateRequest(BaseModel):
    status: DealStatus = None
    stage: DealStage = None

    @model_validator(mode='after')
    def check_all_none(self):
        if all(value is None for value in self.model_dump().values()):
            raise ValueError("All fields cannot be None")
        return self


class ActivityResponse(BaseModel):
    id: int
    deal_id: int
    author_id: int
    type: ActivityType
    payload: Dict[str, Any]
    created_at: datetime


class CreateActivityRequest(BaseModel):
    text: str
