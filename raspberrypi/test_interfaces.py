from unittest import TestCase
from unittest.mock import patch

from raspberrypi import enums
from raspberrypi import interfaces


class AnalogInputModuleTest(TestCase):

	@patch('raspberrypi.interfaces.smbus2.SMBus', autospec=True)
	def setUp(self, busMock):
		self.adc = interfaces.ADC()
		self.bus = busMock.return_value

	def test_ADC_closes_the_bus_when_deleted(self):	
		self.adc.__del__()

		self.bus.close.assert_called_once()
	
	def test_readChannel_configures_channel_0_for_reading(self):
		self.adc.readChannel(0)

		self.bus.write_i2c_block_data.assert_called_once_with(enums.ADC_I2C_ADDRESS_1, 
								enums.ADC_REG_CONFIGURATION, 
								[enums.AIN_CMN_CFG_HByte | enums.ADC_CFG_MUX_AIN_0, enums.AIN_CMN_CFG_LByte])

	def test_readChannel_configures_channel_1_for_reading(self):
		self.adc.readChannel(1)

		self.bus.write_i2c_block_data.assert_called_once_with(enums.ADC_I2C_ADDRESS_1, 
								enums.ADC_REG_CONFIGURATION, 
								[enums.AIN_CMN_CFG_HByte | enums.ADC_CFG_MUX_AIN_1, enums.AIN_CMN_CFG_LByte])

	def test_readChannel_configures_channel_4_for_reading(self):	
		self.adc.readChannel(4)

		self.bus.write_i2c_block_data.assert_called_once_with(enums.ADC_I2C_ADDRESS_2, 
								enums.ADC_REG_CONFIGURATION, 
								[enums.AIN_CMN_CFG_HByte | enums.ADC_CFG_MUX_AIN_0, enums.AIN_CMN_CFG_LByte])

	def test_readChannel_raises_exception_if_channel_index_is_out_of_range(self):
		self.assertRaises(IndexError, self.adc.readChannel, -1)
		self.assertRaises(IndexError, self.adc.readChannel, 8)

	def test_readChannel_reads_channel_0(self):
		self.adc.readChannel(0)

		self.bus.read_i2c_block_data.assert_called_once_with(enums.ADC_I2C_ADDRESS_1, enums.ADC_REG_CONVERSION, 2)

	def test_readChannel_reads_channel_7(self):
		self.adc.readChannel(7)

		self.bus.read_i2c_block_data.assert_called_once_with(enums.ADC_I2C_ADDRESS_2, enums.ADC_REG_CONVERSION, 2)

	@patch('raspberrypi.interfaces.time.sleep', autospec=True)
	def test_readChannel_waits_until_conversion_is_done(self, time_sleep_mock):
		self.adc.readChannel(6)

		self.bus.write_i2c_block_data.assert_called_once()
		# To be on the safe side, readChannel should wait 1 msec more after the config is written.
		time_sleep_mock.assert_called_once_with(1.0 / enums.ADC_SAMPLE_PER_SECOND + 0.001)
		self.bus.read_i2c_block_data.assert_called_once()

	def test_readChannel_returns_zero_integer_for_zero(self):
		self.bus.read_i2c_block_data.return_value = [0x00, 0x00]

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


@patch('raspberrypi.interfaces.gpiozero.OutputDevice', autospec=True)
class DigitalOutputModuleTest(TestCase):
	
	def test_turns_channel_0_off(self, gpioMock):
		interfaces.DO.off(0)

		gpioMock.assert_called_once_with(0, active_high=False)
		gpioMock.return_value.off.assert_called_once()

	def test_turns_channel_7_off(self, gpioMock):
		interfaces.DO.off(7)

		gpioMock.assert_called_once_with(7, active_high=False)
		gpioMock.return_value.off.assert_called_once()
		
	def test_turns_channel_0_on(self, gpioMock):
		interfaces.DO.on(0)

		gpioMock.assert_called_once_with(0, active_high=False)
		gpioMock.return_value.on.assert_called_once()

	def test_turns_channel_7_on(self, gpioMock):
		interfaces.DO.on(7)

		gpioMock.assert_called_once_with(7, active_high=False)
		gpioMock.return_value.on.assert_called_once()
		
	def test_returns_state_of_channel_5(self, gpioMock):
		gpioMock.return_value.value = False

		self.assertEqual(interfaces.DO.state(5), False)

		gpioMock.assert_called_once_with(5, active_high=False)

	def test_toggles_the_output_of_channel_2(self, gpioMock):
		gpioMock.return_value.value = False
		self.assertEqual(interfaces.DO.state(2), False)

		interfaces.DO.toggle(2)

		gpioMock.return_value.value = True
		self.assertEqual(interfaces.DO.state(2), True)
		self.assertEqual(gpioMock.call_count, 3)
		gpioMock.assert_called_with(2, active_high=False)
		gpioMock.return_value.toggle.assert_called_once()
		
