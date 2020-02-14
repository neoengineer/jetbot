import atexit

from adafruit_motor import servo

import traitlets
from traitlets.config.configurable import Configurable


class Motor(Configurable):

    value = traitlets.Float()
    
    # config
    alpha = traitlets.Float(default_value=1.0).tag(config=True)
    beta = traitlets.Float(default_value=0.0).tag(config=True)

    def __init__(self, driver, channel, *args, **kwargs):
        super(Motor, self).__init__(*args, **kwargs)  # initializes traitlets

        self._driver = driver
        self._motor = servo.ContinuousServo(self._driver.channels[channel])
        # The pulse range is 750 - 2250 by default.
        # If your servo doesn't stop once the script is finished you may need to tune the
        # reference_clock_speed above or the min_pulse and max_pulse timings below.
        # servo7 = servo.ContinuousServo(pca.channels[7], min_pulse=750, max_pulse=2250)

        atexit.register(self._release)
        
    @traitlets.observe('value')
    def _observe_value(self, change):
        self._write_value(change['new'])

    def _write_value(self, value):
        
        """Sets throttle value between [-1, 1]"""
        mapped_value = self.alpha * value + self.beta
        tuned_throttle = min(max(mapped_value, -1), 1) # ensure throttle speed is between -1, 1 after alpha and beta are applied 
        self._motor.throttle = tuned_throttle
        # print("Setting throttle to = %f" % tuned_throttle)
        
    def _release(self):
        """Stops motor by releasing control"""
        self._driver.deinit()


