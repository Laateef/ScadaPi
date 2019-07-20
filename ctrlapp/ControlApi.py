import smbus2

from . import Enums

class ADC:
	bus = None
	
	def __init__(self, i2c_bus):
		self.bus = i2c_bus
	
	def configureChannel(self, arg):
		self.bus.write_i2c_block_data(0x00, 0x00, [ 0x00, 0x00 ])
