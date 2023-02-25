from fastapi import APIRouter

from .endpoints import donations_router, projects_router, users_router

main_router = APIRouter()

main_router.include_router(users_router)
main_router.include_router(projects_router,
                           prefix='/charity_project',
                           tags=['Charity Projects'],
                           )
main_router.include_router(donations_router,
                           prefix='/donation',
                           tags=['Donations']
                           )