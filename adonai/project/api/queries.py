from graphene import ID, Field, List, ObjectType

from ...app import db
from ...app.decorators import permissions_required
from ..crud import ProjectCRUD
from ..permission import ProjectPermissions
from .types import Project


class ProjectQuery(ObjectType):
    projects = List(Project)
    get_project = Field(Project, id=ID(required=True))

    @permissions_required(ProjectPermissions.read)
    def resolve_projects(self, info):
        return ProjectCRUD.objects(db.session)

    @permissions_required(ProjectPermissions.read)
    def resolve_get_project(self, info, id: int):
        return ProjectCRUD.get(db.session, id)

