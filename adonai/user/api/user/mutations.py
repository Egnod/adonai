import graphene as gph
from flask import abort

from ..types import User
from ...crud import UserCRUD, UserPermissionCRUD
from ....domain.crud import DomainCRUD
from ....app import db
from ....app.decorators import permissions_required
from ...permission import UserPermissions, UserPermissionPermissions


class CreateUser(gph.Mutation):
    class Arguments:
        login = gph.String(required=True)
        password = gph.String(required=True)
        first_name = gph.String(required=True)
        last_name = gph.String(required=True)
        domain_id = gph.ID(required=True)
        internal_auth = gph.Boolean()

    user = gph.Field(lambda: User)

    @permissions_required(UserPermissions.create)
    def mutate(self, root, **arguments):

        user = UserCRUD.create(db.session, arguments)

        return CreateUser(user=user)


class UpdateUser(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        login = gph.String()
        password = gph.String()
        first_name = gph.String()
        last_name = gph.String()
        internal_auth = gph.Boolean()
        domain_id = gph.ID()

    user = gph.Field(lambda: User)

    @permissions_required(UserPermissions.update)
    def mutate(self, root, id: int, **arguments):
        user_status = UserCRUD.is_active(db.session, id)

        if user_status is None:
            abort(404)

        elif not user_status:
            abort(423)

        user = UserCRUD.update(db.session, id, arguments)

        return UpdateUser(user=user)


class ToggleUser(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        is_active = gph.Boolean(required=True)

    user = gph.Field(lambda: User)

    @permissions_required(UserPermissions.delete)
    def mutate(self, root, id: int, is_active: bool):
        user = UserCRUD.get(db.session, id)

        if not user:
            abort(404)

        if not DomainCRUD.is_active(db.session, user.domain_id):
            abort(423)

        user = UserCRUD.update(db.session, id, {"is_active": is_active})

        return ToggleUser(user=user)


class DelegatePermissionUser(gph.Mutation):
    class Arguments:
        user_id = gph.ID(required=True)
        permission_id = gph.ID(required=True)

    user = gph.Field(lambda: User)

    @permissions_required(UserPermissionPermissions.create)
    def mutate(self, root, **argumnets):
        user_status = UserCRUD.is_active(db.session, argumnets["user_id"])

        if user_status is None:
            abort(404)

        elif not user_status:
            abort(423)

        if not UserPermissionCRUD.is_unique(
            db.session, argumnets["user_id"], argumnets["permission_id"]
        ):
            abort(409)

        UserPermissionCRUD.create(db.session, argumnets)

        return DelegatePermissionUser(
            user=UserCRUD.get(db.session, argumnets["user_id"])
        )


class DemotePermissionUser(gph.Mutation):
    class Arguments:
        user_id = gph.ID(required=True)
        permission_id = gph.ID(required=True)

    deleted = gph.Boolean()

    @permissions_required(UserPermissionPermissions.delete)
    def mutate(self, root, **argumnets):

        user_permission = UserPermissionCRUD.get_by_pair(db.session, **argumnets)

        if not user_permission:
            abort(404)

        UserPermissionCRUD.delete(db.session, user_permission.id)

        return DemotePermissionUser(deleted=True)


class UserMutation(gph.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    toggle_user = ToggleUser.Field()
    delegate_permission_to_user = DelegatePermissionUser.Field()
    demote_permission_from_user = DemotePermissionUser.Field()
