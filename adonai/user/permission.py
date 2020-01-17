from ..permission.internal.defaults import CRUDPermissions
from ..permission.internal.permission_set import InternalPermissionSet


class UserPermissions(InternalPermissionSet, CRUDPermissions):
    name = "user"


class UserPermissionPermissions(InternalPermissionSet, CRUDPermissions):
    name = "user_permission"


class UserGroupPermissions(InternalPermissionSet, CRUDPermissions):
    name = "user_group"


class UserGroupPermissionPermissions(InternalPermissionSet, CRUDPermissions):
    name = "user_group_permission"


class UserGroupUserPermissions(InternalPermissionSet, CRUDPermissions):
    name = "user_group_user"
