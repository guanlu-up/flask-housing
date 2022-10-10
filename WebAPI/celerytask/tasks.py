from .application import celery_app


@celery_app.task
def celery_testing():
    import time
    time.sleep(5)
    print("This is celery testing !!!")
