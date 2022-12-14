from setuptools import setup, find_packages

def readme():
    with open('Readme.md') as f:
        return f.read()

VERSION = '0.0.3' 
DESCRIPTION = 'Easy to use python package to use MPU-6050. So get out your project setup and dream up some well-balanced projects'

# Setting up
setup(name='mpu6050-PI',
      version='0.0.3',
      description=DESCRIPTION,
      long_description=readme(),
      long_description_type="text/markdown",
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Topic :: Software Development :: Libraries',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Operating System :: POSIX :: Linux',
      ],
      keywords='mpu6050 raspberry python accelerometer gyroscope',
      url='https://github.com/Gagan-REPOSITORIES/sensors/tree/main/MPU6050/RaspberryPi',
      author=['Gagan Deepak','Aditya Chaudhary'],
      author_email='ac3101282@gmail.com',
      license='MIT',
      packages=['MPU6050'],
      zip_safe=False
      )
