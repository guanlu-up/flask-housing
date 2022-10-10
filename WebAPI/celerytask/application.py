from celery import Celery

from . import config

celery_app = Celery("HomeApp")
celery_app.config_from_object(config)
celery_app.autodiscover_tasks(["WebAPI.celerytask.tasks"])
