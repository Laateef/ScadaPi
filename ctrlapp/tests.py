from unittest import TestCase
from unittest.mock import patch

import smbus2

from . import ControlApi, Enums

class AnalogInputModuleTest(TestCase):
	
	@patch('smbus2.SMBus')
	def test_configuring_a_channel_for_reading(self, SMBusMock):
		adc = ControlApi.ADC(SMBusMock)
		adc.configureChannel(0)
		self.assertEqual(SMBusMock.write_i2c_block_data.called, True)
		(i2c_address, register_address, data_array), kwargs = SMBusMock.write_i2c_block_data.call_args
		self.assertEqual(i2c_address, Enums.ADC_I2C_ADDRESS_1)
		self.assertEqual(register_address, Enums.ADC_REG_CONFIGURATION)
		self.assertEqual(data_array, [ Enums.AIN_CFG_HByte | (0x04 << Enums.ADC_CFG_MUX_OFFSET), Enums.AIN_CFG_LByte ])
