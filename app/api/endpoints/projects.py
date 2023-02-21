from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_project_exists, check_project_name, check_project_investments
from app.core.db import get_async_session
from app.crud import projects_crud
from app.schemas.projects import ProjectCreate, ProjectDB, ProjectUpdate

router = APIRouter()


@router.get('/', response_model=list[ProjectDB],
            response_model_exclude_none=True)
async def get_projects(session: AsyncSession = Depends(get_async_session)
                       ) -> list[ProjectDB]:
    project_list = await projects_crud.get_object_list(session)
    return project_list


@router.post('/', response_model=ProjectDB,
             response_model_exclude_none=True)
async def create_project(project: ProjectCreate,
                         session: AsyncSession = Depends(get_async_session)
                         ) -> ProjectDB:
    await check_project_name(project, session)
    new_project = await projects_crud.create_object(project, session)
    return new_project


@router.delete('/{project_id}', response_model=ProjectDB,
               response_model_exclude_none=True)
async def delete_project(project_id: int,
                         session: AsyncSession = Depends(get_async_session)
                         ) -> ProjectDB:
    db_obj = await check_project_investments(project_id, session)
    db_obj = await projects_crud.delete_object(db_obj, session)
    return db_obj


@router.patch('/{project_id}', response_model=ProjectDB,
              response_model_exclude_none=True)
async def update_project(project_id, data: ProjectUpdate,
                         session: AsyncSession = Depends(get_async_session)
                         ) -> ProjectDB:
    project = await projects_crud.get_object(obj_id=project_id, session=session)
