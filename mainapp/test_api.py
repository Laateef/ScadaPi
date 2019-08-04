from django.test import TestCase

from unittest.mock import patch
from unittest.mock import call

import json

@patch('mainapp.api.devices.Thermistor', autospec=True)
class ThermistorApiTest(TestCase):
	base_url = '/api/thermistor/'
	def test_get_returns_json_200(self, thermistorMock):
		response = self.client.get(self.base_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['content-type'], 'application/json')

	def test_get_returns_thermistor_temperature_at_specific_channel(self, thermistorMock):
		thermistorMock.temperature.return_value = 37.5

		response = self.client.get(self.base_url + '1/')

		thermistorMock.temperature.assert_called_once_with(1)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'temperature': 37.5} ])

		thermistorMock.reset_mock()

		thermistorMock.temperature.return_value = 16.7

		response = self.client.get(self.base_url + '8/')

		thermistorMock.temperature.assert_called_once_with(8)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 8, 'temperature': 16.7} ])

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


@patch('mainapp.api.devices.Heater', autospec=True)
class HeaterDeviceApiTest(TestCase):
	base_url = '/api/heater/'
	def test_get_returns_json_200(self, deviceMock):
		response = self.client.get(self.base_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['content-type'], 'application/json')

	def test_get_returns_state_of_specific_heater(self, deviceMock):
		deviceMock.return_value.state.return_value = 1

		response = self.client.get(self.base_url + '1/')

		self.assertEqual(deviceMock.call_args_list, [call(1)])
		self.assertTrue(deviceMock.return_value.state.called)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'state': 1} ])

		deviceMock.reset_mock()

		deviceMock.return_value.state.return_value = 0

		response = self.client.get(self.base_url + '2/')

		self.assertEqual(deviceMock.call_args_list, [call(2)])
		self.assertTrue(deviceMock.return_value.state.called)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 2, 'state': 0} ])

	def test_get_returns_heater_state_array(self, deviceMock):
		deviceMock.return_value.state.side_effect = iter([1, 0])

		response = self.client.get(self.base_url)

		self.assertEqual(deviceMock.return_value.state.call_count, 2)
		self.assertEqual(deviceMock.call_count, 2)
		self.assertEqual(deviceMock.call_args_list, [call(1), call(2)])
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'state': 1}, {'id': 2, 'state': 0} ])

	def test_put_toggles_specific_heater(self, deviceMock):
		response = self.client.put(self.base_url + '1/toggle/')
		deviceMock.assert_called_once_with(1)
		self.assertTrue(deviceMock.return_value.toggle.called)
		self.assertEqual(deviceMock.return_value.toggle.call_count, 1)
		self.assertEqual(response.status_code, 200)

		deviceMock.reset_mock()

		response = self.client.put('/api/heater/2/toggle/')

		deviceMock.assert_called_once_with(2)
		self.assertTrue(deviceMock.return_value.toggle.called)
		self.assertEqual(deviceMock.return_value.toggle.call_count, 1)
		self.assertEqual(response.status_code, 200)

	def test_put_turns_specific_heater_on(self, deviceMock):
		response = self.client.put('/api/heater/1/on/')

		deviceMock.assert_called_once_with(1)
		self.assertTrue(deviceMock.return_value.on.called)
		self.assertEqual(deviceMock.return_value.on.call_count, 1)
		self.assertEqual(response.status_code, 200)

		deviceMock.reset_mock()

		response = self.client.put(self.base_url + '2/on/')

		deviceMock.assert_called_once_with(2)
		self.assertTrue(deviceMock.return_value.on.called)
		self.assertEqual(deviceMock.return_value.on.call_count, 1)
		self.assertEqual(response.status_code, 200)

	def test_put_turns_specific_heater_off(self, deviceMock):
		response = self.client.put(self.base_url + '1/off/')

		self.assertEqual(deviceMock.call_args_list, [call(1)])
		self.assertTrue(deviceMock.return_value.off.called)
		self.assertEqual(deviceMock.return_value.off.call_count, 1)
		self.assertEqual(response.status_code, 200)

		deviceMock.reset_mock()

		response = self.client.put(self.base_url + '2/off/')

		deviceMock.assert_called_once_with(2)
		self.assertTrue(deviceMock.return_value.off.called)
		self.assertEqual(deviceMock.return_value.off.call_count, 1)
		self.assertEqual(response.status_code, 200)


@patch('mainapp.api.devices.Valve', autospec=True)
class ValveDeviceApiTest(TestCase):

	def test_get_returns_valve_state_array(self, deviceMock):
		deviceMock.return_value.state.side_effect = iter([1, 1, 0, 1, 1])

		response = self.client.get('/api/valve/')

		self.assertEqual(deviceMock.return_value.state.call_count, 5)
		self.assertEqual(deviceMock.call_count, 5)
		self.assertEqual(deviceMock.call_args_list, [call(1), call(2), call(3), call(4), call(5)])
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'state': 1}, 
										{'id': 2, 'state': 1}, 
										{'id': 3, 'state': 0}, 
										{'id': 4, 'state': 1}, 
										{'id': 5, 'state': 1} ])

@patch('mainapp.api.devices.Pump', autospec=True)
class ValveDeviceApiTest(TestCase):

	def test_get_returns_pump_state_array(self, deviceMock):
		deviceMock.return_value.state.side_effect = iter([1, 1, 0])

		response = self.client.get('/api/pump/')

		self.assertEqual(deviceMock.return_value.state.call_count, 3)
		self.assertEqual(deviceMock.call_count, 3)
		self.assertEqual(deviceMock.call_args_list, [call(1), call(2), call(3)])
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'state': 1}, 
										{'id': 2, 'state': 1}, 
										{'id': 3, 'state': 0} ])

@patch('mainapp.api.devices.Thermistor', autospec=True)
@patch('mainapp.api.devices.Heater', autospec=True)
@patch('mainapp.api.devices.Valve', autospec=True)
@patch('mainapp.api.devices.Pump', autospec=True)
class AllDevicesApiTest(TestCase):
	
	def test_get_returns_all_devices_state_list_as_json_200(self, pumpMock, valveMock, heaterMock, thermistorMock):
		thermistorMock.temperatureArray.return_value = [25.1, 26.2, 27.3, 28.4, 29.5, 30.6, 31.7, 32.8]
		heaterMock.return_value.state.side_effect = iter([1, 0])
		valveMock.return_value.state.side_effect = iter([1, 1, 0, 1, 1])
		pumpMock.return_value.state.side_effect = iter([1, 1, 0])

		response = self.client.get('/api/')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['content-type'], 'application/json')
		self.assertEqual(json.loads(response.content.decode('utf8')), [
			{ 'thermistor': [ 
				{'id': 1, 'temperature': 25.1},
				{'id': 2, 'temperature': 26.2},
				{'id': 3, 'temperature': 27.3},
				{'id': 4, 'temperature': 28.4},
				{'id': 5, 'temperature': 29.5},
				{'id': 6, 'temperature': 30.6},
				{'id': 7, 'temperature': 31.7},  
				{'id': 8, 'temperature': 32.8} ] },
			{ 'heater': [ 
				{'id': 1, 'state': 1}, 
				{'id': 2, 'state': 0} ] },
			{ 'valve': [ 
				{'id': 1, 'state': 1}, 
				{'id': 2, 'state': 1}, 
				{'id': 3, 'state': 0}, 
				{'id': 4, 'state': 1}, 
				{'id': 5, 'state': 1} ] },
			{ 'pump': [ 
				{'id': 1, 'state': 1}, 
				{'id': 2, 'state': 1}, 
				{'id': 3, 'state': 0} ] }
		])


