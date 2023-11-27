from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

from src.models.author import Author
from src.models.session import UserSession
from src.models.upload import Upload
from src.models.user import User
