from graphene_sqlalchemy import SQLAlchemyObjectType

from ..models import Domain as DomainModel


class Domain(SQLAlchemyObjectType):
    class Meta:
        model = DomainModel
