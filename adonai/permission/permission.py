from .internal.defaults import CRUDPermissions
from .internal.permission_set import InternalPermissionSet


class PermissionPermissions(InternalPermissionSet, CRUDPermissions):
    name = "permission"
