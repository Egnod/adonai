from ..app.crud import CRUDBase
from .models import Project


class ProjectCRUD(CRUDBase):
    model = Project

    @classmethod
    def is_active(cls, session, id: int) -> bool:
        project = cls.get(session, id)

        if project is not None:
            return project.is_active

    @classmethod
    def is_global_active(cls, session, id: int) -> bool:
        project = cls.get(session, id)

        if project is not None:
            return project.is_active and project.domain.is_active
