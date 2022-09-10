# Disable Temperature Sensor

# Author: Gagan Deepak & Aditya Chaudhary
# License: MIT License (https://opensource.org/licenses/MIT)


from MPU6050 import MPU6050
import time

# Pass your MPU6050 Address
mpu = MPU6050.MPU6050(0x68)

# Init Settings
mpu.reset()
mpu.power_manage(temp_sense_disable=True) #Setting it to True disables the temperature sensor
mpu.gyro_config()
mpu.accel_config()

while True:

    # Temperature Readings in Celsius
    print(f"Temperature values are {mpu.get_temperature()}") #You will notice that temperature values will be 0
    
    time.sleep(0.5)
    