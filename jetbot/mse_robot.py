import time 
import traitlets
from traitlets.config.configurable import SingletonConfigurable

from board import SCL, SDA
import busio
# Import the PCA9685 module. Available in the bundle and here:
#   https://github.com/adafruit/Adafruit_CircuitPython_PCA9685
from adafruit_pca9685 import PCA9685

from .mse_motor import Motor
#from jetbot import Motor

class Robot(SingletonConfigurable):
    
    pwm_driver = traitlets.Instance(PCA9685)
    left_motor = traitlets.Instance(Motor)
    right_motor = traitlets.Instance(Motor)

    # config
    left_motor_channel = traitlets.Integer(default_value=0).tag(config=True)
    left_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    right_motor_channel = traitlets.Integer(default_value=1).tag(config=True)
    right_motor_alpha = traitlets.Float(default_value=1.0).tag(config=True)
    
    def __init__(self, *args, **kwargs):
        super(Robot, self).__init__(*args, **kwargs)

        # Create a i2c bus interface, a simple PCA9685 class instance and set the pwn frequency.
        # You can optionally provide a finer tuned reference clock speed to improve the accuracy of the
        # timing pulses. This calibration will be specific to each board and its environment. See the
        # calibration.py example in the PCA9685 driver.
        # pca = PCA9685(i2c, reference_clock_speed=25630710)
        _i2c = busio.I2C(SCL, SDA)
        _pwm_driver = PCA9685(_i2c)
        _pwm_driver.frequency = 50

        self.left_motor = Motor(_pwm_driver, channel=self.left_motor_channel, alpha=self.left_motor_alpha, beta=0.05)
        self.right_motor = Motor(_pwm_driver, channel=self.right_motor_channel, alpha=self.right_motor_alpha, beta=0.05)
        
    def set_motors(self, left_speed, right_speed):
        self.left_motor.value = left_speed
        self.right_motor.value = right_speed
        
    def forward(self, speed=1.0, duration=None):
        self.left_motor.value = speed
        self.right_motor.value = -speed

    def backward(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = speed

    def left(self, speed=1.0):
        self.left_motor.value = -speed
        self.right_motor.value = -speed

    def right(self, speed=1.0):
        self.left_motor.value = speed
        self.right_motor.value = speed

    def stop(self):
        self.left_motor.value = 0.0
        self.right_motor.value = 0.0
