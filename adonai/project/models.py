from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from ..app import db


class Project(db.Model):
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    uuid = db.Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid4)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, server_default="true", nullable=False)

    domain = db.relationship("Domain", backref="projects")
