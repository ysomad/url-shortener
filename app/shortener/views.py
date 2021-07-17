from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from django.views.generic import FormView, RedirectView, ListView 

from .forms import URLForm
from .services import (
    save_url_form_to_db, save_url_mapping_to_cache
)


class URLFormView(FormView):
    template_name = 'url_new.html'
    form_class = URLForm
    success_url = reverse_lazy('url_list')

    def form_valid(self, form: URLForm) -> HttpResponse:
        """Сохраняет инстанс модели URL из формы URLForm в БД и кэш,
        если форма провалидирована без ошибок"""
        url_code, original_url = save_url_form_to_db(
            self.request.session.session_key, form) 
        save_url_mapping_to_cache(url_code, original_url)
        return super().form_valid(form)


class URLListView(ListView):
    template_name = 'url_list.html'
    context_object_name = 'user_urls'

    # def get_queryset(self) -> QuerySet:
    #     return get_url_list_queryset_by_session_key(
    #         self.request.session.session_key)

    # def get_context_data(self):
    #     session_key = self.request.session.session_key

    #     # Если в кэше пусто, берет из БД

    #     url_list_queryset = self.get_queryset()

    #     # Сбилдить укороченный URL для всех урлов в queryset
    #     for url in url_list_queryset:
    #         url.shortened_url = build_shortened_url(self.request, url.code)

    #     add_url_list_queryset_to_cache(session_key, url_list_queryset)

    #     context_object_name = self.get_context_object_name(url_list_queryset)
    #     context = {
    #         'paginator': None,
    #         'page_obj': None,
    #         'is_paginated': False,
    #         'object_list': url_list_queryset
    #     }
    #     if context_object_name is not None:
    #         context[context_object_name] = url_list_queryset
    #     return super().get_context_data(**context)


class ShortenerView(RedirectView):
    pass


# @require_GET
# def url_list_view(request):
#     """Представление для отображения списка URLов 
#     текущей сессии пользователя"""
#     try:
#         context = {'user_urls': request.session['user_urls']}
#         return render(request, 'url_list.html', context=context)
#     except KeyError:
#         logger.info('No shortened URLs found in current user session')
#         return render(request, 'url_list.html')


# @require_POST
# def shorten_url_view(request):
#     """Представление процесса сокращения URLов"""
#     form = URLForm(request.POST)

#     if form.is_valid():
#         form.save()

#         original_url = form.cleaned_data['original_url']
#         url_code = form.cleaned_data['code']
#         shortened_url = build_shortened_url(request, url_code)

#         logger.info(
#             f'{original_url} was successfully saved with code "{url_code}"'
#         )

#         add_urls_in_user_session(request.session, original_url, shortened_url)
#         add_url_mapping_to_cache(url_code, original_url)
#         return redirect('url_list') 

#     add_url_form_error_messages_to_message_storage(request, form) 
#     return redirect('home')


# @require_GET
# def redirect_view(request, code):
#     """Редиректит на оригинальный URL из кэша, либо из БД, если в кэше
#     не найдено"""
#     try:
#         original_url_cached = get_original_url_from_cache(code)
#         logger.info((
#             f'Opening "{original_url_cached}" '
#             f'with code "{code}" from cache'
#         ))
#         return HttpResponseRedirect(original_url_cached)
#     except ValueError:
#         try:
#             original_url = get_original_url_from_db(code)
#             add_url_mapping_to_cache(code, original_url)
#             logger.info(f'Opening {original_url} with code "{code}" from db')
#             return HttpResponseRedirect(original_url)
#         except URL.DoesNotExist:
#             logger.info(f'URL with code "{code}" does not exist')
#             raise Http404 