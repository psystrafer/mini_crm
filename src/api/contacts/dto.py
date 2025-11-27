from datetime import datetime

from pydantic import BaseModel, Field


class ContactRequest(BaseModel):
    page: int = 1
    page_size: int = Field(le=100)
    search: str
    owner_id: int


class ContactResponse(BaseModel):
    id: int
    organization_id: int
    owner_id: int
    name: str
    email: str
    phone: str
    created_at: datetime

    class Config:
        from_attributes = True


class CreateContactRequest(BaseModel):
    name: str
    email: str
    phone: str
