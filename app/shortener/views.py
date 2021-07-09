from loguru import logger

from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.views.decorators.http import require_GET, require_POST

from .forms import URLForm
from .models import URL
from .services import (add_urls_in_user_session, build_shortened_url,
    add_url_form_error_messages_to_message_storage)


@require_GET
def home_view(request):
    """Представление домашней страницы"""
    return render(request, 'url_new.html', {'form': URLForm()})


@require_GET
def url_list_view(request):
    """Представление для отображения списка URLов 
    текущей сессии пользователя"""
    try:
        context = {'user_urls': request.session['user_urls']}
        return render(request, 'url_list.html', context=context)
    except KeyError:
        logger.info('No shortened URLs found in current user session')
        return render(request, 'url_list.html')


@require_POST
def shorten_url_view(request):
    """Представление процесса сокращения URLов"""
    form = URLForm(request.POST)

    if form.is_valid():
        form.save()

        original_url = form.cleaned_data['original_url']
        url_code = form.cleaned_data['code']
        shortened_url = build_shortened_url(request, url_code)

        logger.info(
            f'URL {original_url} was successfully saved with code {url_code}'
        )

        add_urls_in_user_session(request.session, original_url, shortened_url)
        return redirect('url_list') 

    add_url_form_error_messages_to_message_storage(request, form) 
    return redirect('home')


@require_GET
def redirect_view(request, code):
    """Представление редиректа по сокращенному URLу"""
    try:
        url = URL.objects.get(code=code)
        return HttpResponseRedirect(url.original_url)
    except URL.DoesNotExist:
        logger.info('URL with given unique code does not exist')
        raise Http404
