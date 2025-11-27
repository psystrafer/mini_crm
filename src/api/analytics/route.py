from fastapi import APIRouter, Depends

from src.api.analytics.dto import SummaryResponse
from src.api.analytics.service import get_summary, get_funnel
from src.api.base.depend import check_read_access

analytics_router = APIRouter(tags=["Analytics"])
analytics_router.add_api_route(
    path="/analytics/deals/summary",
    endpoint=get_summary,
    methods=["GET"],
    response_model=SummaryResponse,
    dependencies=Depends(check_read_access),
)
analytics_router.add_api_route(
    path="/analytics/deals/funnel",
    endpoint=get_funnel,
    methods=["GET"],
    dependencies=Depends(check_read_access),
)
