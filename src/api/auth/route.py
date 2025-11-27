from fastapi import APIRouter
from starlette.status import HTTP_201_CREATED, HTTP_200_OK

from .service import register, login


auth_router = APIRouter(tags=["Auth"])
auth_router.add_api_route(
    path="/auth/register",
    endpoint=register,
    status_code=HTTP_201_CREATED,
    methods=["POST"],
)
auth_router.add_api_route(
    path="/auth/login",
    endpoint=login,
    status_code=HTTP_200_OK,
    methods=["POST"],
)