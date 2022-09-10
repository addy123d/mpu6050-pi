# Set Sample Rate for your readings.
# It's as easy as you think, just call sample_rate(no_of_samples)

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
mpu.sample_rate(5) #Note: Given range is 3.906 to 8000

while True:

    # Temperature Readings in Celsius
    print(f"Temperature values are {mpu.get_temperature()}")
    
    time.sleep(0.5)
    