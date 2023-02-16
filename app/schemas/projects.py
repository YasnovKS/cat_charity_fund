from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    name: Optional[str]
    description: Optional[str]
    full_amount: Optional[int]


class ProjectUpdate(ProjectBase):
    pass


class ProjectCreate(ProjectBase):
    name: str
    description: str
    full_amount: int


class ProjectDB(ProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
