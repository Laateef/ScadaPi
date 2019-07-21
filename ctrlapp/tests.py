from unittest import TestCase
from unittest.mock import patch

import smbus2

from . import ControlApi, Enums

class AnalogInputModuleTest(TestCase):

	@patch('smbus2.SMBus')
	def setUp(self, SMBusMock):
		self.bus = SMBusMock	
		self.adc = ControlApi.ADC(self.bus)
	
	def test_readChannel_configures_channel_0_for_reading(self):
		self.adc.readChannel(0)

		self.assertTrue(self.bus.write_i2c_block_data.called)
		(i2c_address, register_address, data_array), kwargs = self.bus.write_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_1)
		self.assertEqual(register_address, Enums.ADC_REG_CONFIGURATION)
		self.assertEqual(data_array, [Enums.AIN_CMN_CFG_HByte | Enums.ADC_CFG_MUX_AIN_0, Enums.AIN_CMN_CFG_LByte])

	def test_readChannel_configures_channel_1_for_reading(self):
		self.adc.readChannel(1)

		self.assertTrue(self.bus.write_i2c_block_data.called)
		(i2c_address, register_address, data_array), kwargs = self.bus.write_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_1)
		self.assertEqual(register_address, Enums.ADC_REG_CONFIGURATION)
		self.assertEqual(data_array, [Enums.AIN_CMN_CFG_HByte | Enums.ADC_CFG_MUX_AIN_1, Enums.AIN_CMN_CFG_LByte])

	def test_readChannel_configures_channel_4_for_reading(self):
		self.adc.readChannel(4)

		self.assertTrue(self.bus.write_i2c_block_data.called)
		(i2c_address, register_address, data_array), kwargs = self.bus.write_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_2)
		self.assertEqual(register_address, Enums.ADC_REG_CONFIGURATION)
		self.assertEqual(data_array, [Enums.AIN_CMN_CFG_HByte | Enums.ADC_CFG_MUX_AIN_0, Enums.AIN_CMN_CFG_LByte])

	def test_readChannel_raises_exception_if_channel_index_is_out_of_range(self):
		self.assertRaises(IndexError, self.adc.readChannel, -1)
		self.assertRaises(IndexError, self.adc.readChannel, 8)

	def test_readChannel_reads_channel_0(self):
		self.adc.readChannel(0)

		self.assertTrue(self.bus.read_i2c_block_data.called)
		(i2c_address, register_address, data_array_size), kwargs = self.bus.read_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_1)
		self.assertEqual(register_address, Enums.ADC_REG_CONVERSION)
		self.assertEqual(data_array_size, 2)

	def test_readChannel_reads_channel_7(self):
		self.adc.readChannel(7)

		self.assertTrue(self.bus.read_i2c_block_data.called)
		(i2c_address, register_address, data_array_size), kwargs = self.bus.read_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_2)
		self.assertEqual(register_address, Enums.ADC_REG_CONVERSION)
		self.assertEqual(data_array_size, 2)

	@patch('time.sleep')
	def test_readChannel_waits_until_conversion_is_done(self, time_sleep_mock):
		self.adc.readChannel(6)

		self.assertTrue(self.bus.write_i2c_block_data.called)
		self.assertTrue(time_sleep_mock.called)
		args, kwargs = time_sleep_mock.call_args
		# To be on the safe side, 1 msec is added to the sleep function
		self.assertAlmostEqual(args[0], 1.0 / Enums.ADC_SAMPLE_PER_SECOND + 0.001) 
		self.assertTrue(self.bus.read_i2c_block_data.called)

