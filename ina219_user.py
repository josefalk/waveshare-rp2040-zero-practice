from machine import I2C, Pin
from ina219 import INA219

# Function to initialize INA219 and return current and voltage readings
def read_ina219_data(i2c):
    SHUNT_OHMS = 0.1  # Check the value of your shunt resistor
    
    # Initialize I2C interface (adjust pins according to your setup)
    #i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)
    
    # Initialize INA219 with the I2C interface
    ina = INA219(i2c)
    
    # Get current and voltage readings
    current = ina.current
    voltage = ina.bus_voltage
    
    return current, voltage
