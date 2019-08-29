from .devices import Heater, Pump, Valve, Thermistor

from . import enums

from mainapp.models import Experiment, Temperature

from threading import Thread

import time

# flag to indicate automation loop state 
running = False

# experiment object is created and saved for each automation session 
experiment = None

# regularly fetched thermistor temperature array

temperature_list = []

def update_temperature_list():
	global running, experiment, temperature_list

	while True:
		temperature_list = Thermistor.temperature_list()

		if running:
			Temperature.objects.create(
				experiment = experiment,
				thermistor_1 = temperature_list[0],
				thermistor_2 = temperature_list[1],
				thermistor_3 = temperature_list[2],
				thermistor_4 = temperature_list[3],
				thermistor_5 = temperature_list[4],
				thermistor_6 = temperature_list[5],
				thermistor_7 = temperature_list[6],
				thermistor_8 = temperature_list[7],
			).save()

		time.sleep(enums.TEMPERATURE_REFRESH_INTERVAL)

Thread(target=update_temperature_list, daemon=True).start()

# define devices
device_map = {
	'heater_1': Heater(1),
	'heater_2': Heater(2),

	'pump_1': Pump(1),
	'pump_2': Pump(2),
	'pump_3': Pump(3),

	'valve_1': Valve(1),
	'valve_2': Valve(2),
	'valve_3': Valve(3),
	'valve_4': Valve(4),
	'valve_5': Valve(5)
}

def start():
	global running, experiment
	running = True
	
	experiment = Experiment.objects.create()
	experiment.save()

def stop():
	global running, experiment
	running = False

	experiment.save()

def toggle():
	global running
	running = not running




