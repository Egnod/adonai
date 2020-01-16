import typing
from functools import wraps

from flask import abort
from flask_jwt import current_identity, jwt_required

from ..permission.internal.permission import InternalPermission


def auth_required(func: typing.Callable) -> typing.Callable:
    @wraps(func)
    @jwt_required()
    def wrapper(*args, **kwargs) -> typing.Callable:
        if not current_identity:
            abort(401)

        return func(*args, **kwargs)

    return wrapper


def permissions_required(
    requirement_permissions: typing.Union[
        InternalPermission, typing.List[InternalPermission]
    ]
) -> typing.Callable:
    if isinstance(requirement_permissions, InternalPermission):
        requirement_permissions = [requirement_permissions]

    def decorator(func: typing.Callable) -> typing.Callable:
        @wraps(func)
        @auth_required
        def wrappper(*args, **kwargs) -> typing.Any:

            current_permissions = [
                permission.name for permission in current_identity.internal_permissions
            ]
            permissions = [permission.name for permission in requirement_permissions]

            for permission in permissions:
                if permission not in current_permissions:
                    abort(403)

            return func(*args, **kwargs)

        return wrappper

    return decorator
