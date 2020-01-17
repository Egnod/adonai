from ..permission.internal.defaults import CRUDPermissions
from ..permission.internal.permission_set import InternalPermissionSet


class UserPermissions(InternalPermissionSet, CRUDPermissions):
    name = "user"


class UserPermissionPermissions(InternalPermissionSet, CRUDPermissions):
    name = "user_permission"
