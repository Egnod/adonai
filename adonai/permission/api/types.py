import graphene as gph
from graphene_sqlalchemy import SQLAlchemyObjectType

from ...app.api.resolver import permissionable_relation_resolver
from ...project.permission import ProjectPermissions
from ..models import Permission as PermissionModel


class Permission(SQLAlchemyObjectType):
    class Meta:
        model = PermissionModel

    project = gph.Field(
        "adonai.project.api.types.Project",
        resolver=permissionable_relation_resolver(ProjectPermissions.read, "project"),
    )
