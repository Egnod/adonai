from http import HTTPStatus

import graphene as gph
from flask import abort

from ....app import db
from ....app.decorators import permissions_required
from ....domain.crud import DomainCRUD
from ....permission.crud import PermissionCRUD
from ...crud import UserCRUD, UserPermissionCRUD
from ...permission import UserPermissionPermissions, UserPermissions
from ..types import User


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
        domain_status = DomainCRUD.is_active(db.session, arguments["domain_id"])
        if domain_status is None:
            abort(HTTPStatus.NOT_FOUND)
        
        elif not domain_status:
            abort(HTTPStatus.LOCKED)

        user = UserCRUD.create(db.session, arguments)

        return CreateUser(user=user)


class UpdateUser(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        password = gph.String()
        first_name = gph.String()
        last_name = gph.String()

    user = gph.Field(lambda: User)

    @permissions_required(UserPermissions.update)
    def mutate(self, root, id: int, **arguments):
        user_status = UserCRUD.is_active(db.session, id)

        if user_status is None:
            abort(HTTPStatus.NOT_FOUND)

        elif not user_status:
            abort(HTTPStatus.LOCKED)

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
            abort(HTTPStatus.NOT_FOUND)

        if not DomainCRUD.is_active(db.session, user.domain_id):
            abort(HTTPStatus.LOCKED)

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
        permission_status = PermissionCRUD.is_active(
            db.session, argumnets["permission_id"]
        )

        if user_status is None or permission_status is None:
            abort(HTTPStatus.NOT_FOUND)

        elif not user_status or not permission_status:
            abort(HTTPStatus.LOCKED)

        if not UserPermissionCRUD.is_unique(
            db.session, argumnets["user_id"], argumnets["permission_id"]
        ):
            abort(HTTPStatus.CONFLICT)

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
            abort(HTTPStatus.NOT_FOUND)

        UserPermissionCRUD.delete(db.session, user_permission.id)

        return DemotePermissionUser(deleted=True)


class UserMutation(gph.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    toggle_user = ToggleUser.Field()
    delegate_permission_to_user = DelegatePermissionUser.Field()
    demote_permission_from_user = DemotePermissionUser.Field()
