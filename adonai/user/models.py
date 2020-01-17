import re
from typing import List, Union
from uuid import uuid4

from passlib.hash import argon2
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint

from ..app import db


class User(db.Model):
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)

    login = db.Column(db.String, nullable=False)
    _password_hash = db.Column("password_hash", db.String, nullable=False)

    uuid = db.Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid4)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    domain = db.relationship("Domain", backref="users")

    def set_password_hash(self, value: str):
        self._password_hash = argon2.hash(value)

    password = property(None, set_password_hash)

    internal_auth = db.Column(db.Boolean, server_default="false", nullable=False)

    is_active = db.Column(db.Boolean, server_default="true", nullable=False)

    @db.validates("login")
    def login_validate(self, key: str, value: str) -> str:
        assert re.match(r"^[a-z0-9_-]{3,16}$", value) is not None

        return value

    def check_password(self, candidate: str) -> bool:
        return argon2.verify(candidate, self._password_hash)

    @property
    def groups(self) -> List["UserGroup"]:
        return [link.group for link in self.user_group_member_linker]

    @property
    def permissions(self) -> List["Permission"]:
        permissions = self.get_permissions(groups_exclude=True)
        permissions_list = []

        for permission in permissions:
            if permission.type in ("object", "action"):
                permissions_list.append(permission)

        return permissions_list

    @property
    def internal_permissions(self) -> List["Permission"]:
        permissions = self.get_permissions(groups_exclude=True)
        internal_permissions_list = []

        for permission in permissions:
            if permission.type == "internal":
                internal_permissions_list.append(permission)

        return internal_permissions_list

    def get_permissions(
        self, only_names: bool = False, groups_exclude: bool = False
    ) -> Union[List["Permission"], List[str]]:
        direct_permissions = [link.permission for link in self.user_permission_linker]

        group_permissions = []

        if not groups_exclude:
            for group in self.groups:
                group_permissions.extend(group.permissions)

        all_permissions = direct_permissions + group_permissions

        if only_names:
            all_permissions = [permission.name for permission in all_permissions]

        return list(set(all_permissions))


class UserPermission(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permission.id"), nullable=False
    )

    user = db.relationship("User", backref="user_permission_linker")
    permission = db.relationship("Permission")

    __table_args__ = (UniqueConstraint("user_id", "permission_id"),)


class UserGroup(db.Model):
    name = db.Column(db.String, nullable=False)
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)
    domain = db.relationship("Domain", backref="groups")

    @property
    def permissions(self) -> List["Permission"]:
        return [link.permission for link in self.group_permission_linker]

    @property
    def members(self) -> List["User"]:
        return [link.user for link in self.user_group_member_linker]


class UserGroupMember(db.Model):
    group_id = db.Column(db.Integer, db.ForeignKey("user_group.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    group = db.relationship("UserGroup", backref="user_group_member_linker")
    user = db.relationship("User", backref="user_group_member_linker")


class UserGroupPermission(db.Model):
    permission_id = db.Column(
        db.Integer, db.ForeignKey("permission.id"), nullable=False
    )
    group_id = db.Column(db.Integer, db.ForeignKey("user_group.id"), nullable=False)

    permission = db.relationship("Permission")
    group = db.relationship("UserGroup", backref="group_permission_linker")
