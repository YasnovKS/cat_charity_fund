from fastapi import APIRouter
from .endpoints import projects_router

main_router = APIRouter()

main_router.include_router(projects_router,
                           prefix='/charity_project',
                           tags=['Charity Projects'],
                           )