from django.test import SimpleTestCase
from django.urls import reverse, resolve

from shortener.views import URLFormView, URLListView, URLRedirectView


class RouteTest(SimpleTestCase):

	def test_url_new_is_resolved(self):
		url = reverse('url_new')
		self.assertEqual(resolve(url).func.view_class, URLFormView)

	def test_url_list_is_resolved(self):
		url = reverse('url_list')
		self.assertEqual(resolve(url).func.view_class, URLListView)

	def test_url_redirect_is_resolved(self):
		url = reverse('url_redirect', args=['urlRedirectResolve'])
		self.assertEqual(resolve(url).func.view_class, URLRedirectView)