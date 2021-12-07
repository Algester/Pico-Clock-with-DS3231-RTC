from lib import RTC_DS3231
from lib import am2320
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
#i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


#RTC
rtc_i2c= I2C(1, sda=machine.Pin(2), scl=machine.Pin(3), freq=100000)
rtc = RTC_DS3231.RTC(rtc_i2c)

#Humidity and Temperature
sensor_i2c = I2C(0, sda=machine.Pin(4), scl=machine.Pin(5))
sensor = am2320.AM2320(sensor_i2c)

#if possible attempt to use GPIO 20-22 buttons to configure time rather than set them on the PC first
#Weekday is start at Saturday with x01
#                     sec\min\hou\wee\day\mon\yea
#rtc.DS3231_SetTime(b'\x50\x40\x16\x04\x07\x12\x21')
#remove comment to set time. Do this only once otherwise time will be set everytime the code is executed.

while True:
    t = rtc.DS3231_ReadTime(1)
    temp = sensor.temperatur()
    humi = sensor.humidity()
    #read RTC and receive data in Mode 1 (see /my_lib/RTC_DS3231.py)
    lcd.move_to(0,0)
    lcd.putstr(t)
    time.sleep(1)
    #attempt to use maker pi's built in buttons
    if machine.Pin(20, machine.Pin.OUT):
        sensor.measure()
        lcd.clear()
        lcd.move_to(0,0)
        lcd.putstr(temp)
        lcd.move_to(1,0)
        lcd.putstr(humi)
        time.sleep_ms(30)


