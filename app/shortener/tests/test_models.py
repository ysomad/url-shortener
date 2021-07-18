from django.test import TestCase

from shortener.models import URL


class ModelTest(TestCase):

	def setUp(self):
		self.no_code_url = URL.objects.create(
			original_url='http://no-code-url.com'
		)
		self.code_url = URL.objects.create(
			original_url='http://code-url.com', 
			code='codeUrl'
		)

	def test_url_is_assigned_code_creation(self):
		url_from_db = URL.objects.get(original_url='http://no-code-url.com')
		self.assertEqual(self.no_code_url.code, url_from_db.code)

	def test_url_is_assigned(self):
		self.assertEqual(self.code_url.original_url, 'http://code-url.com')
		self.assertEqual(self.code_url.code, 'codeUrl')