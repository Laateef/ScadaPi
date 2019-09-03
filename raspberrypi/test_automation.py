from unittest import TestCase
from unittest.mock import patch

from mainapp.models import Experiment, Temperature

from . import enums

import time
import datetime

from django.utils import timezone

with patch('raspberrypi.devices.Thermistor', autospec=True) as thermistorMock:
	temperature_list = [25.1, 26.2, 27.3, 28.4, 29.5, 30.6, 31.7, 32.8]
	thermistorMock.temperature_list.return_value = temperature_list

	with patch('raspberrypi.devices.Heater', autospec=True) as heaterMock:
		with patch('raspberrypi.devices.Pump', autospec=True) as pumpMock:
			with patch('raspberrypi.devices.Valve', autospec=True) as valveMock:
				from raspberrypi import automation

class AutomationTest(TestCase):

	def test_fetch_temperature_list(self):
		self.assertNotEqual(thermistorMock.temperature_list.call_count, 0)
		self.assertEqual(automation.temperature_list, temperature_list)

	def test_save_temperature_list_in_database_only_during_experiment(self):
		Temperature.objects.all().delete()

		self.assertEqual(Temperature.objects.all().count(), 0)

		automation.start()	
		
		time.sleep(enums.TEMPERATURE_REFRESH_INTERVAL + 0.1)

		self.assertEqual(Temperature.objects.all().count(), 1)
		self.assertTrue(timezone.now() - Temperature.objects.all().first().date < datetime.timedelta(milliseconds=1500))	
		
		automation.stop()	
		
		time.sleep(enums.TEMPERATURE_REFRESH_INTERVAL + 0.1)

		self.assertEqual(Temperature.objects.all().count(), 1)

	def test_experiment_start_and_end_date(self):
		automation.start()
		
		self.assertTrue(timezone.now() - automation.experiment.start_date < datetime.timedelta(milliseconds=500))	
		
		time.sleep(enums.TEMPERATURE_REFRESH_INTERVAL + 0.1)

		automation.stop()	
		
		self.assertTrue(timezone.now() - automation.experiment.end_date < datetime.timedelta(milliseconds=500))	
