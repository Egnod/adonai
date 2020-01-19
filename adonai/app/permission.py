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


def init_internal_permissions():
    for permission_set in permission_sets:
        if "__init_defaults__" in dir(permission_set):
            permission_set.__init_defaults__()


def get_internal_permissions_names():
    permissions_names = []

    for permission_set in permission_sets:
        permissions = permission_set.get_permissions()

        for permission in permissions:
            permissions_names.append(permission.name)

    return permissions_names
