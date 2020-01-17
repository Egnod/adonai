import typing

from flask_jwt import JWTError

from ..user.crud import UserCRUD
from ..user.models import User
from . import db, jwt


@jwt.authentication_handler
def authenticate(username: str, password: str) -> typing.Optional[User]:
    user = UserCRUD.get_by_login(db.session, username)

    if user and user.check_password(password):
        if not user.internal_auth and UserCRUD.is_global_active(db.session, user.id):
            raise JWTError(
                "Forbidden", "Internal authentication not accepted", status_code=403
            )
        return user


@jwt.identity_handler
def identity(payload: dict) -> typing.Optional[User]:
    user_id = payload["identity"]

    return User.query.get(user_id)
