from django.urls import path

from shortener.models import URL

from .views import URLFormView, URLListView


urlpatterns = [
    path('', URLFormView.as_view(), name='url_new'),
    path('urls/', URLListView.as_view(), name='url_list'),
    # path('<str:code>', redirect_view, name='redirect'),
    # path('shorten/', shorten_url_view, name='url_shorten'),
]
