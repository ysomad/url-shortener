from datetime import datetime, timedelta

from celery import shared_task
from loguru import logger

from shortener.models import URL
from config.settings import URL_STORE_LIMIT_DAYS


@shared_task
def delete_old_urls_from_db() -> None:
    """Удаляет все старые URLы из базы данных, 
    старее config.settings.URL_STORE_LIMIT_DAYS дней"""
    urls_to_delete = URL.objects.filter(
        created_at__lt=datetime.now() - timedelta(days=URL_STORE_LIMIT_DAYS)
    ).delete()
    logger.info((
        f'Deleted URLs older than {URL_STORE_LIMIT_DAYS} '
        f'days from database {urls_to_delete}'
    ))