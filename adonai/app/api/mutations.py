from ...domain.api.mutations import DomainMutation
from ...user.api.mutations import UserMutation, UserGroupMutation
from ...project.api.mutations import ProjectMutation


class Mutation(DomainMutation, UserMutation, UserGroupMutation, ProjectMutation):
    pass
