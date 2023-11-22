import os

from celery import Celery

REDIS_SERVER = os.getenv("REDIS_SERVER", "redis://cache:6379")

celery = Celery("celery", backend=REDIS_SERVER, broker=REDIS_SERVER)
