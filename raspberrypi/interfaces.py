import time
import smbus2
import gpiozero

from . import enums

class ADC:
	def __init__(self):
		self.bus = smbus2.SMBus(1)
	
	def __del__(self):
		self.bus.close()

	def readChannel(self, channel):
		if 0 > channel or channel > 7:
			raise IndexError('The channel must be between 0 and 7')

		self.bus.write_i2c_block_data(enums.ADC_I2C_ADDRESS_1 + channel // enums.MODULE_CHANNEL_COUNT, 
			enums.ADC_REG_CONFIGURATION, 
			[enums.AIN_CMN_CFG_HByte | (enums.ADC_CFG_MUX_AIN_0 + ( (channel % enums.MODULE_CHANNEL_COUNT) << enums.ADC_CFG_MUX_OFFSET ) ), enums.AIN_CMN_CFG_LByte])

		time.sleep(1.0 / enums.ADC_SAMPLE_PER_SECOND + 0.001)

		data_bytes = self.bus.read_i2c_block_data(enums.ADC_I2C_ADDRESS_1 + channel // enums.MODULE_CHANNEL_COUNT, enums.ADC_REG_CONVERSION, 2)
 

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

class DO:
	def off(self, channel):
		gpiozero.LED(channel).off()

	def on(self, channel):
		gpiozero.LED(channel).on()
