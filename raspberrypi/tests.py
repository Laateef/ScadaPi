from unittest import TestCase
from unittest.mock import patch
from unittest import mock

import smbus2


from raspberrypi import interfaces
from raspberrypi import enums

class AnalogInputModuleTest(TestCase):

	@patch('smbus2.SMBus')
	def setUp(self, SMBusMock):
		self.bus = SMBusMock	
		self.adc = interfaces.ADC(self.bus)
	
	def test_readChannel_configures_channel_0_for_reading(self):
		self.adc.readChannel(0)

		self.bus.write_i2c_block_data.assert_called_with(enums.ADC_I2C_ADDRESS_1, 
								enums.ADC_REG_CONFIGURATION, 
								[enums.AIN_CMN_CFG_HByte | enums.ADC_CFG_MUX_AIN_0, enums.AIN_CMN_CFG_LByte])

	def test_readChannel_configures_channel_1_for_reading(self):
		self.adc.readChannel(1)

		self.bus.write_i2c_block_data.assert_called_with(enums.ADC_I2C_ADDRESS_1, 
								enums.ADC_REG_CONFIGURATION, 
								[enums.AIN_CMN_CFG_HByte | enums.ADC_CFG_MUX_AIN_1, enums.AIN_CMN_CFG_LByte])

	def test_readChannel_configures_channel_4_for_reading(self):
		self.adc.readChannel(4)

		self.bus.write_i2c_block_data.assert_called_with(enums.ADC_I2C_ADDRESS_2, 
								enums.ADC_REG_CONFIGURATION, 
								[enums.AIN_CMN_CFG_HByte | enums.ADC_CFG_MUX_AIN_0, enums.AIN_CMN_CFG_LByte])

	def test_readChannel_raises_exception_if_channel_index_is_out_of_range(self):
		self.assertRaises(IndexError, self.adc.readChannel, -1)
		self.assertRaises(IndexError, self.adc.readChannel, 8)

	def test_readChannel_reads_channel_0(self):
		self.adc.readChannel(0)

		self.bus.read_i2c_block_data.assert_called_with(enums.ADC_I2C_ADDRESS_1, enums.ADC_REG_CONVERSION, 2)

	def test_readChannel_reads_channel_7(self):
		self.adc.readChannel(7)

		self.bus.read_i2c_block_data.assert_called_with(enums.ADC_I2C_ADDRESS_2, enums.ADC_REG_CONVERSION, 2)

	@patch('time.sleep')
	def test_readChannel_waits_until_conversion_is_done(self, time_sleep_mock):
		self.adc.readChannel(6)

		self.assertTrue(self.bus.write_i2c_block_data.called)
		# To be on the safe side, readChannel should wait 1 msec more after the config is written.
		time_sleep_mock.assert_called_with(1.0 / enums.ADC_SAMPLE_PER_SECOND + 0.001)
		self.assertTrue(self.bus.read_i2c_block_data.called)

	def test_readChannel_returns_zero_integer_for_zero(self):
		self.bus.read_i2c_block_data = mock.Mock('self.bus.read_i2c_block_data', return_value = [0x00, 0x00])

		adc_value = self.adc.readChannel(7)

		self.assertEqual(adc_value, 0)
		self.assertEqual(type(adc_value), int)

	def test_readChannel_returns_two_complement_conversion_for_negatives(self):
		self.bus.read_i2c_block_data.return_value = [0x80, 0x00]

		adc_value = self.adc.readChannel(7)

		self.assertEqual(adc_value, -32768)

	def test_readChannel_returns_two_complement_conversion_for_positives(self):
		self.bus.read_i2c_block_data.return_value = [0x7F, 0xFF]

		adc_value = self.adc.readChannel(7)

		self.assertEqual(adc_value, 32767)

























