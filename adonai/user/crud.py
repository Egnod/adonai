from ..app.crud import CRUDBase
from .models import (
    User,
    UserGroup,
    UserGroupMember,
    UserGroupPermission,
    UserPermission,
)


class UserCRUD(CRUDBase):
    model = User

    @classmethod
    def get_by_login(cls, session, login: str) -> User:
        return User.query.filter_by(login=login).first()


class UserGroupCRUD(CRUDBase):
    model = UserGroup


class UserGroupMemberCRUD(CRUDBase):
    model = UserGroupMember


class UserGroupPermissionCRUD(CRUDBase):
    model = UserGroupPermission


class UserPermissionCRUD(CRUDBase):
    model = UserPermission
