from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from ..app import db


class Project(db.Model):
    domain_id = db.Column(db.Integer, db.ForeignKey("domain.id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    uuid = db.Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid4)
    description = db.Column(db.Text)

    domain = db.relationship("Domain", backref="projects")
