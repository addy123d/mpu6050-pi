
# MPU6050 Official Documentation

![https://hackster.imgix.net/uploads/attachments/1448773/ice_screenshot_20220526-074424_WUTL2Ooslq.png?auto=compress%2Cformat&w=680&h=510&fit=max](https://hackster.imgix.net/uploads/attachments/1448773/ice_screenshot_20220526-074424_WUTL2Ooslq.png?auto=compress%2Cformat&w=680&h=510&fit=max)

Easy to use python package to use MPU-6050. So get out your project setup and dream up some well-balanced projects.

# Example

If address of your MPU6050 is 0x68, this is how you get values of accelerometer and gyroscope readings : 

```python
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
```

## 🌡️ Get Temperature Values:

```python
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

    # Temperature Readings in Celsius
    print(f"Temperature values are {mpu.get_temperature()}")
    
    # Temperature Readings in Fahrenheit
    print(f"Temperature values are {mpu.get_temperature(fahrenheit=True)}")
    
    time.sleep(0.5)
```

# Dependencies

[python-smbus](https://pypi.org/project/smbus/) or [python3-smbus](https://pypi.org/project/smbus/) package, according to your python version.

## Installation

```python
pip install mpu6050-PI
```



# Issues and Bugs 🐛

Please report any issues or bugs here:

[https://github.com/addy123d/MPU6050-raspberrypi/issues](https://github.com/addy123d/MPU6050-raspberrypi/issues)

# License

Copyright (c) 2022 Gagan Deepak (gagan@ineuron.ai), Aditya Chaudhary (adityachaudhary@ineuron.ai) and contributors. Available under the MIT License. For more information, see `LICENSE`.

