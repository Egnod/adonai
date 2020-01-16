from .permission import InternalPermission


class CRUDPermissions:
    @classmethod
    def __init_defaults__(cls):
        cls.create = InternalPermission(f"{cls.name}_create")
        cls.delete = InternalPermission(f"{cls.name}_delete")
        cls.read = InternalPermission(f"{cls.name}_read")
        cls.update = InternalPermission(f"{cls.name}_update")

        return cls
