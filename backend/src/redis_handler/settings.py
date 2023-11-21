from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    redis_host: str
    redis_port: int
    redis_ssl: bool
    redis_db: int
    redis_username: str
    redis_password: str
