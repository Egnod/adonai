import re

from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.schema import CheckConstraint, UniqueConstraint

from ..app import db


class Permission(db.Model):
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    type = db.Column(ENUM("internal", "action", "object", name="permission_type"))

    project = db.relationship("Project", backref="permissions")

    __table_args__ = (
        CheckConstraint("NOT(project_id IS NULL AND type IS NULL)"),
        UniqueConstraint(
            "name", "type", name="unique_name_and_type_on_permission_table"
        ),
    )

    @db.validates("name")
    def name_validate(self, key: str, value: str) -> str:
        assert re.match(r"^[a-z0-9_-]{3,16}$", value) is not None

        return value
