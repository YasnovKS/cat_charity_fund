from pydantic import BaseModel


class ProjectBase(BaseModel):
    name: str
    description: str
    