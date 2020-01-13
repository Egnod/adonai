from ..app.crud import CRUDBase
from .models import Project


class ProjectCRUD(CRUDBase):
    model = Project
