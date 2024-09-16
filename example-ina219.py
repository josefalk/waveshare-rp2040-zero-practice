#ina219-user.py
from machine import I2C, Pin
from ina219 import INA219
import time

# Depending on the port, the Pins for SDA and SCL must be specified
# See the MicroPython documentation for your port.
# I2C requires pull-up resistors at SDA and SCL.

I2C_INTERFACE_NO = 1
SHUNT_OHMS = 0.1  # Check value of shunt used with your INA219

i2c = I2C(1, scl=Pin(7), sda=Pin(6))
ina = INA219(i2c)


current = ina.current
voltage = ina.bus_voltage
print("{} mA  {} V".format(current, voltage))
 