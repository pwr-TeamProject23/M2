from src.worker import celery


@celery.task(name='hello.world', bind=True)
def hello_world(self, name):
    print("Hello world")
