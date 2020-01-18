from graphene import ID, Field, List, ObjectType

from ...app import db
from ...app.decorators import permissions_required
from ..crud import PermissionCRUD
from ..permission import PermissionPermissions
from .types import Permission


class PermissionQuery(ObjectType):
    permissions = List(Permission)
    get_permission = Field(Permission, id=ID(required=True))

    @permissions_required(PermissionPermissions.read)
    def resolve_permissions(self, info):
        return PermissionCRUD.objects(db.session)

    @permissions_required(PermissionPermissions.read)
    def resolve_get_permission(self, info, id: int):
        return PermissionCRUD.get(db.session, id)
