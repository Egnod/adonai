from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Project as ProjectModel


class Project(SQLAlchemyObjectType):
    class Meta:
        model = ProjectModel
