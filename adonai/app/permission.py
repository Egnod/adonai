from ..domain.permission import DomainPermissions
from ..permission.permission import PermissionPermissions
from ..project.permission import ProjectPermissions
from ..user.permission import (
    UserGroupPermissionPermissions,
    UserGroupPermissions,
    UserGroupUserPermissions,
    UserPermissionPermissions,
    UserPermissions,
)


def sync_internal_permissions():

    permission_sets = [
        DomainPermissions,
        PermissionPermissions,
        ProjectPermissions,
        UserPermissions,
        UserPermissionPermissions,
        UserGroupPermissions,
        UserGroupPermissionPermissions,
        UserGroupUserPermissions,
    ]

    for permission_set in permission_sets:
        if "__init_defaults__" in dir(permission_set):
            permission_set.__init_defaults__()
