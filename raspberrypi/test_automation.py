from unittest import TestCase
from unittest.mock import patch
from unittest.mock import call

with patch('raspberrypi.devices.Thermistor', autospec=True) as thermistorMock:
	temperature_list = [25.1, 26.2, 27.3, 28.4, 29.5, 30.6, 31.7, 32.8]
	thermistorMock.temperature_list.return_value = temperature_list

	with patch('raspberrypi.devices.Heater', autospec=True) as heaterMock:
		with patch('raspberrypi.devices.Pump', autospec=True) as pumpMock:
			with patch('raspberrypi.devices.Valve', autospec=True) as valveMock:
				from raspberrypi import automation

class AutomationTest(TestCase):

	def test_fetch_temperature_list(self):
		self.assertEqual(thermistorMock.temperature_list.call_count, 1)
		self.assertEqual(automation.temperature_list, temperature_list)
