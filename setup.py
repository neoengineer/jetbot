import glob
import subprocess
from setuptools import setup, find_packages, Extension


def build_libs():
    subprocess.call(['cmake', '.'])
    subprocess.call(['make'])
    

build_libs()

# TEM changed installation requirement from Adafruit_MotorHat to Adafruit-circuitpython-motor
# The MSE version of the jetbot uses the adafruit pwm driver doard rather than the
# motorhat board. The mse_motor.py file now has this new dependency.
setup(
    name='jetbot',
    version='0.4.0',
    description='An open-source robot based on NVIDIA Jetson Nano',
    packages=find_packages(),
    install_requires=[
        'adafruit-circuitpython-pca9685',
        'adafruit-circuitpython-motor',
        'Adafruit-SSD1306',
    ],
    package_data={'jetbot': ['ssd_tensorrt/*.so']},
)

