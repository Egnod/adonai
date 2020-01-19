from ..decorators import permissions_required
from ...permission.internal.permission import InternalPermission
from ..crud import CRUDBase
from typing import Union, List
from .. import db


def permissionable_relation_resolver(permissions: Union[InternalPermission, List[InternalPermission]], relation_attribute_name: str):
    @permissions_required(permissions)
    def resolver(root, info):
        relation = getattr(root, relation_attribute_name, None)
        return relation

    return resolver
