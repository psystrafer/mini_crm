from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import select, func

from src.api.analytics.dto import SummaryResponse
from src.clients.db import AsyncSession
from src.models import Deal
from src.models.deal import DealStatus


async def get_summary(session: AsyncSession):
    async with session() as s:
        stmt = select(
            Deal.status,
            func.count(Deal.id).label("count"),
            func.sum(Deal.amount).label("total"),
        ).group_by(Deal.status)
        result = await s.execute(stmt)

        count_by_status = []
        sum_by_status = []
        for (status, count, total) in result:
            count_by_status.append({status: count})
            sum_by_status.append({status: total})

        average_amount_by_won = await s.execute(
            select(func.avg(Deal.amount).label("average"))
            .where(Deal.status == DealStatus.WON)
        )
        average_amount_by_won = average_amount_by_won.scalar()
        average_amount_by_won = (
            average_amount_by_won
            if average_amount_by_won is None
            else average_amount_by_won.quantize(Decimal("0.00"))
        )

        last_new_deals = await s.execute(
            select(func.sum(Deal.id).label("count"))
            .where(Deal.created_at >= datetime.today() - timedelta(days=30))
        )

        return SummaryResponse(
            count_by_status=count_by_status,
            sum_by_status=sum_by_status,
            average_amount_by_won=average_amount_by_won,
            last_new_deals=last_new_deals.scalar(),
        )


async def get_funnel(session: AsyncSession):
    async with session() as s:
        stmt = select(
            Deal.status,
            Deal.stage,
            func.count(Deal.id).label("count"),
        ).group_by(Deal.status, Deal.stage)
        result = await s.execute(stmt)
        return [(status, stage, count) for (status, stage, count) in result.all()]
