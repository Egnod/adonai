from ...domain.api.mutations import DomainMutation
from ...project.api.mutations import ProjectMutation
from ...user.api.mutations import UserGroupMutation, UserMutation
from ...permission.api.mutations import PermissionMutation


class Mutation(
    DomainMutation, UserMutation, UserGroupMutation, ProjectMutation, PermissionMutation
):
    pass
