from ..domain.permission import DomainPermissions
from ..permission.permission import PermissionPermissions
from ..project.permission import ProjectPermissions
from ..user.permission import UserPermissionPermissions, UserPermissions


def sync_internal_permissions():

    permission_sets = [
        DomainPermissions,
        PermissionPermissions,
        ProjectPermissions,
        UserPermissions,
        UserPermissionPermissions,
    ]

    for permission_set in permission_sets:
        permission_set.__init_defaults__()
