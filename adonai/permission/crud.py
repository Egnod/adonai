from ..app.crud import CRUDBase
from .models import Permission


class PermissionCRUD(CRUDBase):
    model = Permission
