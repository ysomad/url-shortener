from loguru import logger

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response

from .serializers import URLSerializer

from shortener.models import URL


class URLListCreateViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
	queryset = URL.objects.all()
	serializer_class = URLSerializer

	# def create(self, request):
	# 	"""Перезаписанный метод create из 
	# 	rest_framework.mixins.CreateModelMixin. 
	# 	После создания URL записи в БД, также добавляет маппинг в кэш"""
	# 	serializer = self.get_serializer(data=request.data)
	# 	serializer.is_valid(raise_exception=True)
	# 	self.perform_create(serializer)
	# 	add_url_mapping_to_cache(
	# 		serializer.data['code'], serializer.data['original_url']
	# 	)
	# 	headers = self.get_success_headers(serializer.data)
	# 	return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

