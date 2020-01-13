from sqlalchemy.dialects.postgresql import UUID, ENUM
from uuid import uuid4
from sqlalchemy.schema import CheckConstraint
from passlib.hash import argon2
from typing import List, Union
from ..app import db
import re


class User(db.Model):
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)

    login = db.Column(db.String, nullable=False)
    _password_hash = db.Column("password_hash", db.String, nullable=False)

    uuid = db.Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid4)

    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)

    domain = db.relationship("Domain", backref="users")

    def set_password_hash(self, value: str):
        self.password_hash = argon2.hash(value)

    password = property(None, set_password_hash)

    @db.validates("login")
    def login_validate(self, key: str, value: str) -> str:
        assert re.match(r"^[a-z0-9_-]{3,16}$", value) is not None

        return value

    def check_password(self, candidate: str) -> bool:
        return argon2.verify(candidate, self.password_hash)

    @property
    def groups(self) -> List["UserGroup"]:
        return [link.group for link in self.user_group_member_linker]

    @property
    def permissions(self) -> List["Permission"]:
        return self.get_permissions(groups_exclude=True)

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


class UserGroup(db.Model):
    name = db.Column(db.String, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    project = db.relationship("Project", backref="groups")

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
