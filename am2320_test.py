from lib import am2320
from machine import I2C
import time
i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))
sensor = am2320.AM2320(i2c)
while True:
    sensor.measure()
    print(sensor.temperature())
    print(sensor.humidity())
    time.sleep_ms(4000)