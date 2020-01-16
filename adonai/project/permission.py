from ..permission.internal.permission_set import InternalPermissionSet
from ..permission.internal.defaults import CRUDPermissions


class ProjectPermissions(InternalPermissionSet, CRUDPermissions):
    name = "project"
