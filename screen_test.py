from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd

# Creates i2c and lcd objects
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 4, 20)

while True:
    lcd.blink_cursor_on()
    lcd.putstr("Nick's Thermo Bot"+"\n")
    lcd.putstr("Temperature: 24 C")
    sleep(2)
    lcd.clear()
