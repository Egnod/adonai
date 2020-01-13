from ..app.crud import CRUDBase
from .models import Domain

import typing
from sqlalchemy.orm.session import Session


class DomainCRUD(CRUDBase):
    model = Domain

    @classmethod
    def delete(
        cls, session: Session, id: int, commit: bool = True, autoflush: bool = False
    ) -> typing.Optional[bool]:
        obj = cls.get(session, id)

        if obj:
            if autoflush:
                session.flush()

            if commit:
                obj.is_active = False
                session.commit()

            return True
