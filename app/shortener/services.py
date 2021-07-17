from django.http import HttpRequest
from django.core.cache import cache

from loguru import logger

from config.settings import CACHE_TTL
from .forms import URLForm
from .models import URL


def save_url_form_to_db(session_key: str, form: URLForm) -> tuple[str]:
    """Сохраняет инстанс модели URL из формы URLForm в БД.
    Возвращает кортеж с оригинальным URL и его уникальным кодом"""
    original_url_received = form.data['original_url']
    try:
        url_code_received = form.data['code']
    except KeyError:
        url_code_received = ''

    logger.info((
        f'Received original URL "{original_url_received}" with code '
        f'"{url_code_received}", session "{session_key}" from {URLForm}'
    ))

    url_instance = form.save(commit=False)
    url_instance.session = session_key
    url_instance.save()

    return url_instance.original_url, url_instance.code
    

def build_shortened_url(request: HttpRequest, code: str) -> str:
    """Собирает укороченный URL на основе абсолютного пути до
    домашней страницы и идентификатора укороченного URL.code"""
    return request.build_absolute_uri('/') + code


def save_url_mapping_to_cache(url_code: str, original_url: str) -> None:
    """Добавляет оригинальный URL с ключом url_code в кэш"""
    cache.set(url_code, original_url, timeout=CACHE_TTL)
    logger.info(
        f'Original URL "{original_url}" with code "{url_code}" saved in cache')


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


