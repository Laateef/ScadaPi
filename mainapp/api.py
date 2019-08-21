from django.http import HttpResponse

from raspberrypi import devices
from raspberrypi import automation

from mainapp import util

import json

def thermistor_view(request, thermistor_id=None):
	return HttpResponse(util.thermistor_state_as_json(thermistor_id) if thermistor_id else util.thermistor_state_list_as_json(), content_type='application/json')

def single_generic_device_state_view(request, device_type, device_id):
	return HttpResponse(util.generic_device_state_as_json(device_type, device_id), content_type='application/json')


def multiple_generic_device_state_view(request, device_type):
	return HttpResponse(util.generic_devices_state_list_as_json(device_type), content_type='application/json')


def single_generic_device_actuation_view(request, device_type, device_id, device_op):
	device_no = int(device_id)

	device = util.device_class(device_type)(device_no)

	if device_op == 'toggle': device.toggle()
	elif device_op == 'on':	device.on()
	elif device_op == 'off': device.off()

	return HttpResponse()

def all_devices_state_list_view(request):
	return HttpResponse(json.dumps([{ 'thermistor': json.loads(util.thermistor_state_list_as_json()) },
					{ 'heater': json.loads(util.generic_devices_state_list_as_json('heater')) },
					{ 'valve': json.loads(util.generic_devices_state_list_as_json('valve')) },
					{ 'pump': json.loads(util.generic_devices_state_list_as_json('pump')) } ]), content_type='application/json')

def automation_view(request, operation=None):
	if operation:
		if operation == 'start': automation.start()
		elif operation == 'stop': automation.stop()
		elif operation == 'toggle': automation.toggle()		
		return HttpResponse()

	return HttpResponse(json.dumps([{ 'state': automation.running }]), content_type='application/json')

