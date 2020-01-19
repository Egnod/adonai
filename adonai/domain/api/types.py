import graphene as gph
from graphene_sqlalchemy import SQLAlchemyObjectType

from ...app.api.resolver import permissionable_relation_resolver
from ...project.permission import ProjectPermissions
from ...user.permission import UserGroupPermissions, UserPermissions
from ..models import Domain as DomainModel


class Domain(SQLAlchemyObjectType):
    projects = gph.List(
        "adonai.project.api.types.Project",
        resolver=permissionable_relation_resolver(ProjectPermissions.read, "projects"),
    )

    users = gph.List(
        "adonai.user.api.types.User",
        resolver=permissionable_relation_resolver(UserPermissions.read, "users"),
    )

    groups = gph.List(
        "adonai.user.api.types.UserGroup",
        resolver=permissionable_relation_resolver(UserGroupPermissions.read, "groups"),
    )

    class Meta:
        model = DomainModel
