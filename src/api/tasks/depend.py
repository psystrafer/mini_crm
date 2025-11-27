from datetime import datetime

from sqlalchemy import select

from src.models import Task


def get_tasks_query(
    deal_id: int,
    only_open: bool,
    due_before: datetime,
    due_after: datetime,
):
    q = (
        select(Task)
        .where(Task.deal_id == deal_id)
        .where(Task.is_done == only_open)
        .where(Task.due_date.between(due_before, due_after))
    )
    return q
