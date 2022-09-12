"""MPU6050 Interface with RaspberryPi I2C port"""

# The MIT License (MIT)
# Copyright (c) 2022 Gagan Deepak, Aditya Chaudhary and contributors
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

from .Registers import MPURegisters as mpu6050
from smbus import SMBus
import time

Debug = False  


class MPU6050:
    """
    MPU6050 GY-521 Interface with RaspberryPi
    """

    def __init__(self, address, bus=1):
        # Init parameters
        self.address = address
        self.bus = SMBus(bus)
        self.ACCEL_SCALE_MODIFIER = 16384.0
        self.GYRO_SCALE_MODIFIER = 131.0
        self.GRAVITIY_MS2 = 9.80665

        '''
        Initial Conditions:
        WRITE DATA on MPU6050_PWR_MGMT_1
        By setting 0x01 means , it is 00000 001, we have to focus on last three bits.
        Device Reset Bit is set to 0.
        Sleep Bit is set to 0.
        CYCLE Bit is set to 0.
        TEMP_DIS is set to 0, as it enables the temperature sensor by default.
        CLKSEL Bit is 001, that means we are going with 1, PLL with X axis gyroscopic reference.
        '''
        self.power_manage(clock_source=1)
        self.sample_rate()  # freqency divide by 1
        self.configuration(Dig_low_pass_filter=1)  # frequency = 1khz
        self.gyro_config()
        self.accel_config()

    def power_manage(self, reset: bool = False, sleep: bool = False, cycle: bool = False,
                    temp_sense_disable: bool = False, clock_source: int = 0, value: int = 0):
        '''
        Sets the PWR_MGMT_1 register of MPU6050

        :param reset: True = resets all internal registers to their default values
        :type reset: bool
        :param sleep: True = puts the MPU-6050 into sleep mode
        :type sleep: bool
        :param cycle: True = MPU-6050 will cycle between sleep mode and waking up
        :type cycle: bool
        :param temp_sense_disable: True = disables the temperature sensor
        :type temp_sense_disable: bool
        :param clock_source: Specifies the clock source of the device
        :type clock_source: int 3-bit unsigned value
        :param value: The value to set the PWR_MGMT_1 register to
        :type value: int 8-bit unsigned value
        '''

        if value != 0:
            self.bus.write_byte_data(
                mpu6050.ADDRESS_DEFAULT, mpu6050.PWR_MGMT_1, value)
        else:
            # @gagan bug fix
            # byte = self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT,mpu6050.PWR_MGMT_1)
            value = (reset*128 + sleep*64 + cycle*32 +
                     temp_sense_disable*8 + clock_source)  # | byte
            self.bus.write_byte_data(
                mpu6050.ADDRESS_DEFAULT, mpu6050.PWR_MGMT_1, value)

    '''
    Method to calculate value from multiple registers
    For example we have TEMP_OUT_H and TEMP_OUT_L , 0x41 and 0x42, to calculate temperature
    '''

    def read_i2c_byte_data(self, register):
        '''
        Read two i2c registers and combine them,
        :param register:address to read two bytes from
        :type register:int
        :return: int data(address+address+1)
        '''

        HIGH = self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, register)
        LOW = self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, register + 1)

        # Calculation
        result_value = (HIGH << 8) + LOW

        if (result_value >= 0x8000):
            return -((65535 - result_value) + 1)
        else:
            return result_value

    def get_temperature(self, fahrenheit: bool = False):
        """
        Reads the temperature from the temperature sensor on MPU-6050.
        :param fahrenheit:True returns the tempature in fahrenheit
        :return: Temperature in Fahrenheit or celsius
        """

        temp_register_value = self.read_i2c_byte_data(mpu6050.TEMP_OUT)

        # Formula to compute the temp register value to temperature in degree celsius
        # Temperature in degree celsius = (TEMP_OUT Register Value as a signed quantity)/340 + 36.53
        temperature_value = (temp_register_value/340) + 36.53

        if (fahrenheit):
            # In Fahrenheit
            # Conversion (0°C × 9/5) + 32 = 32°F
            fahrenheit_value = (temperature_value * (9/5)) + 32
            return "%.2f" % fahrenheit_value
        

        else:
            # In Celsius
            return "%.2f" % temperature_value

    def reset(self):
        """
            Resets the whole MPU6050.

            Reset Value for all registers is 0x00 ,
            but MPU6050_PWR_MGMT_1 will be 0x40 and WHO_AM_I will be 0x68
        """

        self.power_manage(reset=True)
        print("Device Resetting...") if Debug else None
        time.sleep(0.01)

    def sample_rate(self, value: int = 1000):
        '''
        Update : Just provide number of samples you want in range 3.906 to 8000
        WRITE DATA on MPU6050_SMPRT_DIV
        By setting 0x00 means, it is 00000000, it is a 8 bit unsigned value.
        Formula : Sample Rate = Gyroscope_Output_Rate/(1 + MPU6050_SMPLRT_DIV)
        initially we are turning off digital low pass filter (DLPF = 000 or 111), therefore Gyroscope_Output_Rate = 8Khz
        We will get maximum samples through this.
        :param value: sampling rate
        :type value: int 8-bit unsigned value
        '''

        '''
        Update @addy123d:
        we can take number of samples from user.
        Formula : SMPRT_DIV = (Gyroscopic_Output_Rate/Number_Of_Samples) - 1
        Initial Conditions we are turning off digital low pass filter (DLPF = 000 or 111), therefore Gyroscope_Output_Rate = 8Khz
        '''

        number_of_samples = value

        # Range For Samples , max = 8000 and min = 3.906

        if (number_of_samples >= 3.906 and number_of_samples <= 8000):
            
            if(number_of_samples > 1000):
                self.configuration(Dig_low_pass_filter=0)
            else:
                self.configuration(Dig_low_pass_filter=1)

            value = (8000/number_of_samples) - 1
            self.bus.write_byte_data(mpu6050.ADDRESS_DEFAULT, mpu6050.SMPRT_DIV, int(value))
            
        else:
            # Generate OUT OF RANGE Error
            print("ERROR: SAMPLES ARE OUT OF RANGE, Range is between 3.906 and 8000 samples")


    def configuration(self, ext_sync: int = 0, Dig_low_pass_filter: int = 0, value: int = 0):
        '''
        WRITE DATA on MPU6050_CONFIG
        We will set it to 0x00, as we are not using DLPF and EXT_SYNC_SET, and we are keeping as low or 0.
        :param ext_sync: Configures the FSYNC pin sampling
        :type ext_sync: int 3-bit unsigned value
        :param Dig_low_pass_filter: Configures the DLPF setting
        :type Dig_low_pass_filter: int 3-bit unsigned value
        :param value: configuration value
        :type value: int 6-bit unsigned value
        '''
        if value == 0:
            value = (ext_sync << 3) | Dig_low_pass_filter

        self.bus.write_byte_data(mpu6050.ADDRESS_DEFAULT, mpu6050.CONFIG, value)
        

    def gyro_config(self, XG_ST: bool = False, YG_ST: bool = False, ZG_ST: bool = False, FULL_SCALE_RANGE: int = 250, value: int = 0):
        """This register is used to trigger gyroscope self-test and configure the gyroscopes full scale range.
        :param XG_ST: True = Setting this bit causes the X axis gyroscope to perform self test
        :type XG_ST: bool
        :param YG_ST: True = Setting this bit causes the Y axis gyroscope to perform self test
        :type YG_ST: bool
        :param ZG_ST: True = Setting this bit causes the Z axis gyroscope to perform self test
        :type ZG_ST: bool
        :param Full_Scale_Range : Selects the full scale range of gyroscopes
        :type Full_Scale_Range: int 2-bit unsigned value
        """
        
        '''
        update @addy123d:
        Now you can pass default values mentioned: 250, 500, 1000, 2000 degrees/second
        '''
        # Create a dictionary
        # Full Scale Range Selector
        scale_range = {
            250 : 0,
            500 : 1,
            1000 : 2,
            2000 : 3
        }
        
        self.GYRO_SCALE_MODIFIER = 32768/FULL_SCALE_RANGE
        
        if value == 0:
            value = XG_ST*128 + YG_ST*64 + ZG_ST*32 + (scale_range[FULL_SCALE_RANGE] <<3) | 0

        self.bus.write_byte_data(mpu6050.ADDRESS_DEFAULT, mpu6050.GYRO_CONFIG, value)

    def accel_config(self, XA_ST: bool = False, YA_ST: bool = False,ZA_ST: bool = False,FULL_SCALE_RANGE: str = "2g",value: int = 0):
        """This register is used to trigger accel self-test and configure the accel scopes full scale range.
        :param XA_ST: True = Setting this bit causes the X axis accel to perform self test
        :type XA_ST: bool
        :param YA_ST: True = Setting this bit causes the Y axis accel to perform self test
        :type YA_ST: bool
        :param ZA_ST: True = Setting this bit causes the Z axis accel to perform self test
        :type ZA_ST: bool
        :param FULL_SCALE_RANGE : Selects the full scale range of accelerometer
        :type FULL_SCALE_Range: int 2-bit unsigned value
        """
        
        '''
        update @addy123d:
        Now you can pass default values mentioned: 2g, 4g, 8g, 16g directly
        '''
        
        # Create a dictionary
        # Full Range Selector
        scale_range = {    #@aditya bug fix
            "2g" : 0,
            "4g" : 1,
            "8g" : 2,
            "16g" : 3
        }
        
        #update @addy123d, seperate 2 from string '2g'.
        self.ACCEL_SCALE_MODIFIER = 32768/int(FULL_SCALE_RANGE[:-1])
      
        
        if value == 0:
            value = XA_ST*128 + YA_ST*64 + ZA_ST*32 + (scale_range[FULL_SCALE_RANGE] <<3) | 0
            
        self.bus.write_byte_data(mpu6050.ADDRESS_DEFAULT, mpu6050.ACCEL_CONFIG, value)

    def read_accelerometer(self, ACCEL_XOUT: bool = True, ACCEL_YOUT: bool = True, ACCEL_ZOUT: bool = True, gravity: bool = False):
        """
        Fetches Recent accelerometer values
        """
        ACCEL_XOUT_data = 0
        ACCEL_YOUT_data = 0
        ACCEL_ZOUT_data = 0
        
        if ACCEL_XOUT:
            ACCEL_XOUT_data = self.read_i2c_byte_data(mpu6050.ACCEL_XOUT_H)

        if ACCEL_YOUT:
            ACCEL_YOUT_data = self.read_i2c_byte_data(mpu6050.ACCEL_XOUT_H+2)

        if ACCEL_ZOUT:
            ACCEL_ZOUT_data = self.read_i2c_byte_data(mpu6050.ACCEL_XOUT_H+4)
            
            
        ACCEL_XOUT_data = ACCEL_XOUT_data / self.ACCEL_SCALE_MODIFIER
        ACCEL_YOUT_data = ACCEL_YOUT_data / self.ACCEL_SCALE_MODIFIER
        ACCEL_ZOUT_data = ACCEL_ZOUT_data / self.ACCEL_SCALE_MODIFIER
        
        if gravity == False: #@aditya bug fix, basically we will provide values in m/s^2
            ACCEL_XOUT_data = ACCEL_XOUT_data * self.GRAVITIY_MS2
            ACCEL_YOUT_data = ACCEL_YOUT_data * self.GRAVITIY_MS2
            ACCEL_ZOUT_data = ACCEL_ZOUT_data * self.GRAVITIY_MS2


        return {'x': ACCEL_XOUT_data, 'y': ACCEL_YOUT_data, 'z': ACCEL_ZOUT_data}

    def read_gyroscope(self, GYRO_XOUT: bool = True, GYRO_YOUT: bool = True, GYRO_ZOUT: bool = True):
        """
        Fetches Recent gyroscope values
        """
        GYRO_XOUT_data = 0
        GYRO_YOUT_data = 0
        GYRO_ZOUT_data = 0
        
        
        if GYRO_XOUT:
            GYRO_XOUT_data = self.read_i2c_byte_data(mpu6050.GYRO_XOUT_H)
        if GYRO_YOUT:
            GYRO_YOUT_data = self.read_i2c_byte_data(mpu6050.GYRO_XOUT_H+2)
        if GYRO_ZOUT:
            GYRO_ZOUT_data = self.read_i2c_byte_data(mpu6050.GYRO_XOUT_H+4)
            
            
        GYRO_XOUT_data = GYRO_XOUT_data / self.GYRO_SCALE_MODIFIER
        GYRO_YOUT_data = GYRO_YOUT_data / self.GYRO_SCALE_MODIFIER
        GYRO_ZOUT_data = GYRO_ZOUT_data / self.GYRO_SCALE_MODIFIER

        return {'x': GYRO_XOUT_data, 'y': GYRO_YOUT_data, 'z': GYRO_ZOUT_data}

    def self_test(self):
        """
        Self test of MPU6050
        """
        gyro_result = self.self_test_gyroscope()
        accel_result = self.self_test_accelerometer()

        return gyro_result, accel_result

    def self_test_accelerometer(self):
        '''
        Self Testing accelerometer for checking difference between factory trim values vs actuals
        '''
        value_without_self_test = self.read_accelerometer()
        self.accel_config(value=0xF0)
        value_with_self_test = self.read_accelerometer()
        # getting last 5 bits
        XA_TEST = ((self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x0D) & 0xE0) >> 3) | ((self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x10) >> 4) & 0x03)
        YA_TEST = ((self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x0E) & 0xE0) >> 3) | ((self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x10) >> 2) & 0x03)
        ZA_TEST = ((self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x0F) & 0xE0) >> 3) | ((self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x10) >> 0) & 0x03)

        self_test_response = value_with_self_test['x'] - \
            value_without_self_test['x']
        factory_trim_value = self.get_accel_ft_value(XA_TEST)
        diff_x = (self_test_response-factory_trim_value)/factory_trim_value

        self_test_response = value_with_self_test['y'] - \
            value_without_self_test['y']
        factory_trim_value = self.get_accel_ft_value(YA_TEST)
        diff_y = (self_test_response-factory_trim_value)/factory_trim_value

        self_test_response = value_with_self_test['z'] - \
            value_without_self_test['z']
        factory_trim_value = self.get_accel_ft_value(ZA_TEST)
        diff_z = (self_test_response-factory_trim_value)/factory_trim_value

        return {'diff_x': diff_x, 'diff_y': diff_y, 'diff_z': diff_z}

    def self_test_gyroscope(self):
        """
        Self Testing gyroscope for checking difference between factory trim values vs actuals
        """
        value_without_self_test = self.read_gyroscope()
        self.gyro_config(value=0xE0)
        value_with_self_test = self.read_gyroscope()
        # getting last 5 bits
        XG_TEST = self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x0D) & 0x1F
        YG_TEST = self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x0E) & 0x1F
        ZG_TEST = self.bus.read_byte_data(mpu6050.ADDRESS_DEFAULT, 0x0F) & 0x1F

        self_test_response = value_with_self_test['x'] - \
            value_without_self_test['x']
        factory_trim_value = self.get_gyro_ft_value(XG_TEST)
        diff_x = (self_test_response-factory_trim_value)/factory_trim_value

        self_test_response = value_with_self_test['y'] - \
            value_without_self_test['y']
        factory_trim_value = -self.get_gyro_ft_value(YG_TEST)
        diff_y = (self_test_response-factory_trim_value)/factory_trim_value

        self_test_response = value_with_self_test['z'] - \
            value_without_self_test['z']
        factory_trim_value = self.get_gyro_ft_value(ZG_TEST)
        diff_z = (self_test_response-factory_trim_value)/factory_trim_value

        return {'diff_x': diff_x, 'diff_y': diff_y, 'diff_z': diff_z}

    def get_gyro_ft_value(self, value=0):
        """
        finds the ft value of the gyroscope
        """
        return 25*131*pow(1.046, value-1)

    def get_accel_ft_value(self, value=0):
        """
        finds the ft value of the accel
        """
        return (4096*0.34*pow(0.92, ((value-1)/30)))/0.34
