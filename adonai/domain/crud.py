from ..app.crud import CRUDBase
from .models import Domain


class DomainCRUD(CRUDBase):
    model = Domain
