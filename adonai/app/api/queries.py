from ...domain.api.queries import DomainQuery
from ...permission.api.queries import PermissionQuery
from ...project.api.queries import ProjectQuery
from ...user.api.queries import UserGroupQuery, UserQuery


class Query(DomainQuery, UserQuery, UserGroupQuery, ProjectQuery, PermissionQuery):
    pass
