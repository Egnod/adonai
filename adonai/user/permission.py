from ..permission.internal.permission_set import InternalPermissionSet
from ..permission.internal.defaults import CRUDPermissions


class UserPermissions(InternalPermissionSet, CRUDPermissions):
    name = "user"
