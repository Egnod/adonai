from http import HTTPStatus

import graphene as gph
from flask import abort

from ...app import db
from ...app.decorators import permissions_required
from ...project.crud import ProjectCRUD
from ..crud import PermissionCRUD
from ..permission import PermissionPermissions
from .types import Permission


class CreatePermission(gph.Mutation):
    class Arguments:
        name = gph.String(required=True)
        description = gph.String()
        project_id = gph.ID()
        type = gph.String(required=True)

    permission = gph.Field(lambda: Permission)

    @permissions_required(PermissionPermissions.create)
    def mutate(self, root, **arguments):
        if "project_id" in arguments and not ProjectCRUD.is_global_active(
            db.session, arguments["project_id"]
        ):
            abort(HTTPStatus.LOCKED)

        if not PermissionCRUD.is_unique(
            db.session, arguments["type"], arguments["name"]
        ):
            abort(HTTPStatus.CONFLICT)

        permission = PermissionCRUD.create(db.session, arguments)

        return CreatePermission(permission=permission)


class UpdatePermission(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        description = gph.String()

    permission = gph.Field(lambda: Permission)

    @permissions_required(PermissionPermissions.update)
    def mutate(self, root, id: int, **arguments):
        permission = PermissionCRUD.is_active(db.session, id)

        if permission is None:
            abort(HTTPStatus.NOT_FOUND)

        elif not permission:
            abort(HTTPStatus.LOCKED)

        permission = PermissionCRUD.update(db.session, id, arguments)

        return UpdatePermission(permission=permission)


class TogglePermission(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        is_active = gph.Boolean(required=True)

    permission = gph.Field(lambda: Permission)

    @permissions_required(PermissionPermissions.delete)
    def mutate(self, root, id: int, is_active: bool):
        permission = PermissionCRUD.get(db.session, id)

        if not permission:
            abort(HTTPStatus.NOT_FOUND)

        if not ProjectCRUD.is_global_active(db.session, permission.project_id):
            abort(HTTPStatus.LOCKED)

        permission = PermissionCRUD.update(db.session, id, {"is_active": is_active})

        return TogglePermission(permission=permission)


class PermissionMutation(gph.ObjectType):
    create_permission = CreatePermission.Field()
    update_permission = UpdatePermission.Field()
    toggle_permission = TogglePermission.Field()
