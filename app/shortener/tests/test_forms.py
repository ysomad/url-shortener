from django.test import TestCase

from shortener.forms import URLForm


class URLFormTest(TestCase):
	
	def setUp(self):
		self.valid_url = 'http://valid-url.com'
		self.valid_code = 'validCode' # char <= 16 symbols
		self.invalid_url = 'invalidUrl,*com'
		self.invalid_code = 'UNIQUECODEMORETHAN16SYMBOLS'
	
	def test_urlform_valid_url_no_code(self):
		form = URLForm({'original_url': self.valid_url})
		self.assertTrue(form.is_valid())

	def test_urlform_valid_url_and_valid_code(self):
		form = URLForm({
			'original_url': self.valid_url,
			'code': self.valid_code
		})
		self.assertTrue(form.is_valid())

	def test_urlform_no_data(self):
		form = URLForm({})
		self.assertFalse(form.is_valid())
		self.assertEqual(len(form.errors), 1) # only 1 required field in URL model

	def test_urlform_invalid_url_no_code(self):
		form = URLForm({'original_url': self.invalid_url})
		self.assertFalse(form.is_valid())
		self.assertEqual(len(form.errors), 1)

	def test_urlform_valid_url_and_invalid_code(self):
		form = URLForm({
			'original_url': self.valid_url,
			'code': self.invalid_code
		})
		self.assertFalse(form.is_valid())
		self.assertEqual(len(form.errors), 1)

	def test_urlform_invalid_url_and_invalid_code(self):
		form = URLForm({
			'original_url': self.invalid_url,
			'code': self.invalid_code
		})
		self.assertFalse(form.is_valid())
		self.assertEqual(len(form.errors), 2)