# ADS1115 Bit Enumeration
# -----------------------
# ADC I2C Address 
ADC_I2C_ADDRESS_1		= 0x48 
ADC_I2C_ADDRESS_2		= 0x49

# ADC Register
ADC_REG_CONVERSION		= 0x00
ADC_REG_CONFIGURATION		= 0x01

# ADC Configuration Register
ADC_CFG_OS			= 0x80 # Begin a single conversion
ADC_CFG_MUX_AIN_0		= 0x40 # Single-ended P = AIN0, N = GND
ADC_CFG_MUX_AIN_1		= 0x50 # Single-ended P = AIN1, N = GND
ADC_CFG_MUX_AIN_2		= 0x60 # Single-ended P = AIN2, N = GND
ADC_CFG_MUX_AIN_3		= 0x70 # Single-ended P = AIN3, N = GND
ADC_CFG_MUX_OFFSET		= 0x04
ADC_CFG_PGA			= 0x01 # +/-4.096V range = Gain 1
ADC_CFG_MODE			= 0x00 # Continuous conversion mode
ADC_CFG_DR			= 0x80 # 128 samples per second
ADC_CFG_COMP_QUE		= 0x03 # Disable the comparator and put ALERT/RDY in high state


ADC_SCALE_LSB_SIZE_IN_VOLT	= 0.000125 
ADC_SAMPLE_PER_SECOND		= 128

AIN_CMN_CFG_HByte 		= ADC_CFG_OS | ADC_CFG_PGA | ADC_CFG_MODE
AIN_CMN_CFG_LByte 		= ADC_CFG_DR | ADC_CFG_COMP_QUE

MODULE_CHANNEL_COUNT		= 4
TOTAL_CHANNEL_COUNT		= 8
		
ADC_SOURCE_VOLTAGE		= 3.3 	 # Source Voltage: 3.3(v)		
ADC_REFERENCE_RESISTANCE	= 10000  # Reference Resistance: 10000(ohm)

NTC_STANDARD_TEMPERATURE	= 25 	 # Thermistor Standard Temperature: 25(c) 
NTC_NOMINAL_RESISTANCE		= 10000  # Thermistor Nominal Resistance at Standard Temperature: 10000(ohm) at 25(c)
NTC_TEMPERATURE_COEFFICIENT	= 3980 	 # Thermistor Temperature Coefficient(beta)

KELVIN_CONVERSION_CONSTANT	= 273.15 # Kelvin Conversion Constant

HEATER_PIN_MAP			= {1:23, 2:24}

PUMP_PIN_MAP			= {1:6, 2:13, 3:26}

VALVE_PIN_MAP			= {1:4, 2:17, 3:27, 4:22, 5:5}

TEMPERATURE_REFRESH_INTERVAL	= 1
