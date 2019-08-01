from django.http import HttpResponse

import json

from raspberrypi import enums
from raspberrypi import devices

def thermistor_view(request, device_id=None):
	temperature_array = []

	if device_id:
		temperature_array.append(devices.Thermistor.temperature(int(device_id)))
	else:
		temperature_array = devices.Thermistor.temperatureArray()

	return HttpResponse(json.dumps([{ 'id': idx + 1, 'temperature': float(temperature_array[idx]) } for idx in range(len(temperature_array))]), content_type='application/json')

