from typing import Generic, TypeVar

from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
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
        cls,
        session: Session,
        lookup_field: str,
        lookup_value: any,
        *,
        order_by_field: str | None = None,
        desc: bool = False,
    ) -> list[T]:
        lookup_field: ColumnElement = getattr(cls.__model__, lookup_field)
        query = session.query(cls.__model__).where(lookup_field == lookup_value)
        if order_by_field:
            order_by_field: ColumnElement = getattr(cls.__model__, order_by_field)
            query = (
                query.order_by(order_by_field.desc())
                if desc
                else query.order_by(order_by_field)
            )
        return query.all()

    @classmethod
    def find_first_by_values(cls, session: Session, lookup: dict) -> T | None:
        query = session.query(cls.__model__)
        for field, value in lookup.items():
            lookup_field: ColumnElement = getattr(cls.__model__, field)
            query.filter(lookup_field == value)
        return query.first()

    @classmethod
    def create(cls, session: Session, instance: T) -> T:
        session.add(instance)
        session.commit()
        session.refresh(instance)
        return instance

    @classmethod
    def create_all(cls, session: Session, instances: list[T]) -> list[T]:
        session.add_all(instances)
        session.commit()
        for instance in instances:
            session.refresh(instance)
        return instances

    @classmethod
    def update(cls, session: Session, instance: T, update_data: dict) -> T:
        try:
            db_instance = (
                session.query(cls.__model__)
                .where(cls.__model__.id == instance.id)
                .one()
            )
        except NoResultFound:
            raise ValueError(
                f"{cls.__model__.__name__} with id={instance.id} not found"
            )
        for key, value in update_data.items():
            setattr(db_instance, key, value)
        session.commit()
        session.refresh(db_instance)
        return db_instance

    @classmethod
    def delete(cls, session: Session, instance: T) -> None:
        session.delete(instance)
        session.commit()

    @classmethod
    def delete_by_field(cls, session: Session, lookup_field: str, lookup_value: any):
        lookup_field: ColumnElement = getattr(cls.__model__, lookup_field)
        session.query(cls.__model__).where(lookup_field == lookup_value).delete()
        session.commit()
