from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DonationBase(BaseModel):
    full_amount: int
    comment: Optional[str]


class DonationCreate(DonationBase):
    pass


class DonationUserDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationFullDB(DonationUserDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
