from app.core.db import Base
from sqlalchemy import Column, String, Text, Integer, DateTime, Boolean
from sqlalchemy.sql import func


class CharityProject(Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=func.now())
    close_date = Column(DateTime, default=None)

    def close_project(self):
        '''Method for changing values of "close_date" and "fully_invested"
        fields when the project is closed.'''
        if self.invested_amount == self.full_amount:
            self.close_date = func.now()
            self.fully_invested = True
