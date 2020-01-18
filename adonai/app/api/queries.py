from ...domain.api.queries import DomainQuery
from ...project.api.queries import ProjectQuery
from ...user.api.queries import UserGroupQuery, UserQuery


class Query(DomainQuery, UserQuery, UserGroupQuery, ProjectQuery):
    pass
