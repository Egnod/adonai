from typing import List, Union

from ...permission.internal.permission import InternalPermission
from ..decorators import permissions_required


def permissionable_relation_resolver(
    permissions: Union[InternalPermission, List[InternalPermission]],
    relation_attribute_name: str,
):
    @permissions_required(permissions)
    def resolver(root, info):
        relation = getattr(root, relation_attribute_name, None)
        return relation

    return resolver
