from fastapi import Depends

from .depend import get_contacts_query
from .dto import CreateContactRequest
from ..base.depend import get_current_organization_id, check_update_access
from ...clients.db import AsyncSession
from ...models import Contact


async def get_contacts(
    session: AsyncSession,
    contacts_query = Depends(get_contacts_query),
):
    async with session() as s:
        contacts = await s.scalars(contacts_query)
        return contacts


async def create_contacts(
    request: CreateContactRequest,
    session: AsyncSession,
    user_id: int = Depends(check_update_access),
    organization_id: int = Depends(get_current_organization_id),
):
    contact = Contact(
        organization_id=organization_id,
        owner_id=user_id,
        name=request.name,
        email=request.email,
        phone=request.phone,
    )
    async with session.begin() as s:
        s.add(contact)
        return contact
