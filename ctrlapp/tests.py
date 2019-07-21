from unittest import TestCase
from unittest.mock import patch

import smbus2

from . import ControlApi, Enums

class AnalogInputModuleTest(TestCase):

	@patch('smbus2.SMBus')
	def setUp(self, SMBusMock):
		self.bus = SMBusMock	
		self.adc = ControlApi.ADC(self.bus)
	
	
	def test_configures_channel_0_for_reading(self):
		self.adc.configureChannel(0)

		self.assertEqual(self.bus.write_i2c_block_data.called, True)
		(i2c_address, register_address, data_array), kwargs = self.bus.write_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_1)
		self.assertEqual(register_address, Enums.ADC_REG_CONFIGURATION)
		self.assertEqual(data_array, [Enums.AIN_CMN_CFG_HByte | Enums.ADC_CFG_MUX_AIN_0, Enums.AIN_CMN_CFG_LByte])

	def test_configures_channel_1_for_reading(self):
		self.adc.configureChannel(1)

		self.assertEqual(self.bus.write_i2c_block_data.called, True)
		(i2c_address, register_address, data_array), kwargs = self.bus.write_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_1)
		self.assertEqual(register_address, Enums.ADC_REG_CONFIGURATION)
		self.assertEqual(data_array, [Enums.AIN_CMN_CFG_HByte | Enums.ADC_CFG_MUX_AIN_1, Enums.AIN_CMN_CFG_LByte])

	def test_configures_channel_4_for_reading(self):
		self.adc.configureChannel(4)

		self.assertEqual(self.bus.write_i2c_block_data.called, True)
		(i2c_address, register_address, data_array), kwargs = self.bus.write_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_2)
		self.assertEqual(register_address, Enums.ADC_REG_CONFIGURATION)
		self.assertEqual(data_array, [Enums.AIN_CMN_CFG_HByte | Enums.ADC_CFG_MUX_AIN_0, Enums.AIN_CMN_CFG_LByte])

	def test_configures_out_of_range_channel_will_raise_exception(self):
		self.assertRaises(IndexError, self.adc.configureChannel, -1)
		self.assertRaises(IndexError, self.adc.configureChannel, 8)


