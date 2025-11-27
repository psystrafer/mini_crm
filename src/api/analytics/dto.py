from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from src.models.deal import DealStatus


class SummaryResponse(BaseModel):
    count_by_status: list[dict[DealStatus, int]]
    sum_by_status: list[dict[DealStatus, Decimal]]
    average_amount_by_won: Optional[Decimal]
    last_new_deals: int


class FunnelResponse(BaseModel):
    ...
