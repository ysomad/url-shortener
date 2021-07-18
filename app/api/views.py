from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response

from .serializers import URLSerializer
from .services import save_url_serializer

from shortener.services import (get_urls_from_db_by_session_key, 
	save_url_mapping_to_cache, append_url_to_list_in_cache)



class URLListCreateViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
	serializer_class = URLSerializer

	def get_queryset(self) -> QuerySet:
		return get_urls_from_db_by_session_key(self.request.session.session_key)

	def create(self, request: HttpRequest) -> HttpResponse:
		"""Сохраняет URL инстанс в БД и кэш"""
		serializer = save_url_serializer(request.session.session_key, 
			self.get_serializer(data=request.data))

		original_url = serializer.data['original_url']
		url_code = serializer.data['code']

		save_url_mapping_to_cache(url_code, original_url)
		append_url_to_list_in_cache(request, original_url, url_code)

		headers = self.get_success_headers(serializer.data)
		return Response(
			serializer.data, status=status.HTTP_201_CREATED, headers=headers)