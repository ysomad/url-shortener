from django.test import TestCase
from django.core.cache import cache
from django.test.client import Client

from shortener import services as S
from shortener.forms import URL, URLForm


class ShortenerServiceTestCase(TestCase):

	def setUp(self):
		self.req = self.client.get('url_new').wsgi_request
		self.host = self.req.build_absolute_uri('/')

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
		session_key = self.request.session.session_key
		url_list = [
			{
				'original_url': 'http://orig-url.com',
				'shortened_url': 'http://localhost:8000/shU'
			},
			{
				'original_url': 'http://orig-url2.com',
				'shortened_url': 'http://localhost:8000/shU2'
			}
		]
		cache.set(session_key, url_list)
		url_list_from_cache = S.get_url_list_from_cache(session_key)
		self.assertIsNotNone(url_list_from_cache)
		self.assertIsInstance(url_list_from_cache, list)
		self.assertEqual(url_list_from_cache, url_list)

	def test_build_shortened_url(self):
		code = 'code'
		shortened_url = S.build_shortened_url(self.req, code)
		self.assertIsNotNone(shortened_url)
		self.assertEqual(self.host + code, shortened_url)
		self.assertIsInstance(shortened_url, str)

	def test_append_url_to_list_in_cache_from_cache(self):
		cli = Client()
		req = cli.get(self.host).wsgi_request
		session_key = req.session.session_key
		original_url = 'http://original-url.com'
		code = 'urlCode1337'
		shortened_url = self.host + code
		cache.set(session_key, [
			{'original_url': original_url, 'shortened_url': shortened_url}
		])
		S.append_url_to_list_in_cache(req, original_url, code)
		url_list_from_cache = cache.get(session_key)
		self.assertNotEqual(session_key, self.client.session.session_key)
		self.assertIsInstance(url_list_from_cache, list)
		self.assertEqual(url_list_from_cache[0]['original_url'], original_url)
		self.assertEqual(url_list_from_cache[0]['shortened_url'], shortened_url)

	def test_get_url_list_from_cache(self):
		cli = Client()
		req = cli.get(self.host).wsgi_request
		session_key = req.session.session_key
		original_url = 'http://original-url-from-cache.com'
		code = 'urlCode1337cache'
		shortened_url = self.host + code
		url_dict = {'original_url': original_url, 'shortened_url': shortened_url}
		cache.set(session_key, [url_dict])
		url_list_from_cache = S.get_url_list_from_cache(session_key)
		self.assertNotEqual(session_key, self.client.session.session_key)
		self.assertIsInstance(url_list_from_cache, list)
		self.assertEqual(url_list_from_cache[0]['original_url'], original_url)
		self.assertEqual(url_list_from_cache[0]['shortened_url'], shortened_url)

	def test_get_url_list_from_cache_empty_list_in_cache(self):
		cli = Client()
		req = cli.get(self.host).wsgi_request
		session_key = req.session.session_key
		cache.delete(session_key)
		self.assertNotEqual(session_key, self.client.session.session_key)
		self.assertRaises(
			ValueError, S.get_url_list_from_cache, session_key=session_key
		)

	def test_build_shortened_urls_in_url_list(self):
		url_list = [
			('http://orig-url.com', 'code1'),
			('http://orig-url2.com', 'code2')
		]
		url_list_with_shortened_urls = S.build_shortened_urls_in_url_list(
			self.req, url_list)
		self.assertIsInstance(url_list_with_shortened_urls, list)
		self.assertEqual(
			url_list_with_shortened_urls[0]['original_url'], 
			url_list[0][0]
		)
		self.assertEqual(
			url_list_with_shortened_urls[1]['original_url'], 
			url_list[1][0]
		)
		self.assertEqual(
			url_list_with_shortened_urls[0]['shortened_url'],
			self.host + url_list[0][1]
		)
		self.assertEqual(
			url_list_with_shortened_urls[1]['shortened_url'],
			self.host + url_list[1][1]
		)

	def test_build_shortened_urls_in_url_list_raising_typeerror(self):
		invalid_url_list = [[], [], []]
		self.assertRaises(
			TypeError, 
			S.build_shortened_urls_in_url_list,
			request=self.req,
			urls=invalid_url_list
		)

	def test_save_url_list_to_cache(self):
		cli = Client()
		req = cli.get(self.host).wsgi_request
		session_key = req.session.session_key
		url_list = [
			{
				'original_url': 'http://orig-url.com',
				'shortened_url': 'http://localhost:8000/shU'
			},
			{
				'original_url': 'http://orig-url2.com',
				'shortened_url': 'http://localhost:8000/shU2'
			}
		]
		S.save_url_list_to_cache(session_key, url_list)
		url_list_from_cache = cache.get(session_key)
		self.assertNotEqual(session_key, self.client.session.session_key)
		self.assertIsInstance(url_list_from_cache, list)
		self.assertEqual(
			url_list_from_cache[0]['original_url'], 
			url_list[0]['original_url']
		)
		self.assertEqual(
			url_list_from_cache[1]['original_url'], 
			url_list[1]['original_url']
		)
		self.assertEqual(
			url_list_from_cache[0]['shortened_url'], 
			url_list[0]['shortened_url']
		)
		self.assertEqual(
			url_list_from_cache[1]['shortened_url'], 
			url_list[1]['shortened_url']
		)

	def test_save_url_list_to_cache_raising_valueerror(self):
		self.assertRaises(
			ValueError,
			S.save_url_list_to_cache,
			session_key='dummy_session_key',
			urls=[]
		)




	






