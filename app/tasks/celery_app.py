from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_process_init

from app.core.config import settings
from app.core.logging import setup_logging

celery_app = Celery(
    'delivery_app',
    broker=settings.REDIS_BROKER,
    include=['app.tasks.calculate_delivery_cost']
)

celery_app.conf.beat_schedule = {
    "calculate_delivery_cost": {
        "task": "app.tasks.calculate_delivery_cost.calculate_delivery_cost",
        "schedule": crontab(minute="*/5"),
    }
}

celery_app.conf.timezone = "UTC"

@worker_process_init.connect
def init_worker_logging(**kwargs) -> None:
    setup_logging()
