from typing import Generic, TypeVar

from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session
from src.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseRepository(Generic[T]):
    __model__: BaseModel

    @classmethod
    def all(cls, session: Session) -> list[T]:
        return session.query(cls.__model__).all()

    @classmethod
    def find_by_id(cls, session: Session, lookup_id: int) -> T | None:
        return session.query(cls.__model__).where(cls.__model__.id == lookup_id).first()

    @classmethod
    def find_first_by_value(
        cls, session: Session, lookup_field: str, lookup_value: any
    ) -> T | None:
        lookup_field: ColumnElement = getattr(cls.__model__, lookup_field)
        return session.query(cls.__model__).where(lookup_field == lookup_value).first()

    @classmethod
    def find_all_by_value(
        cls, session: Session, lookup_field: str, lookup_value: any
    ) -> list[T]:
        lookup_field: ColumnElement = getattr(cls.__model__, lookup_field)
        return session.query(cls.__model__).where(lookup_field == lookup_value).all()

    @classmethod
    def create(cls, session: Session, instance: T) -> T:
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def delete(cls, session: Session, instance: T) -> None:
        session.delete(instance)
        session.commit()
