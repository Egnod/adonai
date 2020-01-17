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

    @classmethod
    def is_active(cls, session, id: int) -> bool:
        user: User = cls.get(session, id)

        if user:
            return user.is_active

    @classmethod
    def is_global_active(cls, session, id: int) -> bool:
        user: User = cls.get(session, id)

        if not user:
            return None

        else:
            return user.domain.is_active and user.is_active


class UserGroupCRUD(CRUDBase):
    model = UserGroup


class UserGroupMemberCRUD(CRUDBase):
    model = UserGroupMember


class UserGroupPermissionCRUD(CRUDBase):
    model = UserGroupPermission


class UserPermissionCRUD(CRUDBase):
    model = UserPermission

    @classmethod
    def get_by_pair(cls, session, user_id: int, permission_id: int):
        return UserPermission.query.filter_by(
            user_id=user_id, permission_id=permission_id
        ).first()

    @classmethod
    def is_unique(cls, session, user_id: int, permission_id: int):
        return not (
            UserPermission.query.filter_by(
                user_id=user_id, permission_id=permission_id
            ).count()
            == True
        )
