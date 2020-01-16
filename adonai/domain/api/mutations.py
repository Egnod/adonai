import graphene as gph
from .types import Domain
from ..crud import DomainCRUD
from ...app import db
from ...app.decorators import permissions_required
from ..permission import DomainPermissions
from flask import abort


class CreateDomain(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        name = gph.String(required=True)
        description = gph.String()

    domain = gph.Field(lambda: Domain)

    @permissions_required(DomainPermissions.create)
    def mutate(self, root, id: int, **arguments):
        domain_status = DomainCRUD.is_active(db.session, id)

        if domain_status is None:
            abort(404)

        elif not domain_status:
            abort(423)

        domain = DomainCRUD.create(db.session, arguments)

        return CreateDomain(domain=domain)


class UpdateDomain(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        name = gph.String()
        description = gph.String()

    domain = gph.Field(lambda: Domain)

    @permissions_required(DomainPermissions.update)
    def mutate(self, root, id: int, **argumnets):
        domain_status = DomainCRUD.is_active(db.session, id)

        print(domain_status)

        if domain_status is None:
            abort(404)

        elif not domain_status:
            abort(423)

        domain = DomainCRUD.update(db.session, id, argumnets)

        return UpdateDomain(domain=domain)


class ToggleDomain(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        is_active = gph.Boolean(required=True)

    domain = gph.Field(lambda: Domain)

    @permissions_required(DomainPermissions.delete)
    def mutate(self, root, id: int, is_active: bool):
        if not DomainCRUD.exists(db.session, id):
            abort(404)

        domain = DomainCRUD.update(db.session, id, {"is_active": is_active})

        return ToggleDomain(domain=domain)


class DomainMutation(gph.ObjectType):
    create_domain = CreateDomain.Field()
    update_domain = UpdateDomain.Field()
    toggle_domain = ToggleDomain.Field()
