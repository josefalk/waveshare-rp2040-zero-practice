from ina219_user import read_ina219_data
from machine import I2C, Pin

# Define the voltage thresholds for a 3S LiPo battery
FULL_BATTERY_VOLTAGE = 12.6  # 4.2V per cell, 12.6V for a 3S battery
MIN_BATTERY_VOLTAGE = 9.6    # 3.2V per cell, 9.6V for a 3S battery

# Initialize the I2C bus
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)

# Function to read the voltage and calculate battery percentage
def get_battery_percentage(i2c):
    # Get the voltage from INA219 using the read_ina219_data function
    _, voltage = read_ina219_data(i2c)

    # Calculate the battery percentage based on voltage
    if voltage >= FULL_BATTERY_VOLTAGE:
        battery_percentage = 100  # Fully charged
    elif voltage <= MIN_BATTERY_VOLTAGE:
        battery_percentage = 0    # Minimum safe voltage
    else:
        # Linear calculation of percentage
        battery_percentage = ((voltage - MIN_BATTERY_VOLTAGE) / 
                              (FULL_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE)) * 100
        battery_percentage = int(battery_percentage)

    # Print the voltage and battery percentage
    print(f"Voltage: {voltage:.2f} V, Battery Percentage: {battery_percentage}%")
    
    return battery_percentage
