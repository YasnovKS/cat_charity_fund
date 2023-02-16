from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.encoders import jsonable_encoder


class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model

    async def get_object(self, obj_id, session: AsyncSession):
        db_obj = await session.execute(select(self.model)
                                       .where(self.model.id == obj_id)
                                       )
        return db_obj.scalars().first()

    async def get_object_list(self, session: AsyncSession):
        queryset = await session.execute(select(self.model))
        return queryset.scalars().all()

    async def create_object(self, data, session: AsyncSession):
        data = data.dict()
        db_obj = self.model(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def delete_object(self, db_obj, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def update_object(self, db_obj, data, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_data = data.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
