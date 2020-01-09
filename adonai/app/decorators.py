import typing
from functools import wraps

from flask import abort
from flask_jwt import current_identity, jwt_required


def auth_required(func: typing.Callable) -> typing.Callable:
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs) -> typing.Callable:
        if not current_identity:
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def role_required(rolenames: typing.List[str]) -> typing.Callable:
    def decorator(func: typing.Callable) -> typing.Callable:
        @wraps(func)
        @auth_required
        def wrappper(*args, **kwargs) -> typing.Any:
            if current_identity.rolename not in rolenames:
                abort(403)

            return func(*args, **kwargs)

        return wrappper

    return decorator
