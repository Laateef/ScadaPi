import time
import smbus2

from . import Enums

class ADC:
	bus = None
	
	def __init__(self, i2c_bus):
		self.bus = i2c_bus
	
	def readChannel(self, channel):
		if 0 > channel or channel > 7:
			raise IndexError('The channel must be between 0 and 7')

		self.bus.write_i2c_block_data(Enums.ADC_I2C_ADDRESS_1 + channel // Enums.CHANNEL_COUNT, 
			Enums.ADC_REG_CONFIGURATION, 
			[Enums.AIN_CMN_CFG_HByte | (Enums.ADC_CFG_MUX_AIN_0 + ( (channel % Enums.CHANNEL_COUNT) << Enums.ADC_CFG_MUX_OFFSET ) ), Enums.AIN_CMN_CFG_LByte])

		time.sleep(1.0 / Enums.ADC_SAMPLE_PER_SECOND + 0.001)

		data_bytes = self.bus.read_i2c_block_data(Enums.ADC_I2C_ADDRESS_1 + channel // Enums.CHANNEL_COUNT, Enums.ADC_REG_CONVERSION, 2)
 

		# Note that ADS1115's conversion register contains the result in binary tow's complement format.
		adc_value = int(data_bytes[0] * 256 + data_bytes[1])

		# As an example, the following is tow's complement binary representation vs the decimal representation for two bits:
		# 0B10 == -2 
		# 0B11 == -1
		# 0B00 ==  0
		# 0B01 == +1 
		#
		# Any number whose MSB is 1 is a negative number, i.e., values bigger than 0B0111111111111111 refer to negative numbers
		# The negative number can be obtained by subtracting 2^bit_count i.e., 2^16 = 65536 from adc_value. 
		if adc_value > 32767:
        		adc_value -= 65536

		return adc_value
