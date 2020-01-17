from graphene import ID, Field, List, ObjectType

from ....app import db
from ....app.decorators import permissions_required
from ...crud import UserCRUD
from ...permission import UserPermissions
from ..types import User


class UserQuery(ObjectType):
    users = List(User)
    get_user = Field(User, id=ID(required=True))

    @permissions_required(UserPermissions.read)
    def resolve_users(self, info):
        return UserCRUD.objects(db.session)

    @permissions_required(UserPermissions.read)
    def resolve_get_user(self, info, id: int):
        return UserCRUD.get(db.session, id)

