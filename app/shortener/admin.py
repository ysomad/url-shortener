from django.contrib import admin
from django.template.defaultfilters import truncatechars

from .models import URL


@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
	list_display = ('truncated_original_url', 'code', 'created_at')

	def truncated_original_url(self, url_object):
		"""Обрезает оригинальный URL до 50 символов,
		для лучшего отображения в админке, в случае если URL
		очень длинный"""
		return truncatechars(url_object.original_url, 50)
	
	truncated_original_url.short_description = URL._meta.fields[1].verbose_name

