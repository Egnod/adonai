from graphene_sqlalchemy import SQLAlchemyObjectType
import graphene as gph

from ..models import User as UserModel
from ..models import UserGroup as UserGroupModel
from ...permission.api.types import Permission


class UserGroup(SQLAlchemyObjectType):
    class Meta:
        model = UserGroupModel

    permissions = gph.List(Permission)
    members = gph.List("adonai.user.api.types.User")


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        exclude_fields = (UserModel._password_hash.key,)

    groups = gph.List(UserGroup)
    permissions = gph.List(Permission)
    internal_permissions = gph.List(Permission)
