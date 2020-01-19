import graphene as gph
from graphene_sqlalchemy import SQLAlchemyObjectType

from ...app.api.resolver import permissionable_relation_resolver
from ...domain.permission import DomainPermissions
from ...permission.permission import PermissionPermissions
from ...user.permission import UserPermissions
from ..models import User as UserModel
from ..models import UserGroup as UserGroupModel
from ..permission import UserGroupPermissions


class UserGroup(SQLAlchemyObjectType):
    class Meta:
        model = UserGroupModel

    permissions = gph.List(
        "adonai.permission.api.types.Permission",
        resolver=permissionable_relation_resolver(
            PermissionPermissions.read, "permissions"
        ),
    )

    members = gph.List(
        "adonai.user.api.types.User",
        resolver=permissionable_relation_resolver(UserPermissions.read, "members"),
    )

    domain = gph.Field(
        "adonai.domain.api.types.Domain",
        resolver=permissionable_relation_resolver(DomainPermissions.read, "domain"),
    )


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = (UserModel._password_hash.key,)

    groups = gph.List(
        "adonai.user.api.types.UserGroup",
        resolver=permissionable_relation_resolver(UserGroupPermissions.read, "groups"),
    )

    permissions = gph.List(
        "adonai.permission.api.types.Permission",
        resolver=permissionable_relation_resolver(
            PermissionPermissions.read, "permissions"
        ),
    )

    internal_permissions = gph.List(
        "adonai.permission.api.types.Permission",
        resolver=permissionable_relation_resolver(
            PermissionPermissions.read, "internal_permissions"
        ),
    )

    domain = gph.Field(
        "adonai.domain.api.types.Domain",
        resolver=permissionable_relation_resolver(DomainPermissions.read, "domain"),
    )
