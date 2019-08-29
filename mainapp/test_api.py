from django.test import TestCase

from raspberrypi import devices

from . import util

from unittest.mock import patch, call, Mock

import json


heaterMockList=[Mock(devices.Heater), Mock(devices.Heater)]

pumpMockList=[Mock(devices.Pump), Mock(devices.Pump), Mock(devices.Pump)]

valveMockList=[Mock(devices.Valve), Mock(devices.Valve), Mock(devices.Valve), Mock(devices.Valve), Mock(devices.Valve)]

with patch('raspberrypi.devices.Thermistor', autospec=True) as thermistorMock:
	thermistorMock.temperature_list.return_value = [25.1, 26.2, 27.3, 28.4, 29.5, 30.6, 31.7, 32.8]

	with patch('raspberrypi.devices.Heater', autospec=True, side_effect=heaterMockList) as heaterMock:
		with patch('raspberrypi.devices.Pump', autospec=True, side_effect=pumpMockList) as pumpMock:
			with patch('raspberrypi.devices.Valve', autospec=True, side_effect=valveMockList) as valveMock:
				from raspberrypi import automation


class ThermistorApiTest(TestCase):
	base_url = '/api/thermistor/'

	def test_get_returns_json_200(self):
		response = self.client.get(self.base_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['content-type'], 'application/json')

	def test_get_returns_thermistor_temperature_at_specific_channel(self):
		response = self.client.get(self.base_url + '1/')

		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'temperature': 25.1} ])

		response = self.client.get(self.base_url + '8/')

		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 8, 'temperature': 32.8} ])

	def test_get_returns_thermistor_temperature_array(self):
		response = self.client.get(self.base_url)

		self.assertEqual(json.loads(response.content.decode('utf8')), [ 
							{'id': 1, 'temperature': 25.1},
							{'id': 2, 'temperature': 26.2},
							{'id': 3, 'temperature': 27.3},
							{'id': 4, 'temperature': 28.4},
							{'id': 5, 'temperature': 29.5},
							{'id': 6, 'temperature': 30.6},
							{'id': 7, 'temperature': 31.7}, 
							{'id': 8, 'temperature': 32.8} 
						])


def reset_device_mock(device_type):
		[automation.device_map[device_type + '_' + str(idx+1)].reset_mock() for idx in range(util.device_count(device_type))]


class HeaterDeviceApiTest(TestCase):
	base_url = '/api/heater/'

	def setUp(self):
		reset_device_mock('heater')

	def test_init_heaters(self):
		self.assertEqual(heaterMockList[0], automation.device_map['heater_1'])
		self.assertEqual(heaterMockList[1], automation.device_map['heater_2'])
		self.assertEqual(heaterMock.call_args_list, [call(1), call(2)])

	def test_get_returns_json_200(self):
		response = self.client.get(self.base_url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['content-type'], 'application/json')

	def test_get_returns_state_of_specific_heater(self):
		heaterMockList[0].state.return_value = 1

		response = self.client.get(self.base_url + '1/')

		self.assertEqual(heaterMockList[0].state.call_count, 1)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'state': 1} ])

		heaterMockList[1].state.return_value = 0

		response = self.client.get(self.base_url + '2/')

		self.assertEqual(heaterMockList[1].state.call_count, 1)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 2, 'state': 0} ])

	def test_get_returns_heater_state_array(self):
		heaterMockList[0].state.return_value = 1
		heaterMockList[1].state.return_value = 0

		response = self.client.get(self.base_url)

		self.assertEqual(heaterMockList[0].state.call_count, 1)
		self.assertEqual(heaterMockList[1].state.call_count, 1)

		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'id': 1, 'state': 1}, {'id': 2, 'state': 0} ])

	def test_put_toggles_specific_heater(self):
		response = self.client.put(self.base_url + '1/toggle/')

		self.assertEqual(heaterMockList[0].toggle.call_count, 1)
		self.assertEqual(response.status_code, 200)

		response = self.client.put('/api/heater/2/toggle/')

		self.assertEqual(heaterMockList[1].toggle.call_count, 1)
		self.assertEqual(response.status_code, 200)

	def test_put_turns_specific_heater_on(self):
		response = self.client.put('/api/heater/1/on/')

		self.assertEqual(heaterMockList[0].on.call_count, 1)
		self.assertEqual(response.status_code, 200)

		response = self.client.put(self.base_url + '2/on/')

		self.assertEqual(heaterMockList[1].on.call_count, 1)
		self.assertEqual(response.status_code, 200)

	def test_put_turns_specific_heater_off(self):
		response = self.client.put(self.base_url + '1/off/')

		self.assertEqual(heaterMockList[0].off.call_count, 1)
		self.assertEqual(response.status_code, 200)

		response = self.client.put(self.base_url + '2/off/')

		self.assertEqual(heaterMockList[1].off.call_count, 1)
		self.assertEqual(response.status_code, 200)


class PumpDeviceApiTest(TestCase):
	def setUp(self):
		reset_device_mock('pump')

	def test_init_pumps(self):
		self.assertEqual(pumpMockList[0], automation.device_map['pump_1'])
		self.assertEqual(pumpMockList[1], automation.device_map['pump_2'])
		self.assertEqual(pumpMockList[2], automation.device_map['pump_3'])
		self.assertEqual(pumpMock.call_args_list, [call(1), call(2), call(3)])

	def test_get_returns_pump_state_array(self):
		pumpMockList[0].state.return_value = 1
		pumpMockList[1].state.return_value = 1
		pumpMockList[2].state.return_value = 0

		response = self.client.get('/api/pump/')

		self.assertEqual(pumpMockList[0].state.call_count, 1)
		self.assertEqual(pumpMockList[1].state.call_count, 1)
		self.assertEqual(pumpMockList[2].state.call_count, 1)
		self.assertEqual(json.loads(response.content.decode('utf8')), [ 
							{'id': 1, 'state': 1}, 
							{'id': 2, 'state': 1}, 
							{'id': 3, 'state': 0} 
						])


class ValveDeviceApiTest(TestCase):
	def setUp(self):
		reset_device_mock('valve')

	def test_init_valves(self):
		self.assertEqual(valveMockList[0], automation.device_map['valve_1'])
		self.assertEqual(valveMockList[1], automation.device_map['valve_2'])
		self.assertEqual(valveMockList[2], automation.device_map['valve_3'])
		self.assertEqual(valveMockList[3], automation.device_map['valve_4'])
		self.assertEqual(valveMockList[4], automation.device_map['valve_5'])
		self.assertEqual(valveMock.call_args_list, [call(1), call(2), call(3), call(4), call(5)])

	def test_get_returns_valve_state_array(self):
		valveMockList[0].state.return_value = 1
		valveMockList[1].state.return_value = 1
		valveMockList[2].state.return_value = 0
		valveMockList[3].state.return_value = 1
		valveMockList[4].state.return_value = 1

		response = self.client.get('/api/valve/')

		self.assertEqual(valveMockList[0].state.call_count, 1)
		self.assertEqual(valveMockList[1].state.call_count, 1)
		self.assertEqual(valveMockList[2].state.call_count, 1)
		self.assertEqual(valveMockList[3].state.call_count, 1)
		self.assertEqual(valveMockList[4].state.call_count, 1)

		self.assertEqual(json.loads(response.content.decode('utf8')), [
							{'id': 1, 'state': 1}, 
							{'id': 2, 'state': 1}, 
							{'id': 3, 'state': 0}, 
							{'id': 4, 'state': 1}, 
							{'id': 5, 'state': 1} 
						])


class AllDevicesApiTest(TestCase):
	def test_get_returns_all_devices_state_list_as_json_200(self):
		heaterMockList[0].state.return_value = 1
		heaterMockList[1].state.return_value = 0

		pumpMockList[0].state.return_value = 1
		pumpMockList[1].state.return_value = 1
		pumpMockList[2].state.return_value = 0

		valveMockList[0].state.return_value = 1
		valveMockList[1].state.return_value = 1
		valveMockList[2].state.return_value = 0
		valveMockList[3].state.return_value = 1
		valveMockList[4].state.return_value = 1

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


class AutomationApiTest(TestCase):
	def test_automation_is_off_initially(self):
		response = self.client.get('/api/automation/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['content-type'], 'application/json')
		self.assertEqual(json.loads(response.content.decode('utf8')), [ {'state': 0} ])

	def test_start_automation(self):
		response = self.client.put('/api/automation/start/')

		self.assertTrue(automation.running)

	def test_stop_automation(self):
		response = self.client.put('/api/automation/stop/')

		self.assertFalse(automation.running)

	@patch('raspberrypi.automation.stop', autospec=True)
	@patch('raspberrypi.automation.start', autospec=True)
	def test_toggle_automation(self, startFuncMock, stopFuncMock):
		automation.running = True
		response = self.client.put('/api/automation/toggle/')

		self.assertEqual(stopFuncMock.call_count, 1)
		
		automation.running = False
		response = self.client.put('/api/automation/toggle/')

		self.assertEqual(startFuncMock.call_count, 1)


