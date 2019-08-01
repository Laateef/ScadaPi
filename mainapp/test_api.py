from django.test import TestCase
from django.urls import resolve
from unittest.mock import patch
from unittest import mock
import json
import mainapp

@patch('mainapp.api.devices.Thermistor', autospec=True)
class ThermistorApiTest(TestCase):
	base_url = '/api/thermistor/'
	def test_get_returns_json_200(self, m):
		response = self.client.get(self.base_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['content-type'], 'application/json')

	def test_get_returns_thermistor_temperature_array(self, thermistorMock):
		thermistorMock.temperatureArray.return_value = [25.1, 26.2, 27.3, 28.4, 29.5, 30.6, 31.7, 32.8]

		response = self.client.get(self.base_url)

		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'temperature': 25.1},
										{'id': 2, 'temperature': 26.2},
										{'id': 3, 'temperature': 27.3},
										{'id': 4, 'temperature': 28.4},
										{'id': 5, 'temperature': 29.5},
										{'id': 6, 'temperature': 30.6},
										{'id': 7, 'temperature': 31.7}, 
										{'id': 8, 'temperature': 32.8} ])

	def test_get_returns_thermistor_temperature_for_specific_channel(self, thermistorMock):
		thermistorMock.temperature.return_value = 37.5

		response = self.client.get(self.base_url + '1/')

		thermistorMock.temperature.assert_called_once_with(1)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'temperature': 37.5} ])

		thermistorMock.reset_mock()

		thermistorMock.temperature.return_value = 16.7

		response = self.client.get(self.base_url + '8/')

		thermistorMock.temperature.assert_called_once_with(8)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'temperature': 16.7} ])
