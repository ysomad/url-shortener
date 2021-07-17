from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.http import HttpResponseRedirect

from shortener.models import URL


class URLFormViewTestCase(TestCase):
	def test_url_creation_without_code(self):
		data = {'original_url': 'https://valid-url.com'}
		resp = self.client.post(path=reverse('url_new'), data=data)
		url = URL.objects.get(original_url=data['original_url'])
		self.assertEqual(resp.status_code, HTTPStatus.FOUND)
		self.assertEqual(url.original_url, data['original_url'])
		self.assertIsInstance(resp, HttpResponseRedirect)
	
	def test_url_creation_with_code(self):
		data = {'original_url': 'https://valid-url.com', 'code': 'testCode'}
		resp = self.client.post(path=reverse('url_new'), data=data)
		url = URL.objects.get(code=data['code'])
		self.assertEqual(resp.status_code, HTTPStatus.FOUND)
		self.assertEqual(url.original_url, data['original_url'])
		self.assertEqual(url.code, data['code'])
		self.assertIsInstance(resp, HttpResponseRedirect)

	def test_url_creation_with_url_without_prefix(self):
		no_prefix_url = 'invalid.url'
		data = {'original_url':  no_prefix_url, 'code': 'testCode'}
		resp = self.client.post(path=reverse('url_new'), data=data)
		url = URL.objects.get(code=data['code'])
		self.assertEqual(resp.status_code, HTTPStatus.FOUND)
		self.assertEqual(url.original_url, f'http://{no_prefix_url}')
		self.assertIsInstance(resp, HttpResponseRedirect)

