from django.urls import path

from .views import URLFormView, URLListView, URLRedirectView


urlpatterns = [
    path('', URLFormView.as_view(), name='url_new'),
    path('urls/', URLListView.as_view(), name='url_list'),
    path('<str:code>', URLRedirectView.as_view(), name='url_redirect'),
]
