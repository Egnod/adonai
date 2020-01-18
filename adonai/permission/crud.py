from typing import List, Union

from sqlalchemy.orm.session import Session

from ..app.crud import CRUDBase
from .internal.permission_set import InternalPermissionSet
from .models import Permission


class PermissionCRUD(CRUDBase):
    model = Permission

    @classmethod
    def sync_permissions(
        cls,
        session: Session,
        permission_sets: Union[InternalPermissionSet, List[InternalPermissionSet]],
    ):
        if isinstance(permission_sets, InternalPermissionSet):
            permission_sets = [permission_sets]

        for permission_set in permission_sets:
            permissions = permission_set.get_permissions()

            for permission in permissions:
                if (
                    not session.query(Permission)
                    .filter_by(name=permission.name, type="internal")
                    .count()
                ):
                    cls.create(
                        session,
                        {
                            "name": permission.name,
                            "description": permission.description,
                            "type": "internal",
                        },
                    )

    @classmethod
    def is_active(cls, session, id: int) -> bool:
        permission: Permission = cls.get(session, id)

        if permission:
            return permission.is_active

    @classmethod
    def is_unique(cls, session, type: str, name: str) -> bool:
        return not Permission.query.filter_by(name=name, type=type).count()
