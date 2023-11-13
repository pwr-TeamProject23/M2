from typing import TypeVar, Generic
from sqlalchemy.orm import Session

from src.models import BaseModel

T = TypeVar("T", bound=BaseModel)


class BaseModelManager(Generic[T]):
    __model__: BaseModel

    @classmethod
    def all(cls, db: Session) -> list[T]:
        return db.query(cls.__model__).all()

    @classmethod
    def find_by_id(cls, db: Session, model_id: int) -> T | None:
        return db.query(cls.__model__).where(cls.__model__.id == model_id).first()

    @classmethod
    def create(cls, db: Session, instance: T) -> T:
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def delete(cls, db: Session, instance: T) -> None:
        db.delete(instance)
        db.commit()