import json

from raspberrypi import enums

def device_count(device_type):
	if device_type == 'heater': return len(enums.HEATER_PIN_MAP)
	if device_type == 'valve': return len(enums.VALVE_PIN_MAP)
	if device_type == 'pump': return len(enums.PUMP_PIN_MAP)


def thermistor_state_as_json(device_id):
	from raspberrypi import automation

	device_no = int(device_id)
	return json.dumps([{ 'id': device_no, 'temperature': automation.temperature_list[device_no - 1] }])


def thermistor_state_list_as_json():
	from raspberrypi import automation

	return json.dumps([{'id': idx + 1, 'temperature': automation.temperature_list[idx]} for idx in range(len(automation.temperature_list))])


def generic_device_state_as_json(device_type, device_id):
	from raspberrypi import automation

	return json.dumps([{ 'id': int(device_id), 'state': automation.device_map[device_type + '_' + device_id].state() }])


def generic_devices_state_list_as_json(device_type):
	from raspberrypi import automation	
	
	device_state_array = [automation.device_map[device_type + '_' + str(idx+1)].state() for idx in range(device_count(device_type))]
	return json.dumps([{ 'id': idx + 1, 'state': int(device_state_array[idx]) } for idx in range(len(device_state_array))])
