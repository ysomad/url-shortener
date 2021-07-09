from django.urls import path
from .views import home_view, shorten_url_view, redirect_view, url_list_view


urlpatterns = [
    path('', home_view, name='home'),
    path('<str:code>', redirect_view, name='redirect'),
    path('shorten/', shorten_url_view, name='url_shorten'),
    path('urls/', url_list_view, name='url_list'),
]
