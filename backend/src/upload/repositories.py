from sqlalchemy.orm import Session

from src.common.repository import BaseRepository
from src.models.reviewer import Reviewer, Source
from src.models.upload import Upload


class ReviewerRepository(BaseRepository[Reviewer]):
    __model__ = Reviewer

    @classmethod
    def create_reviewer(
        cls,
        db_session: Session,
        upload_id: int,
        name: str,
        surname: str,
        faculty: str,
        email: str,
        source: Source,
        article_doi: str,
    ) -> Reviewer:
        reviewer = Reviewer(
            upload_id=upload_id,
            name=name,
            surname=surname,
            faculty=faculty,
            email=email,
            source=source,
            article_doi=article_doi,
        )
        return cls.create(db_session, reviewer)


class UploadReviewer(BaseRepository[Upload]):
    __model__ = Upload

    @classmethod
    def create_upload(
        cls, db_session: Session, user_id: int, file_name: int, error: bool
    ) -> Upload:
        upload = Upload(user_id=user_id, file_name=file_name, error=error)
        return cls.create(db_session, upload)
