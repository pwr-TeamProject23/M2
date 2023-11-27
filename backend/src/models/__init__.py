from sqlalchemy.orm import declarative_base

BaseModel = declarative_base()

from src.models.author import Author
from src.models.search import Search
from src.models.session import UserSession
from src.models.user import User
