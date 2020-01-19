from http import HTTPStatus

from flask import abort
from flask_jwt import current_identity
from graphene import ID, UUID, Field, List, ObjectType, String

from ....app import db
from ....app.decorators import auth_required, permissions_required
from ...crud import UserCRUD
from ...permission import UserPermissions
from ..types import User


class UserQuery(ObjectType):
    current_user = Field(User)
    users = List(User)
    get_user = Field(User, id=ID(required=True))
    authenticate_user = Field(
        User, login=String(required=True), password=String(required=True)
    )

    identity_user = Field(User, uuid=UUID(required=True))

    @permissions_required(UserPermissions.read)
    def resolve_users(self, info):
        return UserCRUD.objects(db.session)

    @permissions_required(UserPermissions.read)
    def resolve_get_user(self, info, id: int):
        return UserCRUD.get(db.session, id)

    @auth_required
    def resolve_current_user(self, info):
        return UserCRUD.get(db.session, current_identity.id)

    @permissions_required(UserPermissions.read)
    def resolve_authenticate_user(self, info, login: str, password: str):
        user = UserCRUD.get_by_login(db.session, login)

        if user is None:
            abort(HTTPStatus.NOT_FOUND)

        if not user.check_password(password):
            abort(HTTPStatus.BAD_REQUEST)

        user_status = UserCRUD.is_global_active(db.session, user.id)

        if not user_status:
            abort(HTTPStatus.LOCKED)

        return user

    @permissions_required(UserPermissions.read)
    def resolve_identity_user(self, info, uuid: UUID):
        user = UserCRUD.get_by_uuid(db.session, uuid)

        if not user:
            abort(HTTPStatus.NOT_FOUND)

        return user
