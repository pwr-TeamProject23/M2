from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_password: str
    postgres_user: str
    postgres_db: str
    postgres_port: int
    postgres_uri: str
    admin_email: str
    admin_password: str
    
