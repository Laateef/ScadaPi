from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

from raspberrypi import devices

from . import util, models

import json

import os

def thermistor_view(request, thermistor_id=None):
	return HttpResponse(util.thermistor_state_as_json(thermistor_id) if thermistor_id else util.thermistor_state_list_as_json(), content_type='application/json')

def single_generic_device_state_view(request, device_type, device_id):
	return HttpResponse(util.generic_device_state_as_json(device_type, device_id), content_type='application/json')


def multiple_generic_device_state_view(request, device_type):
	return HttpResponse(util.generic_devices_state_list_as_json(device_type), content_type='application/json')


def single_generic_device_actuation_view(request, device_type, device_id, device_op):
	from raspberrypi import automation

	device = automation.device_map[device_type + '_' + device_id]

	if device_op == 'toggle': device.toggle()
	elif device_op == 'on':	device.on()
	elif device_op == 'off': device.off()

	return HttpResponse()

def all_devices_state_list_view(request):
	from raspberrypi import automation

	return HttpResponse(json.dumps({
			'thermistor': json.loads(util.thermistor_state_list_as_json()),
			'heater': json.loads(util.generic_devices_state_list_as_json('heater')),
			'valve': json.loads(util.generic_devices_state_list_as_json('valve')),
			'pump': json.loads(util.generic_devices_state_list_as_json('pump')),
			'automation' : { 'state': (automation.running * 1) }
		}), content_type='application/json')

def automation_view(request, operation=None):
	from raspberrypi import automation

	if operation:
		if operation == 'start': automation.start()
		elif operation == 'stop': automation.stop()
		elif operation == 'toggle': automation.toggle()		
		return HttpResponse()

	return HttpResponse(json.dumps([{ 'state': (automation.running * 1) }]), content_type='application/json')

def experiment_view(request):
	last_experiment_id = request.GET.get('last')

	experiment_list = models.Experiment.objects.all().order_by('id')

	if last_experiment_id:
		experiment_list = experiment_list.filter(id__gt=last_experiment_id)
	
	return HttpResponse(json.dumps([{'id': e.id, 'start_date': e.start_date.replace(tzinfo=None).isoformat('T', 'seconds'), 'end_date': e.end_date.replace(tzinfo=None).isoformat('T', 'seconds')} for e in experiment_list]), content_type='application/json')

def experiment_deletion_view(request, experiment_id):
	models.Experiment.objects.filter(id=experiment_id).delete()

	return HttpResponse()

def temperature_view(request):
	temperature_object_list = models.Temperature.objects.filter(experiment=request.GET.get('experiment'))

	last_fetch_date = request.GET.get('last_date')

	if last_fetch_date:
		temperature_object_list = temperature_object_list.filter(date__gt=make_aware(parse_datetime(last_fetch_date)))

	return HttpResponse(json.dumps([{
				'id': t.id,
				'experiment': t.experiment_id,
				'date': t.date.replace(tzinfo=None).isoformat('T', 'seconds'),
				'temperature_array': [float(t.thermistor_1), float(t.thermistor_2), float(t.thermistor_3), float(t.thermistor_4), float(t.thermistor_5), float(t.thermistor_6), float(t.thermistor_7), float(t.thermistor_8)]
					} for t in temperature_object_list]), content_type='application/json')

def provision_view(request):
	os.system("cd /home/pi/project/scadapi")
	os.system("git checkout -- .")
	os.system("git pull")
	os.system("ps aux | grep gunicorn | grep scadapi | awk '{ print $2 }' | xargs kill -HUP")

	return HttpResponse()

