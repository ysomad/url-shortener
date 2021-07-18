from typing import Any, Optional

from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from django.views.generic import FormView, RedirectView, ListView

from .forms import URLForm
from .services import (
    get_original_url_from_cache_or_db, save_url_instance_to_db, 
    save_url_mapping_to_cache, get_urls_from_db_by_session_key, 
    get_url_list_from_db_or_cache, get_or_create_session, 
    append_url_to_list_in_cache
)
from .decorators import ExceptionHandlerMixin


class URLFormView(FormView, ExceptionHandlerMixin):
    template_name = 'url_new.html'
    form_class = URLForm
    success_url = reverse_lazy('url_list')

    def form_valid(self, form: URLForm) -> HttpResponse:
        """Сохраняет инстанс модели URL из формы URLForm в БД и пару
        URL код, оригинальный URL в кэш"""
        session_key = get_or_create_session(self.request.session)
        original_url, url_code = save_url_instance_to_db(session_key, form) 
        save_url_mapping_to_cache(url_code, original_url)
        append_url_to_list_in_cache(self.request, original_url, url_code)
        return super().form_valid(form)


class URLListView(ListView, ExceptionHandlerMixin):
    template_name = 'url_list.html'

    def get_queryset(self) -> QuerySet:
        return get_urls_from_db_by_session_key(self.request.session.session_key)

    def get_context_data(self) -> dict[str, Any]:
        """Передает контекст со списком URLов в шаблон"""
        url_list = get_url_list_from_db_or_cache(self)
        return super().get_context_data(session_urls=url_list)


class URLRedirectView(RedirectView, ExceptionHandlerMixin):
    def get_redirect_url(self, code) -> Optional[str]:
        """Возвращает URL, на который будет перенаправлен пользователь"""
        return get_original_url_from_cache_or_db(code)
