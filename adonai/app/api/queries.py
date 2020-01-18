from ...domain.api.queries import DomainQuery
from ...project.api.queries import ProjectQuery
from ...user.api.queries import UserGroupQuery, UserQuery
from ...permission.api.queries import PermissionQuery


class Query(DomainQuery, UserQuery, UserGroupQuery, ProjectQuery, PermissionQuery):
    pass
