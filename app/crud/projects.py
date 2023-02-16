from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDProjects(CRUDBase):
    pass


crud = CRUDProjects(CharityProject)
