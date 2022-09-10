#Configure your Accelerometer and Gyroscope Values very easily !

# Mapping of the different gyro and accelero configurations:

# GYRO_CONFIG_[0,1,2,3] range = +- [250, 500,1000,2000] deg/s
#                       sensi =    [131,65.5,32.8,16.4] bit/(deg/s)
#
# ACC_CONFIG_[0,1,2,3] range = +- [2,   4,   8,  16] times the gravity (9.81 m/s^2)
#                      sensi =    [16384,8192,4096,2048] bit/gravity

# Author: Gagan Deepak & Aditya Chaudhary
# License: MIT License (https://opensource.org/licenses/MIT)

from MPU6050 import MPU6050
import time

# Pass your MPU6050 Address
mpu = MPU6050.MPU6050(0x68)

# Init Settings
mpu.reset()
mpu.power_manage()

# If you want to configure gyroscope range values, just pass full scale range values as 250, 500, 1000, 2000
mpu.gyro_config(FULL_SCALE_RANGE=2000)

# If you want to configure accelerometer range values, just pass full scale range values as 2g, 4g, 8g, 16g
mpu.accel_config(FULL_SCALE_RANGE="16g")

while True:
    
    # Gyroscope Readings
    # X Y Z Values: 
    print(f"g values are {mpu.read_gyroscope()}")
    
    # X Values: 
    print(f"g x-values are {mpu.read_gyroscope(GYRO_YOUT=False, GYRO_ZOUT=False)}")
    
    # Y Values: 
    print(f"g y-values are {mpu.read_gyroscope(GYRO_XOUT=False, GYRO_ZOUT=False)}")
    
    # Z Values:
    print(f"g z-values are {mpu.read_gyroscope(GYRO_XOUT=False, GYRO_YOUT=False)}")
    
    # Accelerometer Readings
    print(f"a values are {mpu.read_accelerometer()}")
    
    # X Values: 
    print(f"a x-values are {mpu.read_accelerometer(ACCEL_YOUT=False, ACCEL_ZOUT=False)}")
    
    # Y Values: 
    print(f"a y-values are {mpu.read_accelerometer(ACCEL_XOUT=False, ACCEL_ZOUT=False)}")
    
    # Z Values:
    print(f"a z-values are {mpu.read_accelerometer(ACCEL_XOUT=False, ACCEL_YOUT=False)}")
    
    time.sleep(0.5)
    