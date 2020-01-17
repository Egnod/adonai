from ...domain.api.queries import DomainQuery
from ...user.api.queries import UserQuery


class Query(DomainQuery, UserQuery):
    pass
