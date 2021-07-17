from django.test import TestCase
from django.core.cache import cache

from shortener.services import (save_url_instance_to_db, save_url_mapping_to_cache,
	)
from shortener.forms import URL, URLForm


class ShortenerServiceTestCase(TestCase):
	def test_save_url_form_to_db_service_without_url_code(self):
		data = {'original_url': 'http://test-url.com'}
		form = URLForm(data)
		original_url, url_code = save_url_instance_to_db(None, form)
		url = URL.objects.get(code=url_code)
		self.assertEqual(data['original_url'], url.original_url)
		self.assertEqual(original_url, url.original_url)
		self.assertEqual(url_code, url.code)

	def test_save_url_form_to_db_service_with_url_code(self):
		data = {'original_url': 'http://test-url.com', 'code': 'serviceTest'}
		form = URLForm(data)
		original_url, url_code = save_url_instance_to_db(None, form)
		url = URL.objects.get(code=url_code)
		self.assertEqual(data['original_url'], url.original_url)
		self.assertEqual(original_url, url.original_url)
		self.assertEqual(url_code, url.code)

	def test_save_url_mapping_to_cache(self):
		code = 'cacheCode'
		original_url = 'https://test.com'
		save_url_mapping_to_cache(code, original_url)
		cached_original_url = cache.get(code)
		self.assertEqual(original_url, cached_original_url)	




