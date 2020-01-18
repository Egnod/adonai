from ...domain.api.queries import DomainQuery
from ...user.api.queries import UserQuery, UserGroupQuery
from ...project.api.queries import ProjectQuery


class Query(DomainQuery, UserQuery, UserGroupQuery, ProjectQuery):
    pass
