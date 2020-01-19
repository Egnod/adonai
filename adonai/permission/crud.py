from typing import List, Union

from sqlalchemy.orm.session import Session

from ..app.crud import CRUDBase
from .internal.permission_set import InternalPermissionSet
from .models import Permission


class PermissionCRUD(CRUDBase):
    model = Permission

    @classmethod
    def is_active(cls, session, id: int) -> bool:
        permission: Permission = cls.get(session, id)

        if permission:
            return permission.is_active

    @classmethod
    def is_unique(cls, session, type: str, name: str) -> bool:
        return not Permission.query.filter_by(name=name, type=type).count()
