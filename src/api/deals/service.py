from datetime import datetime

from fastapi import Depends
from sqlalchemy import update, select

from src.api.base.depend import get_current_organization_id, check_update_access
from src.api.deals.depend import get_deals_query
from src.api.deals.dto import CreateDealRequest, DealUpdateRequest, CreateActivityRequest
from src.clients.db import AsyncSession
from src.models import Deal, Activity
from src.models.activity import ActivityType
from src.models.deal import DealStatus


async def create_deal(
    request: CreateDealRequest,
    session: AsyncSession,
    organization_id = Depends(get_current_organization_id),
    user_id: int = Depends(check_update_access),
):
    deal = Deal(
        organization_id=organization_id,
        contact_id=request.contact_id,
        owner_id=user_id,
        title=request.title,
        amount=request.amount,
        currency=request.currency,
        updated_at=datetime.now(),
    )
    async with session.begin() as s:
        s.add(deal)
        return deal


async def get_deals(
    session: AsyncSession,
    deals_query = Depends(get_deals_query),
):
    async with session() as s:
        deals = await s.scalars(deals_query)
        return deals


ALLOWED_TRANSITIONS = {
    DealStatus.NEW: [DealStatus.IN_PROGRESS, DealStatus.LOST],
    DealStatus.IN_PROGRESS: [DealStatus.WON, DealStatus.LOST],
    DealStatus.WON: [],
    DealStatus.LOST: []
}


async def update_deal(
    deal_id: int,
    body: DealUpdateRequest,
    session: AsyncSession,
    user_id: int = Depends(check_update_access),
):
    async with session.begin() as s:
        deal = await s.scalar(select(Deal).where(Deal.id == deal_id))
        if body.status in ALLOWED_TRANSITIONS[deal.status]:
            data = {}
            if body.status:
                data["status"] = body.status
            if body.stage:
                data["stage"] = body.stage
            await s.execute(
                update(Deal)
                .where(Deal.id == deal_id)
                .values(**data)
            )
            activity = Activity(
                deal_id=deal_id,
                author_id=user_id,
                type=ActivityType.STATUS_CHANGED,
                payload={"text": {deal.status: body.status}},
            )
            s.add(activity)


async def get_activities(deal_id: int, session: AsyncSession):
    async with session() as s:
        activities = await s.scalars(select(Activity).where(Activity.deal_id == deal_id))
        return activities


async def create_activities(
    deal_id: int,
    request: CreateActivityRequest,
    session: AsyncSession,
    user_id: int = Depends(check_update_access),
):
    async with session.begin() as s:
        activity = Activity(
            deal_id=deal_id,
            author_id=user_id,
            type=ActivityType.COMMENT,
            payload={"text": request.text},
        )
        s.add(activity)
