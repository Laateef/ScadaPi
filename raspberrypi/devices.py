from raspberrypi import interfaces
from raspberrypi import enums

import math

class Thermistor:
	def adc_to_voltage(adc_value):
		return enums.ADC_SCALE_LSB_SIZE_IN_VOLT * adc_value

	def voltage_to_resistance(voltage_value):
		# Source Voltage: 3.3(v)
		v_src = 3.3	
	
		# Reference Resistance: 10000(ohm)
		r_ref = 10000

		# To make higher voltage refers to higher temperature we inverse the voltage against the source
		voltage_value = v_src - voltage_value

		return r_ref * ( voltage_value / (v_src - voltage_value) )

	def resistance_to_temperature(resistance_value):
		# Thermistor Nominal Resistance at 25(c): 10000(ohm)
		th_r25 = 10000

		# Thermistor Temperature Coefficient: 3980
		th_beta = 3980

		# Kelvin Conversion Constant	
		k_const = 273.15 	

		return (1.0 / ( ( math.log(resistance_value / th_r25) / th_beta ) + ( 1.0 / (25 + k_const) ) ) ) - k_const

	def adc_to_temperature(adc_value):
		return Thermistor.resistance_to_temperature(Thermistor.voltage_to_resistance(Thermistor.adc_to_voltage(adc_value)))
	
	def temperature(channel):
		return Thermistor.adc_to_temperature(interfaces.ADC().readChannel(channel))
	
	def temperatureArray():
		ary = []
		adc = interfaces.ADC()
		for ch in range(0, enums.TOTAL_CHANNEL_COUNT):
			ary.insert(ch, Thermistor.adc_to_temperature(adc.readChannel(ch)))

		return ary

class Heater:
	def start():
		interfaces.DO.on(enums.HEATER_PIN_1)
		interfaces.DO.on(enums.HEATER_PIN_2)

	def stop():
		interfaces.DO.off(enums.HEATER_PIN_1)
		interfaces.DO.off(enums.HEATER_PIN_2)

class Valve:
	def _check_valve_no(no):
		if no not in enums.VALVE_PIN_MAP.keys():
			raise IndexError

	def open(no):
		Valve._check_valve_no(no)
		interfaces.DO.on(enums.VALVE_PIN_MAP[no])

	def close(no):
		Valve._check_valve_no(no)
		interfaces.DO.off(enums.VALVE_PIN_MAP[no])


class Pump:
	def _check_pump_no(no):
		if no not in enums.PUMP_PIN_MAP.keys():
			raise IndexError

	def start(no):
		Pump._check_pump_no(no)
		interfaces.DO.on(enums.PUMP_PIN_MAP[no])

	def stop(no):
		Pump._check_pump_no(no)
		interfaces.DO.off(enums.PUMP_PIN_MAP[no])


