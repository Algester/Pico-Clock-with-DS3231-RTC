#from lib import RTC_DS3231
from lib import ds3231_port
from lib import am2320
import time

import utime

import machine
from ds3231_port import DS3231
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
ds3231 = DS3231(i2c)
sensor = am2320.AM2320(i2c)

#rtc.datetime((MM, DD, YY, wday, hh, mm, ss, 0))
#from this line down before pin is reference to the old RTC library
#if possible attempt to use GPIO 20-22 buttons to configure time rather than set them on the PC first
#Weekday is start at Saturday with x01
#                     sec\min\hou\wee\day\mon\yea
#rtc.DS3231_SetTime(b'\x20\x55\x22\x04\x08\x12\x21')
#remove comment to set time. Do this only once otherwise time will be set everytime the code is executed.

pin = machine.Pin(20, machine.Pin.IN)
#temperature and humidity needs to be converted from float to non float value (unknown formula yet)
temp = sensor.temperature()
humi = sensor.humidity()

#24 hour-12 hour conversion??
#display.hour = rtc.hour % 12
#if display.hour == 0:
#  display.hour = 12
#display.pm = rtc.hour >= 12

while True:
    #Display RTC_ReadTime in mode 2 change as needed see lib/RTC_DS3231
    t = ds3231.get_time()
    #t = rtc.DS3231_ReadTime(2)
    lcd.move_to(0,0)
    lcd.putstr(t)
    time.sleep(1)
    #attempt to use maker pi's built in buttons
    if pin.value() == 0:
        lcd.clear()
        sensor.measure()
        lcd.move_to(0,0)
        lcd.putstr(int(sensor.temperature()))
        lcd.move_to(1,0)
        lcd.putstr(int(sensor.humidity()))
        time.sleep_ms(1000)
