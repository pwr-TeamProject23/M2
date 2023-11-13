from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

from .session import UserSession
from .user import User
from .upload import Upload
from .reviewer import Reviewer
