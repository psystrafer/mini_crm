from typing import List

from fastapi import APIRouter, Depends

from src.api.base.depend import check_read_access
from src.api.deals.dto import DealResponse, ActivityResponse
from src.api.deals.service import (
    get_deals,
    create_deal,
    update_deal,
    get_activities,
    create_activities,
)

deals_router = APIRouter(tags=["Deals"])
deals_router.add_api_route(
    path="/deals",
    endpoint=get_deals,
    methods=["GET"],
    response_model=List[DealResponse],
    dependencies=Depends(check_read_access),
)
deals_router.add_api_route(
    path="/deals",
    endpoint=create_deal,
    methods=["POST"],
)
deals_router.add_api_route(
    path="/deals/{deal_id}",
    endpoint=update_deal,
    methods=["PATCH"],
)
deals_router.add_api_route(
    path="/deals/{deal_id}/activities",
    endpoint=get_activities,
    methods=["GET"],
    response_model=List[ActivityResponse],
    dependencies=Depends(check_read_access),
)
deals_router.add_api_route(
    path="/deals/{deal_id}/activities",
    endpoint=create_activities,
    methods=["POST"],
)
