from celery import Celery
from .config import settings

celery_app = Celery(
    'wallet_service_v2',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["src.api.v1.tasks.wallet"]
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_backend=settings.REDIS_URL,
    timezone='UTC',
    broker_connection_retry_on_startup=True
)

