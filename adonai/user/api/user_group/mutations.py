from http import HTTPStatus


import graphene as gph
from flask import abort

from ..types import UserGroup
from ...crud import (
    UserGroupCRUD,
    UserCRUD,
    UserPermissionCRUD,
    UserGroupPermissionCRUD,
    UserGroupMemberCRUD,
)
from ....domain.crud import DomainCRUD
from ....app import db
from ....app.decorators import permissions_required
from ...permission import (
    UserPermissions,
    UserPermissionPermissions,
    UserGroupPermissions,
    UserGroupPermissionPermissions,
    UserGroupUserPermissions,
)
from ....permission.crud import PermissionCRUD


class CreateUserGroup(gph.Mutation):
    class Arguments:
        name = gph.String(required=True)
        domain_id = gph.ID(required=True)

    user_group = gph.Field(lambda: UserGroup)

    @permissions_required(UserGroupPermissions.create)
    def mutate(self, root, **arguments):
        domain_status = DomainCRUD.is_active(db.session, arguments["domain_id"])
        if domain_status is None:
            abort(HTTPStatus.NOT_FOUND)
        elif not domain_status:
            abort(HTTPStatus.LOCKED)

        user_group = UserGroupCRUD.create(db.session, arguments)

        return CreateUserGroup(user_group=user_group)


class UpdateUserGroup(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        name = gph.String()

    user_group = gph.Field(lambda: UserGroup)

    @permissions_required(UserPermissions.update)
    def mutate(self, root, id: int, **arguments):
        user_group_status = UserGroupCRUD.is_active(db.session, id)

        if user_group_status is None:
            abort(HTTPStatus.NOT_FOUND)

        elif not user_group_status:
            abort(HTTPStatus.LOCKED)

        user_group = UserGroupCRUD.update(db.session, id, arguments)

        return UpdateUserGroup(user_group=user_group)


class ToggleUserGroup(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        is_active = gph.Boolean(required=True)

    user_group = gph.Field(lambda: UserGroup)

    @permissions_required(UserGroupPermissions.delete)
    def mutate(self, root, id: int, is_active: bool):
        user_group = UserCRUD.get(db.session, id)

        if not user_group:
            abort(HTTPStatus.NOT_FOUND)

        if not DomainCRUD.is_active(db.session, user_group.domain_id):
            abort(HTTPStatus.LOCKED)

        user_group = UserGroupCRUD.update(db.session, id, {"is_active": is_active})

        return ToggleUserGroup(user_group=user_group)


class DelegatePermissionGroup(gph.Mutation):
    class Arguments:
        group_id = gph.ID(required=True)
        permission_id = gph.ID(required=True)

    user_group = gph.Field(lambda: UserGroup)

    @permissions_required(UserGroupPermissionPermissions.create)
    def mutate(self, root, **argumnets):
        user_group_status = UserGroupCRUD.is_active(db.session, argumnets["group_id"])
        permission_status = PermissionCRUD.is_active(
            db.session, argumnets["permission_id"]
        )

        if user_group_status is None or permission_status is None:
            abort(HTTPStatus.NOT_FOUND)

        elif not user_group_status or not permission_status:
            abort(HTTPStatus.LOCKED)

        if not UserGroupPermissionCRUD.is_unique(
            db.session, argumnets["group_id"], argumnets["permission_id"]
        ):
            abort(HTTPStatus.CONFLICT)

        UserGroupPermissionCRUD.create(db.session, argumnets)

        return DelegatePermissionGroup(
            user_group=UserGroupCRUD.get(db.session, argumnets["group_id"])
        )


class DemotePermissionGroup(gph.Mutation):
    class Arguments:
        group_id = gph.ID(required=True)
        permission_id = gph.ID(required=True)

    deleted = gph.Boolean()

    @permissions_required(UserGroupPermissionPermissions.delete)
    def mutate(self, root, **argumnets):

        user_group_permission = UserGroupPermissionCRUD.get_by_pair(
            db.session, **argumnets
        )

        if not user_group_permission:
            abort(HTTPStatus.NOT_FOUND)

        UserGroupPermissionCRUD.delete(db.session, user_group_permission.id)

        return DemotePermissionGroup(deleted=True)


class DelegateUserGroup(gph.Mutation):
    class Arguments:
        group_id = gph.ID(required=True)
        user_id = gph.ID(required=True)

    user_group = gph.Field(lambda: UserGroup)

    @permissions_required(UserGroupUserPermissions.create)
    def mutate(self, root, **argumnets):
        user_group_status = UserGroupCRUD.is_active(db.session, argumnets["group_id"])
        user_status = UserCRUD.is_active(db.session, argumnets["user_id"])

        if user_group_status is None or user_status is None:
            abort(HTTPStatus.NOT_FOUND)

        elif not user_group_status or not user_status:
            abort(HTTPStatus.LOCKED)

        if not UserGroupMemberCRUD.is_unique(
            db.session, argumnets["group_id"], argumnets["user_id"]
        ):
            abort(HTTPStatus.CONFLICT)

        UserGroupMemberCRUD.create(db.session, argumnets)

        return DelegateUserGroup(
            user_group=UserGroupCRUD.get(db.session, argumnets["group_id"])
        )


class DemoteUserGroup(gph.Mutation):
    class Arguments:
        user_id = gph.ID(required=True)
        group_id = gph.ID(required=True)

    deleted = gph.Boolean()

    @permissions_required(UserGroupUserPermissions.delete)
    def mutate(self, root, **argumnets):

        user_group_user = UserGroupMemberCRUD.get_by_pair(db.session, **argumnets)

        if not user_group_user:
            abort(HTTPStatus.NOT_FOUND)

        UserGroupMemberCRUD.delete(db.session, user_group_user.id)

        return DemoteUserGroup(deleted=True)


class UserGroupMutation(gph.ObjectType):
    create_user_group = CreateUserGroup.Field()
    update_user_group = UpdateUserGroup.Field()
    toggle_user_group = ToggleUserGroup.Field()
    delegate_permission_to_user_group = DelegatePermissionGroup.Field()
    demote_permission_from_user_group = DemotePermissionGroup.Field()
    delegate_user_to_user_group = DelegateUserGroup.Field()
    demote_user_from_user_group = DemoteUserGroup.Field()
