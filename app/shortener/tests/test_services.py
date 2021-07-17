from django.test import TestCase
from django.core.cache import cache

from django.urls import reverse

from shortener import services as S
from shortener.forms import URL, URLForm


class ShortenerServiceTestCase(TestCase):
	def test_save_url_form_to_db_service_without_url_code(self):
		data = {'original_url': 'http://test-url.com'}
		form = URLForm(data)
		original_url, url_code = S.save_url_instance_to_db(None, form)
		url = URL.objects.get(code=url_code)
		self.assertEqual(data['original_url'], url.original_url)
		self.assertEqual(original_url, url.original_url)
		self.assertEqual(url_code, url.code)

	def test_save_url_instance_to_db_service_with_url_code(self):
		data = {'original_url': 'http://test-url.com', 'code': 'serviceTest'}
		form = URLForm(data)
		original_url, url_code = S.save_url_instance_to_db(None, form)
		url = URL.objects.get(code=url_code)
		self.assertEqual(data['original_url'], url.original_url)
		self.assertEqual(original_url, url.original_url)
		self.assertEqual(url_code, url.code)

	def test_save_url_mapping_to_cache(self):
		code = 'cacheCode'
		original_url = 'https://test.com'
		S.save_url_mapping_to_cache(code, original_url)
		cached_original_url = cache.get(code)
		self.assertEqual(original_url, cached_original_url)	
		cache.delete(code)

	def test_save_url_instance_to_db_without_code(self):
		session_key = self.client.session.session_key
		data = {'original_url': 'http://save-url-instance-to-db.test'}
		form = URLForm(data)
		original_url, url_code = S.save_url_instance_to_db(session_key, form)
		url_from_db = URL.objects.get(code=url_code)
		self.assertEqual(data['original_url'], original_url)
		self.assertIsInstance(url_code, str)
		self.assertEqual(original_url, url_from_db.original_url)
		self.assertEqual(url_code, url_from_db.code)

	def test_save_url_instance_to_db_with_code(self):
		session_key = self.client.session.session_key
		data = {
			'original_url': 'http://save-url-instance-to-db.test', 
			'code': 'saveUrlInstance'
		}
		form = URLForm(data)
		original_url, url_code = S.save_url_instance_to_db(session_key, form)
		url_from_db = URL.objects.get(code=data['code'])
		self.assertEqual(data['original_url'], original_url)
		self.assertEqual(data['original_url'], url_from_db.original_url)
		self.assertEqual(original_url, url_from_db.original_url)
		self.assertIsInstance(url_code, str)
		self.assertEqual(url_code, url_from_db.code)
		self.assertEqual(data['code'], url_code)
		self.assertEqual(data['code'], url_from_db.code)

	def test_get_url_list_from_cache(self):
		pass

	def test_build_shortened_url(self):
		pass

	def test_append_url_to_list_in_cache_with_empty_list(self):
		pass

	def test_append_url_to_list_in_cache(self):
		pass

	def test_get_url_list_from_cache(self):
		pass

	def test_build_shortened_urls_in_url_list(self):
		pass

	def test_save_url_list_to_cache(self):
		pass

	def test_get_url_list_from_db_and_save_to_cache(self):
		pass

	def test_test_get_url_list_from_db_or_cache(self):
		pass



	






