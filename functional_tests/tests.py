from selenium import webdriver
from django.test import TestCase

class MainPageTest(TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()
	
	def test_title_is_correct(self):
		self.browser.get('http://localhost:8000')
		self.assertIn('ScadaPi', self.browser.title)
		
