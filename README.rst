mpu6050
=======

|badge_license| |pypi_version| |pypi_downloads|

A Python module for accessing the MPU-6050 digital accelerometer and gyroscope on a Raspberry Pi.

Example
-------

Assuming that the address of your MPU-6050 is 0x68, you can read read accelerometer data like this:

::

    >>> from MPU6050 import MPU6050

    >>> mpu = MPU6050.mpu6050(0x68)

    >>> mpu.reset()

    >>> mpu.power_manage()

    >>> mpu.gyro_config()

    >>> mpu.accel_config()

    >>> while True:

    >>>     gyroscope_data = mpu.read_gyroscope()

    >>>     accelerometer_data = mpu.read_accelerometer()

Dependencies
------------

Either the ``python-smbus`` or ``python3-smbus`` package, according to your
Python version.

Installation
------------

There are two ways of installing this package: via PyPi or via the git repository.
Installing from the git repository insures that you have the absolute latest
version installed, but this can be prone to bugs.

1. install the python-smbus package
::

    sudo apt install python3-smbus

2a. Install this package from PyPi repository
::

    pip install mpu6050-PI

Or:

2b. Clone the repository and run setup.py
::
    
    git clone https://github.com/addy123d/mpu6050-pi.git
    python setup.py install

Issues & Bugs
-------------

Please report any issues or bugs here:

    https://github.com/addy123d/mpu6050-pi/issues


License
-------

Copyright (c) 2022 Gagan Deepak (gagan@ineuron.ai), Aditya Chaudhary (adityachaudhary@ineuron.ai) and contributors.
Available under the MIT License. For more information, see ``LICENSE``.

.. |pypi_version| image:: https://img.shields.io/pypi/v/mpu6050-raspberrypi.svg
    :alt: latest PyPI version
    :target: https://pypi.org/project/mpu6050-raspberrypi/

.. |pypi_downloads| image:: https://img.shields.io/pypi/dm/mpu6050-raspberrypi
    :alt: PyPI download count
    :target: https://pypi.org/project/mpu6050-raspberrypi/

.. |badge_license| image:: https://img.shields.io/github/license/m-rtijn/mpu6050
    :alt: license: MIT
    :target: https://github.com/m-rtijn/mpu6050/blob/master/LICENSE
