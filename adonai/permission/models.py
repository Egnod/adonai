from sqlalchemy.dialects.postgresql import UUID, ENUM
from uuid import uuid4
from sqlalchemy.schema import CheckConstraint

from ..app import db
import re


class Permission(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text)
    type = db.Column(ENUM("internal", "action", "object", name="permission_type"))

    project = db.relationship("Project", backref="permissions")

    __table_args__ = (CheckConstraint("NOT(project_id IS NULL AND type IS NULL)"),)

    @db.validates("name")
    def name_validate(self, key: str, value: str) -> str:
        assert re.match(r"^[a-z0-9_-]{3,16}$", value) is not None

        return value
