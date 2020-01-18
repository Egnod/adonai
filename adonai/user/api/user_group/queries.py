from graphene import ID, Field, List, ObjectType

from ....app import db
from ....app.decorators import permissions_required
from ...crud import UserGroupCRUD
from ...permission import UserGroupPermissions
from ..types import UserGroup


class UserGroupQuery(ObjectType):
    user_groups = List(UserGroup)
    get_user_group = Field(UserGroup, id=ID(required=True))

    @permissions_required(UserGroupPermissions.read)
    def resolve_user_groups(self, info):
        return UserGroupCRUD.objects(db.session)

    @permissions_required(UserGroupPermissions.read)
    def resolve_get_user_group(self, info, id: int):
        return UserGroupCRUD.get(db.session, id)
