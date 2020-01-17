from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Permission as PermissionModel


class Permission(SQLAlchemyObjectType):
    class Meta:
        model = PermissionModel
