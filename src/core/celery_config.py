from celery import Celery

celery_app = Celery(
    'wallet_service_v2',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=["src.api.v1.tasks.wallet"]
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_backend='redis://localhost:6379/0',
    timezone='UTC',
    broker_connection_retry_on_startup=True
)

