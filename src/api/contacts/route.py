from typing import List

from fastapi import APIRouter, Depends

from .dto import ContactResponse
from .service import get_contacts, create_contacts
from ..base.depend import check_read_access

contacts_router = APIRouter(tags=["Contacts"])
contacts_router.add_api_route(
    path="/contacts",
    endpoint=get_contacts,
    methods=["GET"],
    response_model=List[ContactResponse],
    dependencies=[Depends(check_read_access)],
)
contacts_router.add_api_route(
    path="/contacts",
    endpoint=create_contacts,
    methods=["POST"],
)