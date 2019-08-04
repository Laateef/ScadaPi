import json

from raspberrypi import enums
from raspberrypi import devices

def device_class(device_type):
	if device_type == 'heater': return devices.Heater
	if device_type == 'valve': return devices.Valve
	if device_type == 'pump': return devices.Pump

def device_count(device_type):
	if device_type == 'heater': return len(enums.HEATER_PIN_MAP)
	if device_type == 'valve': return len(enums.VALVE_PIN_MAP)
	if device_type == 'pump': return len(enums.PUMP_PIN_MAP)

def thermistor_state_as_json(device_id):
	device_no = int(device_id)
	return json.dumps([{ 'id': device_no, 'temperature': float(devices.Thermistor.temperature(device_no)) }])

def thermistor_state_list_as_json():
	temperature_array = devices.Thermistor.temperatureArray()
	return json.dumps([{'id': idx + 1, 'temperature': float(temperature_array[idx])} for idx in range(len(temperature_array))])

def generic_device_state_as_json(device_type, device_id):
	device_no = int(device_id)
	return json.dumps([{ 'id': device_no, 'state': device_class(device_type)(device_no).state() }])

def generic_devices_state_list_as_json(device_type):
	device_state_array = [device_class(device_type)(idx+1).state() for idx in range(device_count(device_type))]
	return json.dumps([{ 'id': idx + 1, 'state': int(device_state_array[idx]) } for idx in range(len(device_state_array))])
