from unittest import TestCase
from unittest.mock import patch
from unittest.mock import call

from raspberrypi import enums
from raspberrypi import interfaces
from raspberrypi import devices

class ThermistorModuleTest(TestCase):

	def test_returns_thermistor_voltage_for_given_adc_value(self):
		self.assertAlmostEqual(devices.Thermistor.adc_to_voltage(-32768), -4.096)
		self.assertAlmostEqual(devices.Thermistor.adc_to_voltage(0), 0)
		self.assertAlmostEqual(devices.Thermistor.adc_to_voltage(32768), 4.096)

	def test_returns_thermistor_resistance_for_given_voltage(self):
		self.assertAlmostEqual(devices.Thermistor.voltage_to_resistance(1.65), 10000)
		self.assertAlmostEqual(devices.Thermistor.voltage_to_resistance(3), 1000)

	def test_returns_thermistor_temperature_given_resistance(self):
		# NTC thermistor with B=3980 has resistance of 10000(ohm) at 25(c) 
		self.assertAlmostEqual(devices.Thermistor.resistance_to_temperature(10000), 25)

	@patch('raspberrypi.devices.interfaces.ADC', autospec=True)
	def test_returns_thermistor_temperature_for_channel_0(self, adcMock):
		adcMock.readChannel.return_value = 16384

		temperature_value = devices.Thermistor.temperature(0)

		self.assertAlmostEqual(temperature_value, 25)
		adcMock.assert_called_once()
		adcMock.return_value.readChannel.assert_called_once_with(0)

	@patch('raspberrypi.devices.interfaces.ADC', autospec=True)
	def test_returns_thermistor_temperature_array_for_all_channels(self, adcMock):
		adcMock.return_value.readChannel.side_effect = iter([10798, 11100, 12306, 13200, 17522, 23627, 24665, 16350])

		temperature_array = devices.Thermistor.temperatureArray()
		expected_array = [17, 18, 22, 25, 41, 82, 99, 36.28]
		for i in range (0, enums.TOTAL_CHANNEL_COUNT):
			self.assertAlmostEqual(temperature_array[i], expected_array[i], delta = 0.01)

		adcMock.assert_called_once()		
		self.assertEqual(adcMock.return_value.readChannel.call_count, enums.TOTAL_CHANNEL_COUNT)
		self.assertEqual(adcMock.return_value.readChannel.call_args_list, [call(0), call(1), call(2), call(3), call(4), call(5), call(6), call(7)])
	
@patch('raspberrypi.devices.interfaces.DO', autospec=True)
class HeaterModuleTest(TestCase):
	
	def test_starts_heater(self, gpioMock):
		devices.Heater.start()

		self.assertEqual(gpioMock.off.call_args_list, [call(enums.HEATER_PIN_1), call(enums.HEATER_PIN_2)])
		self.assertEqual(gpioMock.off.call_count, 2)

	def test_stops_heater(self, gpioMock):
		devices.Heater.stop()

		self.assertEqual(gpioMock.on.call_args_list, [call(enums.HEATER_PIN_1), call(enums.HEATER_PIN_2)])
		self.assertEqual(gpioMock.on.call_count, 2)


@patch('raspberrypi.devices.interfaces.DO', autospec=True)
class ValveModuleTest(TestCase):
	
	def test_opens_valve_1(self, gpioMock):
		devices.Valve.open(1)

		gpioMock.off.assert_called_once_with(enums.VALVE_PIN_MAP[1])

	def test_opens_valve_5(self, gpioMock):
		devices.Valve.open(5)

		gpioMock.off.assert_called_once_with(enums.VALVE_PIN_MAP[5])

	def test_closes_valve_1(self, gpioMock):
		devices.Valve.close(1)

		gpioMock.on.assert_called_once_with(enums.VALVE_PIN_MAP[1])

	def test_closes_valve_5(self, gpioMock):
		devices.Valve.close(5)

		gpioMock.on.assert_called_once_with(enums.VALVE_PIN_MAP[5])

	def test_raises_exception_if_valve_no_is_out_of_scope(self, gpioMock):
		self.assertRaises(IndexError, devices.Valve.open, 0)
		self.assertRaises(IndexError, devices.Valve.close, 6)


@patch('raspberrypi.devices.interfaces.DO', autospec=True)
class PumpModuleTest(TestCase):
	
	def test_starts_pump_1(self, gpioMock):
		devices.Pump.start(1)
		gpioMock.off.assert_called_once_with(enums.PUMP_PIN_MAP[1])

	def test_starts_pump_3(self, gpioMock):
		devices.Pump.start(3)
		gpioMock.off.assert_called_once_with(enums.PUMP_PIN_MAP[3])

	def test_stops_pump_1(self, gpioMock):
		devices.Pump.stop(1)
		gpioMock.on.assert_called_once_with(enums.PUMP_PIN_MAP[1])

	def test_stops_pump_3(self, gpioMock):
		devices.Pump.stop(3)
		gpioMock.on.assert_called_once_with(enums.PUMP_PIN_MAP[3])

