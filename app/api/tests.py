from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status


class URLTestCase(APITestCase):
	def setUp(self):
		self.path = '/api/'
		self.valid_original_url = 'http://valid-or-url.com'
		self.valid_code = 'validCode'
		self.invalid_original_url = 'in@liv.,2'
		self.invalid_code = 'CODEMORETHATSIXTEENCHARACTERS'

	def test_url_creation_without_code(self):
		data = {'original_url': self.valid_original_url}
		resp = self.client.post(self.path, data=data)
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertEqual(resp.data['original_url'], self.valid_original_url)

	def test_url_creation_with_code(self):
		data = {'original_url': self.valid_original_url, 'code': self.valid_code}
		resp = self.client.post(self.path, data=data)
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		self.assertEqual(resp.data['original_url'], self.valid_original_url)
		self.assertEqual(resp.data['code'], self.valid_code)
		self.assertEqual(resp.data['shortened_url'], resp.wsgi_request.build_absolute_uri('/') + self.valid_code)

	def test_url_creation_invalid_original_url_no_code(self):
		data = {'original_url': self.invalid_original_url}
		resp = self.client.post(self.path, data=data)
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(len(resp.data), 1)
		self.assertEqual(resp.data['original_url'][0], 'Enter a valid URL.')

	def test_url_creation_invalid_code(self):
		data = {'original_url': self.valid_original_url, 'code': self.invalid_code}
		resp = self.client.post(self.path, data=data)
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(len(resp.data), 1)
		self.assertEqual(resp.data['code'][0], 'Ensure this field has no more than 16 characters.')

	def test_url_creation_no_data(self):
		resp = self.client.post(self.path, data={})
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
		self.assertEqual(len(resp.data), 1)
		self.assertEqual(resp.data['original_url'][0], 'This field is required.')

