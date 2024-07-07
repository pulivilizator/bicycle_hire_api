from celery import Celery
from .config import get_config

config = get_config()
app = Celery("bicycle_hire_api")
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()