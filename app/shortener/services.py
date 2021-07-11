from django.contrib import messages
from django.http import HttpRequest
from django.contrib.sessions.models import Session
from django.core.cache import cache

from loguru import logger

from config.settings import CELERY_TASK_TIME_LIMIT
from .forms import URLForm
from .models import URL


def build_shortened_url(request: HttpRequest, code: str) -> str:
    """Собирает укороченный URL на основе абсолютного пути до
    домашней страницы и идентификатора укороченного URL.code"""
    return request.build_absolute_uri('/') + code


def add_urls_in_user_session(
        session: Session, original_url: str, shortened_url: str) -> None:
    """Записывает в сессию оригинальный и укороченный URL"""
    if (not 'user_urls' in session or 
        not session['user_urls']):
        session['user_urls'] = list()

    user_urls = session['user_urls']
    user_urls.append({
        'original_url': original_url,
        'shortened_url': shortened_url,
    })
    session['user_urls'] = user_urls

    logger.info(
        f'Shortened URL {shortened_url} saved in session for {original_url}'
    )


def add_url_form_error_messages_to_message_storage(
        request: HttpRequest, form: URLForm) -> None:
    """Записывает ошибки валидации из формы URLForm в
    хранилище Django Messages"""
    for field, message in form.errors.get_json_data().items():
        cleaned_message = message[0]['message'] 
        logger.info((
            f'Validation error in field "{field}"'
            f'with message "{cleaned_message}"'
        ))
        messages.error(request, cleaned_message)


def delete_all_urls_from_database() -> None:
    """Удаляет все записи shortener.models.URL из базы данных"""
    URL.objects.all().delete()


def delete_all_urls_from_cache() -> None:
    """Удаляет все записи из кэша"""
    cache.clear()


def add_url_mapping_to_cache(url_code: str, original_url: str) -> None:
    """Добавляет ключ значение {"url_code": "original_url"} в кэш"""
    cache.set(url_code, original_url, timeout=CELERY_TASK_TIME_LIMIT)
    logger.info((
        f'{original_url} was successfully '
        f'saved in cache with code "{url_code}"'
    ))


def get_original_url_from_db(url_code: str) -> str:
    """Возвращает оригинальный URL из базы данных под коду"""
    return URL.objects.get(code=url_code).original_url


def get_original_url_from_cache(url_code: str) -> str:
    """Достает оригинальный URL из кэша, если он там есть, иначе
    райзит исключение ValueError"""
    original_url = cache.get(url_code)
    if original_url is None:
        logger.info(f'Original URL with code {url_code} not found in cache')
        raise ValueError
    
    logger.info(f'Found "{original_url}" with code "{url_code}" in cache')
    return original_url


