from typing import List

from fastapi import APIRouter, Depends

from src.api.base.depend import check_read_access
from src.api.tasks.dto import TaskResponse
from src.api.tasks.service import get_tasks, create_task

tasks_router = APIRouter(tags=["Tasks"])
tasks_router.add_api_route(
    path="/tasks",
    endpoint=get_tasks,
    methods=["GET"],
    response_model=List[TaskResponse],
    dependencies=Depends(check_read_access),
)
tasks_router.add_api_route(
    path="/tasks",
    endpoint=create_task,
    methods=["POST"],
)
