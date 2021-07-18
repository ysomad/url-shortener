from http import HTTPStatus

from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.http import HttpResponseRedirect

from shortener.models import URL
from shortener.services import append_url_to_list_in_cache


class TestView(TestCase):

	def setUp(self):
		self.url_new = reverse('url_new')
		self.url_list = reverse('url_list')
		self.test_urls = [
			'http://original-url1.com', 
			'http://original-url2.com', 
			'http://original-url3.com'
		]

	def test_url_creation_without_code(self):
		data = {'original_url': 'https://valid-url-without-code.com'}
		resp = self.client.post(self.url_new, data)
		url = URL.objects.get(original_url=data['original_url'])
		self.assertEqual(resp.status_code, HTTPStatus.FOUND)
		self.assertEqual(url.original_url, data['original_url'])
		self.assertIsInstance(resp, HttpResponseRedirect)
		self.assertRedirects(resp, self.url_list)
	
	def test_url_creation_with_code(self):
		data = {'original_url': 'https://valid-url.com', 'code': 'testCode'}
		resp = self.client.post(self.url_new, data)
		url = URL.objects.get(code=data['code'])
		self.assertEqual(resp.status_code, HTTPStatus.FOUND)
		self.assertEqual(url.original_url, data['original_url'])
		self.assertEqual(url.code, data['code'])
		self.assertIsInstance(resp, HttpResponseRedirect)
		self.assertRedirects(resp, self.url_list)

	def test_url_creation_with_url_without_prefix(self):
		no_prefix_url = 'no-prefix.url'
		data = {'original_url':  no_prefix_url, 'code': 'testCode'}
		resp = self.client.post(self.url_new, data)
		url = URL.objects.get(code=data['code'])
		self.assertEqual(resp.status_code, HTTPStatus.FOUND)
		self.assertEqual(url.original_url, f'http://{no_prefix_url}')
		self.assertIsInstance(resp, HttpResponseRedirect)
		self.assertRedirects(resp, self.url_list)

	def test_no_urls_in_db_and_cache(self):
		resp = self.client.get(self.url_list)
		self.assertEqual(resp.status_code, HTTPStatus.OK)
		self.assertTemplateUsed(resp, 'url_list.html')
		self.assertQuerysetEqual(resp.context['session_urls'], [])

	def test_with_urls_in_cache(self):
		cli = Client()
		session = cli.session
		session.create()
		session_key = cli.session.session_key
		req = cli.get(self.url_new).wsgi_request

		append_url_to_list_in_cache(req, self.test_urls[0], 'testViewCode1') 
		append_url_to_list_in_cache(req, self.test_urls[1], 'testViewCode3')
		append_url_to_list_in_cache(req, self.test_urls[2], 'testViewCode3')

		resp = cli.get(self.url_list)

		self.assertEqual(resp.status_code, HTTPStatus.OK)
		self.assertTemplateUsed(resp, 'url_list.html')
		self.assertContains(resp, self.test_urls[0])
		self.assertContains(resp, self.test_urls[1])
		self.assertContains(resp, self.test_urls[2])
		self.assertEqual(resp.wsgi_request.session.session_key, session_key) 

	def test_with_urls_in_db(self):
		cli = Client()
		session = cli.session
		session.create()
		session_key = cli.session.session_key

		URL.objects.create(original_url=self.test_urls[0], session=session_key)
		URL.objects.create(original_url=self.test_urls[1], session=session_key)
		URL.objects.create(original_url=self.test_urls[2], session=session_key)

		resp = cli.get(self.url_list)

		self.assertEqual(resp.status_code, HTTPStatus.OK)
		self.assertTemplateUsed(resp, 'url_list.html')
		self.assertContains(resp, self.test_urls[0])
		self.assertContains(resp, self.test_urls[1])
		self.assertContains(resp, self.test_urls[2])
		self.assertEqual(resp.wsgi_request.session.session_key, session_key)

