from ...domain.api.mutations import DomainMutation
from ...permission.api.mutations import PermissionMutation
from ...project.api.mutations import ProjectMutation
from ...user.api.mutations import UserGroupMutation, UserMutation


class Mutation(
    DomainMutation, UserMutation, UserGroupMutation, ProjectMutation, PermissionMutation
):
    pass
