from raspberrypi import interfaces
from raspberrypi import enums

import math

class Thermistor:
	@staticmethod
	def adc_to_voltage(adc_value):
		return enums.ADC_SCALE_LSB_SIZE_IN_VOLT * adc_value

	@staticmethod
	def voltage_to_resistance(voltage_value):
		if voltage_value == 0:
			raise ValueError

		return enums.ADC_REFERENCE_RESISTANCE * ( (enums.ADC_SOURCE_VOLTAGE / voltage_value) - 1 )

	@staticmethod
	def resistance_to_temperature(resistance_value):
		if resistance_value <= 0:
			raise ValueError

		return (1.0 / ( ( math.log(resistance_value / enums.NTC_NOMINAL_RESISTANCE) / enums.NTC_TEMPERATURE_COEFFICIENT ) + ( 1.0 / (enums.NTC_STANDARD_TEMPERATURE + enums.KELVIN_CONVERSION_CONSTANT) ) ) ) - enums.KELVIN_CONVERSION_CONSTANT

	@staticmethod
	def adc_to_temperature(adc_value):
		return Thermistor.resistance_to_temperature(Thermistor.voltage_to_resistance(Thermistor.adc_to_voltage(adc_value)))

	@staticmethod
	def get_temperature_from_adc_channel(adc, channel):
		if channel < 0 or channel > 7:
			raise IndexError

		try:
			temperature_value = float("{0:.1f}".format(Thermistor.adc_to_temperature(adc.readChannel(channel))))
		except:
			temperature_value = 999.9;

		return temperature_value

	@staticmethod
	def temperature(channel):
			return Thermistor.get_temperature_from_adc_channel(interfaces.ADC(), channel - 1)
	
	@staticmethod
	def temperature_list():
		ary = []
		adc = interfaces.ADC()
		for ch in range(0, enums.TOTAL_CHANNEL_COUNT):
			ary.insert(ch, Thermistor.get_temperature_from_adc_channel(adc, ch))

		return ary

class Heater(interfaces.GenericDevice):
	def __init__(self, device_no):
		super().__init__(enums.HEATER_PIN_MAP, device_no)

class Valve(interfaces.GenericDevice):
	def __init__(self, device_no):
		super().__init__(enums.VALVE_PIN_MAP, device_no)


class Pump(interfaces.GenericDevice):
	def __init__(self, device_no):
		super().__init__(enums.PUMP_PIN_MAP, device_no)
