from fastapi import Depends

from src.api.base.depend import check_update_access
from src.api.tasks.depend import get_tasks_query
from src.api.tasks.dto import CreateTaskRequest
from src.clients.db import AsyncSession
from src.models import Task


async def get_tasks(
    session: AsyncSession,
    tasks_query = Depends(get_tasks_query)
):
    async with session() as s:
        tasks = await s.scalars(tasks_query)
        return tasks


async def create_task(
    request: CreateTaskRequest,
    session: AsyncSession,
    _: int = Depends(check_update_access),
):
    async with session.begin() as s:
        task = Task(
            deal_id=request.deal_id,
            title=request.title,
            description=request.description,
            due_date=request.due_date,
        )
        s.add(task)
