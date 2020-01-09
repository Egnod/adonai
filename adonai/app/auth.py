import typing

from charybdis.app import jwt

from ..user.models import User


@jwt.authentication_handler
def authenticate(username: str, password: str) -> typing.Optional[User]:
    user = User.lookup(username)

    if user and user.check_password(password):
        return user


@jwt.identity_handler
def identity(payload: dict) -> typing.Optional[User]:
    user_id = payload["identity"]

    return User.query.get(user_id)
