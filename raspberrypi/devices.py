from raspberrypi import interfaces
from raspberrypi import enums

import math

class Thermistor:
	def adc_to_voltage(adc_value):
		return enums.ADC_SCALE_LSB_SIZE_IN_VOLT * adc_value

	def voltage_to_resistance(voltage_value):
		# To make higher voltage refers to higher temperature we inverse the voltage against the source
		voltage_value = enums.ADC_SOURCE_VOLTAGE - voltage_value

		return enums.ADC_REFERENCE_RESISTANCE * ( voltage_value / (enums.ADC_SOURCE_VOLTAGE - voltage_value) )

	def resistance_to_temperature(resistance_value):
		return (1.0 / ( ( math.log(resistance_value / enums.NTC_NOMINAL_RESISTANCE) / enums.NTC_TEMPERATURE_COEFFICIENT ) + ( 1.0 / (enums.NTC_STANDARD_TEMPERATURE + enums.KELVIN_CONVERSION_CONSTANT) ) ) ) - enums.KELVIN_CONVERSION_CONSTANT

	def adc_to_temperature(adc_value):
		return Thermistor.resistance_to_temperature(Thermistor.voltage_to_resistance(Thermistor.adc_to_voltage(adc_value)))
	
	def temperature(channel):
		if channel < 1 or channel > 8:
			raise IndexError

		return Thermistor.adc_to_temperature(interfaces.ADC().readChannel(channel - 1))
	
	def temperatureArray():
		ary = []
		adc = interfaces.ADC()
		for ch in range(0, enums.TOTAL_CHANNEL_COUNT):
			ary.insert(ch, Thermistor.adc_to_temperature(adc.readChannel(ch)))

		return ary


class GenericDevice:
	def __init__(self, device_pin_map, device_no):
		self.device_pin_map = device_pin_map
		self.device_no = device_no

		if self.device_no not in self.device_pin_map:
			raise IndexError

	def on(self):
		interfaces.DO.on(self.device_pin_map[self.device_no])

	def off(self):
		interfaces.DO.off(self.device_pin_map[self.device_no])

	def state(self):
		return interfaces.DO.state(self.device_pin_map[self.device_no])

	def toggle(self):
		interfaces.DO.toggle(self.device_pin_map[self.device_no])


class Heater(GenericDevice):
	def __init__(self, device_no):
		super().__init__(enums.HEATER_PIN_MAP, device_no)


class Valve(GenericDevice):
	def __init__(self, device_no):
		super().__init__(enums.VALVE_PIN_MAP, device_no)


class Pump(GenericDevice):
	def __init__(self, device_no):
		super().__init__(enums.PUMP_PIN_MAP, device_no)
