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
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
rtc = RTC_DS3231.RTC()
sensor = am2320.AM2320(i2c)

#if possible attempt to use GPIO 20-22 buttons to configure time rather than set them on the PC first
#Weekday is start at Saturday with x01
#                     sec\min\hou\wee\day\mon\yea
#rtc.DS3231_SetTime(b'\x20\x55\x22\x04\x08\x12\x21')
#remove comment to set time. Do this only once otherwise time will be set everytime the code is executed.

pin = machine.Pin(20, machine.Pin.IN)
#temperature and humidity needs to be converted from float to non float value (unknown formula yet)
#temp = sensor.temperature()
#humi = sensor.humidity()

while True:
    #Display RTC_ReadTime in mode 2 change as needed see lib/RTC_DS3231
    t = rtc.DS3231_ReadTime(2)
    lcd.move_to(0,0)
    lcd.putstr(t)
    time.sleep(1)
    #attempt to use maker pi's built in buttons
    if pin.value() == 0:
        lcd.clear()
        sensor.measure()
        lcd.move_to(0,0)
        #lcd.putstr(f'sensor.temperature()')
        lcd.move_to(1,0)
        #lcd.putstr(f'sensor.humidity()')
        time.sleep_ms(1000)
