import os
from celery import Celery

REDISSERVER = os.getenv("REDISSERVER", "redis://cache:6379")

celery = Celery("celery", backend=REDISSERVER, broker=REDISSERVER)
