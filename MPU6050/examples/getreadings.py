# Get Accelerometer and Gyroscope Values from your own MPU6050

# Author: Gagan Deepak & Aditya Chaudhary
# License: MIT License (https://opensource.org/licenses/MIT)

from MPU6050 import MPU6050
import time

# Pass your MPU6050 Address
mpu = MPU6050.MPU6050(0x68)

# Init Settings
mpu.reset()
mpu.power_manage()
mpu.gyro_config()
mpu.accel_config()

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
    