from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_correct_full_amount_for_update,
                                check_name_duplicate, check_project_was_closed,
                                check_project_was_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import projects_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import execute_investment_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Get all the charity projects.
        Endpoint is available for all users.
    """
    return await projects_crud.get_multiple(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create new Charity Project.
        Endpoint is available only for superusers.
    """
    await check_name_duplicate(
        charity_project.name, session
    )
    new_charity_project = await projects_crud.create(
        charity_project, session
    )
    await execute_investment_process(
        new_charity_project, session
    )
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
    project_id: int,
    object_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Partial update of Charity Project.
        Endpoint is available only for superuser.
        Fields to update:
            - name (should be unique);
            - description;
            - full_amount (could not be less than the invested amount).
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_project_was_closed(project_id, session)

    if object_in.full_amount is not None:
        await check_correct_full_amount_for_update(
            project_id, session, object_in.full_amount
        )

    if object_in.name is not None:
        await check_name_duplicate(
            object_in.name, session
        )

    return await projects_crud.update(
        charity_project, object_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Deletion of Charity Project.
        The invested project could only be closed but not deleted.
        Not invested projects could be deleted.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_project_was_invested(project_id, session)
    return await (projects_crud.remove(charity_project, session))
