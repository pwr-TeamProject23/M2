from logging import getLogger

from redis.client import Redis
from redis.connection import ConnectionPool
from redis.exceptions import RedisError
from src.redis_handler.settings import RedisSettings

REDIS_SETTINGS = RedisSettings()

connection_pool = ConnectionPool(
    host=REDIS_SETTINGS.redis_host,
    port=REDIS_SETTINGS.redis_port,
    ssl=REDIS_SETTINGS.redis_ssl,
    db=REDIS_SETTINGS.redis_db,
    username=REDIS_SETTINGS.redis_username,
    password=REDIS_SETTINGS.redis_password,
)
redis = Redis(connection_pool=connection_pool)


class RedisHandler:
    def __init__(self, redis: Redis):
        self.logger = getLogger(__name__)
        self.redis = redis

    def get(self, key: str) -> str | None:
        try:
            return self.redis.get(key)
        except RedisError as err:
            self.logger.error(
                f"Could not get value from Redis at key={key}, details: {err}",
                exc_info=True,
            )
            raise

    def set(self, key: str, value: any) -> bool:
        try:
            return self.redis.set(key, value)
        except RedisError as err:
            self.logger.error(
                f"Could not set value in Redis at key={key}, details: {err}",
                exc_info=True,
            )
            raise

    def delete(self, names: list[str]) -> int:
        try:
            return self.redis.delete(names)
        except RedisError as err:
            self.logger.error(
                f"Could not delete {names} from Redis, details: {err}", exc_info=True
            )
            raise
