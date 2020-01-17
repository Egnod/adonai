from ...domain.api.queries import DomainQuery
from ...user.api.queries import UserQuery, UserGroupQuery


class Query(DomainQuery, UserQuery, UserGroupQuery):
    pass
