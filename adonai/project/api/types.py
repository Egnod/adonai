import graphene as gph
from graphene_sqlalchemy import SQLAlchemyObjectType

from ...app.api.resolver import permissionable_relation_resolver
from ...domain.permission import DomainPermissions
from ...permission.permission import PermissionPermissions
from ..models import Project as ProjectModel


class Project(SQLAlchemyObjectType):
    domain = gph.Field(
        "adonai.domain.api.types.Domain",
        resolver=permissionable_relation_resolver(DomainPermissions.read, "domain"),
    )
    permissions = gph.List(
        "adonai.permission.api.types.Permission",
        resolver=permissionable_relation_resolver(
            PermissionPermissions.read, "permissions"
        ),
    )

    class Meta:
        model = ProjectModel
