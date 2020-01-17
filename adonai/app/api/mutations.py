from ...domain.api.mutations import DomainMutation
from ...user.api.mutations import UserMutation


class Mutation(DomainMutation, UserMutation):
    pass
