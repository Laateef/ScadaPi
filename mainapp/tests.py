from django.test import TestCase
from django.urls import resolve
from mainapp.views import main_page

class MainPageTest(TestCase):
	def test_root_url_resolves_to_main_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, main_page)
