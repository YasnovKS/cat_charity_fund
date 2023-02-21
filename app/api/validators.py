from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from http import HTTPStatus
from sqlalchemy import select
from app.models import CharityProject
from app.crud import projects_crud
from app.schemas.projects import ProjectUpdate


async def check_project_name(project, session: AsyncSession) -> None:
    '''Check the project name to reject creating projects with existing names.'''
    data = project.dict()
    project_exists = await session.execute(select(CharityProject)
                                           .where(CharityProject.name == data['name']))
    project_exists = project_exists.scalars().first()
    if project_exists:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект с этим именем уже существует.'
        )


async def check_project_exists(obj_id, session: AsyncSession):
    '''Check that project exists in database.'''
    db_obj = await projects_crud.get_object(obj_id, session)
    if not db_obj:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Проект с таким id отсутствует.'
        )
    return db_obj


async def check_project_investments(obj_id: int,
                                    session: AsyncSession
                                    ) -> bool:
    '''Check invested amount of the project.
    No one can delete projects which were invested.'''
    db_obj: CharityProject = await check_project_exists(obj_id, session)
    if db_obj.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Нельзя удалить проинвестированный проект.'
        )
    return db_obj


def check_project_full_amount(db_obj: CharityProject,
                              data: ProjectUpdate):
    if db_obj.invested_amount > data.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Новая сумма для проекта не может быть меньше уже внесенной.'
        )
