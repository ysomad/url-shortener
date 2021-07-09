from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from .serializers import URLSerializer

from shortener.models import URL


class URLListCreateViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
	queryset = URL.objects.all()
	serializer_class = URLSerializer

