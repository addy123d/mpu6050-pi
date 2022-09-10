"""Register set of MPU6050"""

# The MIT License (MIT)
# Copyright (c) 2022 Gagan Deepak and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class MPURegisters:
	"""
	Register access of MPU6050
	"""
	
	ADDRESS_DEFAULT = 0x68 #address of MPU6050 when AD0 pin is LOW default condition
	ADDRESS_AD0_HIGH = 0x69 #address of MPU6050 when AD0 pin is HIGH
	

	PWR_MGMT_1 = 0x6B #power management register
	SMPRT_DIV = 0x19 #sample rate divider register
	CONFIG = 0x1A #configuration register
 	
	TEMP_OUT = 0x41 #Temperature Measurement Register
	GYRO_CONFIG = 0x1B # configure gyroscope
	ACCEL_CONFIG = 0x1C # configure accelerometer
	ACCEL_XOUT_H = 0x3B # starting address of accelerometer data
	GYRO_XOUT_H = 0x43 #starting address of gyroscope data