from ..permission.internal.defaults import CRUDPermissions
from ..permission.internal.permission_set import InternalPermissionSet


class ProjectPermissions(InternalPermissionSet, CRUDPermissions):
    name = "project"
