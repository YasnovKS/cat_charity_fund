from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from .db import get_async_session
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from app.models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
