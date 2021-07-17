from django.db.models.query import QuerySet

from django.http import HttpRequest
from django.core.cache import cache
from django.views.generic.list import ListView

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


def get_url_list_from_cache(session_key: str) -> list[str]:
    """Возвращает лист URLов из кэша по ключу session_key"""
    url_list = cache.get(session_key)
    if url_list is None:
        raise ValueError('Got empty URL list from cache')
    logger.info(f'Got session URL list from cache {url_list}')
    return url_list


def save_url_list_to_cache(session_key: str, urls: list) -> None:
    """Сохраняет URL массив в кэш с ключом session_key"""
    cache.set(session_key, urls, timeout=CACHE_TTL)
    logger.info(f'Added session URL list to cache {urls}')


def append_url_to_list_in_cache(
        session_key: str, original_url: str, shortened_url: str) -> None:
    """Добавляет укороченный и оригинальный URL в массив в кэше с
    ключом session_key"""
    urls = get_url_list_from_cache(session_key)
    urls.append({'original_url': original_url, 'shortened_url': shortened_url})
    save_url_list_to_cache(session_key, urls)


def build_shortened_url(request: HttpRequest, code: str) -> str:
    """Собирает укороченный URL на основе абсолютного пути до
    домашней страницы и идентификатора укороченного URL.code"""
    return request.build_absolute_uri('/') + code


def save_url_mapping_to_cache(url_code: str, original_url: str) -> None:
    """Сохраняет оригинальный URL с ключом url_code в кэше"""
    cache.set(url_code, original_url, timeout=CACHE_TTL)
    logger.info(
        f'Original URL "{original_url}" with code "{url_code}" saved in cache')


def get_original_url_from_db(url_code: str) -> str:
    """Возвращает оригинальный URL из базы данных под коду"""
    return URL.objects.get(code=url_code).original_url


def get_urls_from_db_by_session_key(session_key: str) -> QuerySet:
    """Возвращает QuerySet со списком URLов, принадлежащим сессии с
    ключом session_key"""
    return URL.objects.filter(session=session_key)


def get_original_url_from_cache(url_code: str) -> str:
    """Достает оригинальный URL из кэша, если он там есть, иначе
    райзит исключение ValueError"""
    original_url = cache.get(url_code)
    if original_url is None:
        logger.info(f'Original URL with code {url_code} not found in cache')
        raise ValueError
    
    logger.info(f'Found "{original_url}" with code "{url_code}" in cache')
    return original_url


def build_shortened_urls_in_url_list(request:HttpRequest, urls: list) -> list:
    """Получает лист с оригинальными URLами и их кодами.
    Возвращает лист словарей с оригинальными и укороченными URLами"""
    url_list_with_shortened_urls = list()

    for instance in urls:
        url_dict = {
            'original_url': instance[0],
            'shortened_url': build_shortened_url(request, instance[1])
        }
        url_list_with_shortened_urls.append(url_dict)
    
    logger.info(f'Generated URL list {url_list_with_shortened_urls}')
    return url_list_with_shortened_urls


def get_url_list_from_db_or_cache(url_list_view: ListView) -> list:
    """Возвращает список оригинальных и укороченных URLов из кэша
    или БД, записывает в кэш если в кэше пусто"""
    session_key = url_list_view.request.session.session_key
    try:
        url_list = get_url_list_from_cache(session_key)
    except ValueError:
        url_list_queryset = url_list_view.get_queryset()
        url_list = build_shortened_urls_in_url_list(
            url_list_view.request,
            list(url_list_queryset.values_list('original_url', 'code'))
        )
        save_url_list_to_cache(session_key, url_list)
    return url_list

