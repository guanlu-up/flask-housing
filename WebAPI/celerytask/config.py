from ..config import LOCALHOST


BROKER_URL = f"redis://{LOCALHOST}:6379/1"
CELERY_RESULT_BACKEND = f"redis://{LOCALHOST}:6379/2"
