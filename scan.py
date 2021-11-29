import machine
#change the pins as needed by your needs
sda = machine.Pin(2)
scl = machine.Pin(3)
#change machine.I2C(1,sda=sda, scl=scl, freq=400000) as needed by your pico pin SDA and SCL pin out IE 0 or 1
i2c = machine.I2C(1,sda=sda, scl=scl, freq=400000)
print(i2c.scan())
