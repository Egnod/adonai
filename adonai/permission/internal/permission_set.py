from .permission import InternalPermission


class InternalPermissionSet:
    name: str

    @classmethod
    def get_permissions(cls):
        if getattr(cls, "__init_defaults__"):
            cls.__init_defaults__()

        attrs = vars(cls)
        permissions_list = []

        for attr_name in attrs:
            attr = attrs[attr_name]

            if isinstance(attr, InternalPermission):
                permissions_list.append(attr)

        return permissions_list
