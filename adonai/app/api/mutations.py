from ...domain.api.mutations import DomainMutation
from ...user.api.mutations import UserMutation, UserGroupMutation


class Mutation(DomainMutation, UserMutation, UserGroupMutation):
    pass
