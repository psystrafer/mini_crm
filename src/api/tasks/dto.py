from datetime import datetime

from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: int
    deal_id: int
    title: str
    description: str
    due_date: datetime
    is_done: bool
    created_at: datetime

    class Config:
        from_attributes = True


class CreateTaskRequest(BaseModel):
    deal_id: int
    title: str
    description: str
    due_date: datetime
