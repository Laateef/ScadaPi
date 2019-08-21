from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from django.test import TestCase

import time

MAX_WAIT = 3

def wait(fn):
	def modified_fn(*args, **kargs):
		start_time = time.time()
		while True:
			try:
				return fn(*args, **kargs)
			except (AssertionError, WebDriverException) as e:
				if time.time() - start_time > MAX_WAIT:
					raise e
				time.sleep(0.5)
	return modified_fn

class MainPageTest(TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()
	
	def test_title_is_correct(self):
		self.browser.get('http://localhost:8000')

		self.assertIn('ScadaPi', self.browser.title)

	@wait
	def test_devices_are_shown_on_control_page(self):
		self.browser.get('http://localhost:8000')

		self.assertEqual(len(self.browser.find_elements_by_css_selector('.thermistor')), 8)
		self.assertEqual(len(self.browser.find_elements_by_css_selector('.valve')), 5)
		self.assertEqual(len(self.browser.find_elements_by_css_selector('.pump')), 3)
		self.assertEqual(len(self.browser.find_elements_by_css_selector('.heater')), 2)


