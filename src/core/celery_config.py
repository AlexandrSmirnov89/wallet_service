from celery import Celery

# Создайте экземпляр Celery и настройте его для использования Redis
celery_app = Celery(
    'wallet_service_v2',  # Имя вашего приложения
    broker='redis://localhost:6379/0',  # Указываем брокер сообщений (Redis)
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

