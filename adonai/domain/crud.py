from sqlalchemy.orm.session import Session

from ..app.crud import CRUDBase
from .models import Domain


class DomainCRUD(CRUDBase):
    model = Domain

    @classmethod
    def is_active(cls, session: Session, id: int) -> bool:
        domain = cls.get(session, id)

        if domain is not None:
            return domain.is_active
