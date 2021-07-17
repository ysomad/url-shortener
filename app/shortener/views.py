from django.urls import reverse_lazy
from django.http.response import HttpResponse
from django.views.generic import FormView, RedirectView, ListView 

from .forms import URLForm
from .services import (
    save_url_form_to_db, save_url_mapping_to_cache, 
    get_urls_from_db_by_session_key, get_url_list_from_db_or_cache
)


class URLFormView(FormView):
    template_name = 'url_new.html'
    form_class = URLForm
    success_url = reverse_lazy('url_list')

    def form_valid(self, form: URLForm) -> HttpResponse:
        """Сохраняет инстанс модели URL из формы URLForm в БД и пару
        URL код, оригинальный URL в кэш"""
        original_url, url_code = save_url_form_to_db(
            self.request.session.session_key, form) 
        save_url_mapping_to_cache(url_code, original_url)
        return super().form_valid(form)


class URLListView(ListView):
    template_name = 'url_list.html'

    def get_queryset(self):
        return get_urls_from_db_by_session_key(self.request.session.session_key)

    def get_context_data(self):
        """Передает контекст со списком URLов в шаблон"""
        url_list = get_url_list_from_db_or_cache(self) 
        return super().get_context_data(session_urls=url_list)


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