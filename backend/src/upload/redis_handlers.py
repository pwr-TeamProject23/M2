from src.redis_handler import RedisHandler
from src.common.models import UploadStatus


class UploadStatusRedisHandler:
    def __init__(self, redis: RedisHandler):
        self.redis = redis

    def get_status(self, upload_id: int) -> str | None:
        status_key = f"status:{upload_id}"
        return self.redis.get(status_key)

    def set_status(
        self, upload_id: int, status: UploadStatus | str = UploadStatus.PENDING
    ) -> bool:
        status_key = f"status:{upload_id}"
        return self.redis.set(status_key, status)
