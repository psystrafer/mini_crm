import uvicorn
from fastapi import FastAPI

from src.api.analytics.route import analytics_router
from src.api.auth.route import auth_router
from src.api.contacts.route import contacts_router
from src.api.deals.route import deals_router
from src.api.organizations.route import organizations_router
from src.api.tasks.route import tasks_router
from src.middlewares import register_middlewares
from src.settings import settings


def create_app() -> FastAPI:
    a = FastAPI(root_path=settings.root_path)
    a.include_router(auth_router)
    a.include_router(organizations_router)
    a.include_router(contacts_router)
    a.include_router(deals_router)
    a.include_router(tasks_router)
    a.include_router(analytics_router)
    register_middlewares(a)
    return a


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        host="0.0.0.0",
        port=8000,
    )
