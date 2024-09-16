from machine import Pin, PWM, ADC, I2C
from time import sleep
import neopixel_control
from oled_display import init_display, display_text
from ina219_user import read_ina219_data
from battery_utils import get_battery_percentage, i2c

# Set up PWM on GPIO 0
pwm_pin = Pin(0)
pwm = PWM(pwm_pin)

# Set the PWM frequency (50Hz for controlling ESCs)
pwm.freq(50)

# Define the neutral duty cycle value
NEUTRAL_DUTY = 4930
MIN_DUTY = 3278  # Minimum allowed duty cycle
MAX_DUTY = 6556  # Maximum allowed duty cycle

# Set up the button on GPIO 27
button = Pin(27, Pin.IN, Pin.PULL_UP)  # Configure button pin 27 as input with pull-up resistor

# Set up the button on GPIO 27
button2 = Pin(8, Pin.IN, Pin.PULL_UP)  # Configure button pin 27 as input with pull-up resistor

# Set up the potentiometer
potentiometer = ADC(Pin(26))

# Initialize the OLED display once
i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
oled = init_display(128, 64, i2c)

# Store previous values to detect changes
previous_motor_speed = None
previous_current = None
previous_voltage = None
previous_percentage = None

def set_motor_speed(duty_cycle):
    duty_cycle = max(MIN_DUTY, min(MAX_DUTY, duty_cycle))
    print(f"Setting PWM pulse width: {duty_cycle}")  # Debug print
    pwm.duty_u16(duty_cycle)

# Function to update only the motor speed part of the display
def update_motor_speed(oled, motor_speed):
    # Clear only the motor speed line (top line)
    oled.fill_rect(0, 0, oled.width, 10, 0)  # Clear the top 10 pixels (first line)
    oled.text(f"Motor Speed: {motor_speed}", 0, 0)
    oled.show()

# Function to update only the current part of the display
def update_current(oled, current):
    # Clear only the current line (second line)
    oled.fill_rect(0, 10, oled.width, 10, 0)  # Clear the 10-20 pixel range (second line)
    oled.text(f"Current: {current:.2f} mA", 0, 10)
    oled.show()

# Function to update only the voltage part of the display
def update_voltage(oled, voltage):
    # Clear only the current line (second line)
    oled.fill_rect(0, 20, oled.width, 20, 0)  # Clear the 10-20 pixel range (third line)
    oled.text(f"voltage: {voltage:.2f} ", 0, 20)
    oled.show()
    
# Call the get_battery_percentage function
battery_percentage = get_battery_percentage(i2c)

# Function to update only the voltage part of the display
def update_percentage(oled, battery_percentage):
    # Clear only the current line (second line)
    oled.fill_rect(0, 40, oled.width, 40, 0)  # Clear the 10-20 pixel range (third line)
    oled.text(f"Bat.: {battery_percentage:.2f}% ", 0, 40)
    oled.show()
    
def read_potentiometer():
    global previous_motor_speed, previous_current, previous_voltage, previous_percentage
    while True:
        pot_value = potentiometer.read_u16()  # Read ADC value
        
        motor_speed = int(((pot_value / 65535) * 100) - 50)

        if button.value() == 0:
            motor_speed = motor_speed * 2
            motor_speed = max(-100, min(100, motor_speed))
        
        if button2.value() == 0:
            motor_speed = motor_speed * 4
            motor_speed = max(-200, min(200, motor_speed))
        
        if button.value() == 0 and button2.value() == 0:
            motor_speed = motor_speed * 8
            motor_speed = max(-400, min(400, motor_speed))

        # Only update motor speed if it has changed
        if motor_speed != previous_motor_speed:
            update_motor_speed(oled, motor_speed)
            previous_motor_speed = motor_speed

        current, voltage = read_ina219_data(i2c)
        
        # Only update current if it has changed
        if current != previous_current:
            update_current(oled, current)
            previous_current = current

        # Only update voltage if it has changed
        if voltage != previous_voltage:
            update_voltage(oled, voltage)
            previous_voltage = voltage

        # Only update voltage if it has changed
        if battery_percentage != previous_percentage:
            update_percentage(oled, battery_percentage)
            previous_percentage = battery_percentage

        print(f"Motor speed: {motor_speed}, Current: {current:.2f} mA, Voltage: {voltage:.2f} V")
        
        # Adjust duty cycle and motor speed logic here
        if motor_speed == 0:
            duty_cycle = NEUTRAL_DUTY
        elif motor_speed > 0:
            duty_cycle = NEUTRAL_DUTY + motor_speed
            neopixel_control.color(int((motor_speed / 50) * 255), 0, 0)  # Red
        else:
            duty_cycle = NEUTRAL_DUTY + motor_speed
            neopixel_control.color(0, int((abs(motor_speed) / 50) * 255), 0)  # Green
        
        set_motor_speed(duty_cycle)

        # Small delay to prevent flooding the OLED with updates
        sleep(0.1)

# Start reading the potentiometer and controlling the motor
read_potentiometer()
