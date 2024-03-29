from unittest import TestCase
from unittest.mock import patch
from unittest.mock import call

from raspberrypi import enums
from raspberrypi import devices

class ThermistorModuleTest(TestCase):

	def test_returns_thermistor_voltage_for_given_adc_value(self):
		self.assertAlmostEqual(devices.Thermistor.adc_to_voltage(-32768), -4.096)
		self.assertAlmostEqual(devices.Thermistor.adc_to_voltage(0), 0)
		self.assertAlmostEqual(devices.Thermistor.adc_to_voltage(32768), 4.096)

	def test_returns_thermistor_resistance_for_given_voltage(self):
		self.assertAlmostEqual(devices.Thermistor.voltage_to_resistance(1.65), 10000)
		self.assertAlmostEqual(devices.Thermistor.voltage_to_resistance(3), 1000)

	def test_voltage_to_resistance_throws_ValueError_if_voltage_is_zero(self):
		self.assertRaises(ValueError, devices.Thermistor.voltage_to_resistance, 0)

	def test_returns_thermistor_temperature_given_resistance(self):
		# NTC thermistor with B=3980 has resistance of 10000(ohm) at 25(c) 
		self.assertAlmostEqual(devices.Thermistor.resistance_to_temperature(10000), 25)

	def test_resistance_to_temperature_throws_ValueError_if_resistance_less_or_equals_zero(self):
		self.assertRaises(ValueError, devices.Thermistor.resistance_to_temperature, 0)
		self.assertRaises(ValueError, devices.Thermistor.resistance_to_temperature, -1)

	@patch('raspberrypi.devices.interfaces.ADC', autospec=True)
	def test_returns_thermistor_1_temperature(self, adcMock):
		adcMock.return_value.readChannel.return_value = 13200

		temperature_value = devices.Thermistor.temperature(1)

		self.assertAlmostEqual(temperature_value, 25)
		adcMock.assert_called_once()
		adcMock.return_value.readChannel.assert_called_once_with(0)

	@patch('raspberrypi.devices.interfaces.ADC', autospec=True)
	def test_temperature_catch_thrown_exceptions_and_returns_99_point_9(self, adcMock):
		adcMock.return_value.readChannel.return_value = 0

		self.assertAlmostEqual(devices.Thermistor.temperature(1), 999.9)

		adcMock.assert_called_once()
		adcMock.return_value.readChannel.assert_called_once_with(0)

	@patch('raspberrypi.devices.interfaces.ADC', autospec=True)
	def test_raises_exception_if_channel_no_is_out_of_scope(self, adcMock):
		self.assertRaises(IndexError, devices.Thermistor.temperature, 0)
		self.assertRaises(IndexError, devices.Thermistor.temperature, 9)

	@patch('raspberrypi.devices.interfaces.ADC', autospec=True)
	def test_returns_thermistor_temperature_array(self, adcMock):
		adcMock.return_value.readChannel.side_effect = iter([10798, 11100, 12306, 13200, 17522, 23627, 24665, 16350])

		temperature_array = devices.Thermistor.temperature_list()
		expected_array = [17, 18, 22, 25, 41, 82, 99, 36.3]
		for i in range (0, enums.TOTAL_CHANNEL_COUNT):
			self.assertAlmostEqual(temperature_array[i], expected_array[i], delta = 0.01)

		adcMock.assert_called_once()		
		self.assertEqual(adcMock.return_value.readChannel.call_count, enums.TOTAL_CHANNEL_COUNT)
		self.assertEqual(adcMock.return_value.readChannel.call_args_list, [call(0), call(1), call(2), call(3), call(4), call(5), call(6), call(7)])
	

@patch('raspberrypi.devices.interfaces.gpiozero.OutputDevice', autospec=True)
class HeaterModuleTest(TestCase):

	def test_starts_heater(self, deviceMock):
		devices.Heater(1).on()

		deviceMock.assert_called_once_with(enums.HEATER_PIN_MAP[1], False)
		deviceMock.return_value.on.assert_called_once()

	def test_stops_heater(self, deviceMock):
		devices.Heater(2).off()

		deviceMock.assert_called_once_with(enums.HEATER_PIN_MAP[2], False)
		deviceMock.return_value.off.assert_called_once()

	def test_returns_heater_state(self, deviceMock):
		deviceMock.return_value.value = False

		self.assertEqual(devices.Heater(1).state(), False)
		deviceMock.assert_called_once_with(enums.HEATER_PIN_MAP[1], False)

		deviceMock.reset_mock()

		deviceMock.return_value.value = True
		self.assertEqual(devices.Heater(2).state(), True)
		deviceMock.assert_called_once_with(enums.HEATER_PIN_MAP[2], False)

	def test_toggles_heater(self, deviceMock):
		deviceMock.return_value.value = False
		self.assertEqual(devices.Heater(2).state(), False)

		devices.Heater(2).toggle()

		deviceMock.return_value.value = True
		self.assertEqual(devices.Heater(2).state(), True)
		deviceMock.return_value.toggle.assert_called_once()

	def test_raises_exception_if_device_no_is_out_of_scope(self, deviceMock):
		self.assertRaises(IndexError, devices.Heater, 0)
		self.assertRaises(IndexError, devices.Heater, 3)

@patch('raspberrypi.devices.interfaces.gpiozero.OutputDevice', autospec=True)
class ValveModuleTest(TestCase):
	def test_turns_valve_1_on(self, deviceMock):
		devices.Valve(1).on()

		deviceMock.assert_called_once_with(enums.VALVE_PIN_MAP[1], False)
		deviceMock.return_value.on.assert_called_once()

	def test_raises_exception_if_valve_no_is_out_of_scope(self, deviceMock):
		self.assertRaises(IndexError, devices.Valve, 0)
		self.assertRaises(IndexError, devices.Valve, 6)
	
@patch('raspberrypi.devices.interfaces.gpiozero.OutputDevice', autospec=True)
class PumpModuleTest(TestCase):
	def test_turns_Pump_1_on(self, deviceMock):
		devices.Pump(1).on()

		deviceMock.assert_called_once_with(enums.PUMP_PIN_MAP[1], False)
		deviceMock.return_value.on.assert_called_once()

	def test_raises_exception_if_valve_no_is_out_of_scope(self, deviceMock):
		self.assertRaises(IndexError, devices.Pump, 0)
		self.assertRaises(IndexError, devices.Pump, 4)
