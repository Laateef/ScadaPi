import smbus2

from . import Enums

class ADC:
	bus = None
	
	def __init__(self, i2c_bus):
		self.bus = i2c_bus
	
	def configureChannel(self, channel):
		if 0 > channel or channel > 7:
			raise IndexError('The channel must be between 0 and 7')

		self.bus.write_i2c_block_data(Enums.ADC_I2C_ADDRESS_1 + channel // Enums.CHANNEL_COUNT, 
			Enums.ADC_REG_CONFIGURATION, 
			[Enums.AIN_CMN_CFG_HByte | (Enums.ADC_CFG_MUX_AIN_0 + ( (channel % Enums.CHANNEL_COUNT) << Enums.ADC_CFG_MUX_OFFSET ) ), Enums.AIN_CMN_CFG_LByte])
