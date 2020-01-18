from ...domain.api.mutations import DomainMutation
from ...project.api.mutations import ProjectMutation
from ...user.api.mutations import UserGroupMutation, UserMutation


class Mutation(DomainMutation, UserMutation, UserGroupMutation, ProjectMutation):
    pass
