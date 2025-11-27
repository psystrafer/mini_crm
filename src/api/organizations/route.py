from fastapi import APIRouter

from .service import get_organizations

organizations_router = APIRouter(tags=["Organizations"])
organizations_router.add_api_route(
    path="/organizations/me",
    endpoint=get_organizations,
    methods=["GET"],
)
