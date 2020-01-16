from .queries import Query
from .mutations import Mutation
from graphene import Schema

schema = Schema(query=Query, mutation=Mutation)

