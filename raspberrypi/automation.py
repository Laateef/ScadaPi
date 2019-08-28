from raspberrypi.devices import Heater
from raspberrypi.devices import Pump
from raspberrypi.devices import Valve
from raspberrypi.devices import Thermistor

from threading import Thread

import time

# regularly fetched thermistor temperature array

temperature_list = []

def update_temperature_list():
	global temperature_list

	while True:
		temperature_list = Thermistor.temperature_list()
		time.sleep(1)

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

# flag to indicate automation loop state 
running = False

def start():
	global running
	running = True

def stop():
	global running
	running = False

def toggle():
	global running
	running = not running




