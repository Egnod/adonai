from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from ..app import db


class Domain(db.Model):
    uuid = db.Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid4)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
