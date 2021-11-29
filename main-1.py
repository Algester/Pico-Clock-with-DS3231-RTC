from lib import RTC_DS3231
import time

import utime

import machine
from machine import I2C
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

#RTC
rtc = RTC_DS3231.RTC()

#Weekday is start at Saturday with x01
#                     sec\min\hou\wee\day\mon\yea
rtc.DS3231_SetTime(b'\x50\x47\x05\x03\x29\x11\x21')
#remove comment to set time. Do this only once otherwise time will be set everytime the code is executed.

while True:
    t = rtc.DS3231_ReadTime(1)
    #read RTC and receive data in Mode 1 (see /my_lib/RTC_DS3231.py)
    lcd.move_to(0,0)
    lcd.putstr(t)
    time.sleep(1)

