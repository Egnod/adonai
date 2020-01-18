from http import HTTPStatus

import graphene as gph
from flask import abort

from ...app import db
from ...app.decorators import permissions_required
from ...domain.crud import DomainCRUD
from ..crud import ProjectCRUD
from ..permission import ProjectPermissions
from .types import Project


class CreateProject(gph.Mutation):
    class Arguments:
        name = gph.String(required=True)
        description = gph.String()
        domain_id = gph.ID(required=True)

    project = gph.Field(lambda: Project)

    @permissions_required(ProjectPermissions.create)
    def mutate(self, root, **arguments):
        if not DomainCRUD.is_active(db.session, arguments["domain_id"]):
            abort(HTTPStatus.LOCKED)

        project = ProjectCRUD.create(db.session, arguments)

        return CreateProject(project=project)


class UpdateProject(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        name = gph.String(required=True)
        description = gph.String()

    project = gph.Field(lambda: Project)

    @permissions_required(ProjectPermissions.update)
    def mutate(self, root, id: int, **arguments):
        project = ProjectCRUD.is_active(db.session, id)

        if project is None:
            abort(HTTPStatus.NOT_FOUND)

        elif not project:
            abort(HTTPStatus.LOCKED)

        project = ProjectCRUD.update(db.session, id, arguments)

        return UpdateProject(project=project)


class ToggleProject(gph.Mutation):
    class Arguments:
        id = gph.ID(required=True)
        is_active = gph.Boolean(required=True)

    project = gph.Field(lambda: Project)

    @permissions_required(ProjectPermissions.delete)
    def mutate(self, root, id: int, is_active: bool):
        project = ProjectCRUD.get(db.session, id)

        if not project:
            abort(HTTPStatus.NOT_FOUND)

        if not DomainCRUD.is_active(db.session, project.domain_id):
            abort(HTTPStatus.LOCKED)

        project = ProjectCRUD.update(db.session, id, {"is_active": is_active})

        return ToggleProject(project=project)


class ProjectMutation(gph.ObjectType):
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    toggle_project = ToggleProject.Field()
