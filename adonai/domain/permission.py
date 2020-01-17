from ..permission.internal.defaults import CRUDPermissions
from ..permission.internal.permission_set import InternalPermissionSet


class DomainPermissions(InternalPermissionSet, CRUDPermissions):
    name = "domain"
