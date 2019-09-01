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
	base_url = 'http://localhost:8000/'

	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()
	
	def test_title_is_correct(self):
		self.browser.get(self.base_url)

		self.assertIn('ScadaPi', self.browser.title)

	@wait
	def test_shows_one_tab_at_a_time(self):
		self.browser.get(self.base_url)

		control_tab_link_element = self.browser.find_element_by_css_selector('.tab-link[href="#control"]')
		monitor_tab_link_element = self.browser.find_element_by_css_selector('.tab-link[href="#monitor"]')
		about_tab_link_element = self.browser.find_element_by_css_selector('.tab-link[href="#about"]')

		control_tab_content_element = self.browser.find_element_by_css_selector('.tab-content#control')
		monitor_tab_content_element = self.browser.find_element_by_css_selector('.tab-content#monitor')
		about_tab_content_element = self.browser.find_element_by_css_selector('.tab-content#about')		

		self.assertTrue(control_tab_content_element.is_displayed())
		self.assertFalse(monitor_tab_content_element.is_displayed())
		self.assertFalse(about_tab_content_element.is_displayed())

		monitor_tab_link_element.click()
		
		self.assertFalse(control_tab_content_element.is_displayed())
		self.assertTrue(monitor_tab_content_element.is_displayed())
		self.assertFalse(about_tab_content_element.is_displayed())

		about_tab_link_element.click()

		self.assertFalse(control_tab_content_element.is_displayed())
		self.assertFalse(monitor_tab_content_element.is_displayed())
		self.assertTrue(about_tab_content_element.is_displayed())

		control_tab_link_element.click()

		self.assertTrue(control_tab_content_element.is_displayed())
		self.assertFalse(monitor_tab_content_element.is_displayed())
		self.assertFalse(about_tab_content_element.is_displayed())

	@wait
	def test_tabs_contain_relevant_elements(self):
		self.browser.get(self.base_url)
		
		# initially, the page shows the control tab.
		self.assertEqual(len(self.browser.find_elements_by_css_selector('.thermistor')), 8)
		self.assertEqual(len(self.browser.find_elements_by_css_selector('.valve')), 5)
		self.assertEqual(len(self.browser.find_elements_by_css_selector('.pump')), 3)
		self.assertEqual(len(self.browser.find_elements_by_css_selector('.heater')), 2)

		# switch to the monitor tab.
		monitor_tab_link_element = self.browser.find_element_by_css_selector('.tab-link[href="#monitor"]')
		monitor_tab_link_element.click()

		self.assertTrue(self.browser.find_element_by_id('temperature-chart').is_displayed())


