from .internal.permission_set import InternalPermissionSet
from .internal.defaults import CRUDPermissions


class PermissionPermissions(InternalPermissionSet, CRUDPermissions):
    name = "permission"

