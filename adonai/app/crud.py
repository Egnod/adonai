import typing
from abc import ABCMeta

from sqlalchemy.ext.declarative.api import DeclarativeMeta
from sqlalchemy.orm.session import Session


class CRUDBase(metaclass=ABCMeta):
    model: DeclarativeMeta = None

    @classmethod
    def objects(cls, session: Session) -> typing.List[typing.Optional[DeclarativeMeta]]:
        return session.query(cls.model).all()

    @classmethod
    def create(
        cls,
        session: Session,
        params: typing.Dict[str, typing.Any],
        commit: bool = True,
        autoflush: bool = False,
    ) -> DeclarativeMeta:
        obj = cls.model(**params)

        session.add(obj)

        if commit:
            session.commit()

            session.refresh(obj)

        if autoflush:
            session.flush()

        return obj

    @classmethod
    def get(cls, session: Session, id: int) -> typing.Optional[DeclarativeMeta]:
        return session.query(cls.model).get(id)

    @classmethod
    def update(
        cls,
        session: Session,
        id: int,
        params: typing.Dict[str, typing.Any],
        commit: bool = True,
        autoflush: bool = False,
    ) -> DeclarativeMeta:
        obj = cls.get(session, id)

        if obj:
            for param in params:

                setattr(obj, param, params[param])

            if commit:
                session.commit()

                session.refresh(obj)

            if autoflush:
                session.flush()

            return obj

    @classmethod
    def delete(
        cls, session: Session, id: int, commit: bool = True, autoflush: bool = False
    ) -> typing.Optional[bool]:
        obj = cls.get(session, id)

        if obj:
            if autoflush:
                session.flush()

            if commit:
                session.delete(obj)
                session.commit()

            return True
