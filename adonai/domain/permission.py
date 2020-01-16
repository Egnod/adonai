from ..permission.internal.permission_set import InternalPermissionSet
from ..permission.internal.defaults import CRUDPermissions


class DomainPermissions(InternalPermissionSet, CRUDPermissions):
    name = "domain"

