FROM python:3.11-slim

WORKDIR /celery_worker

COPY ./requirement.txt /celery_worker/requirements.txt
RUN pip install -r /celery_worker/requirements.txt

COPY . /celery_worker/

CMD celery -A src.tasks worker
