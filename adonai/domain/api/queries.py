from graphene import ID, Field, List, ObjectType

from ...app import db
from ...app.decorators import permissions_required
from ..crud import DomainCRUD
from ..permission import DomainPermissions
from .types import Domain


class DomainQuery(ObjectType):
    domains = List(Domain)
    get_domain = Field(Domain, id=ID(required=True))

    @permissions_required(DomainPermissions.read)
    def resolve_domains(self, info):
        return DomainCRUD.objects(db.session)

    @permissions_required(DomainPermissions.read)
    def resolve_get_domain(self, info, id: int):
        return DomainCRUD.get(db.session, id)
