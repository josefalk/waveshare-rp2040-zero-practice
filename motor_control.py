# motor_control.py
from machine import Pin, PWM, ADC, I2C
from time import sleep
import neopixel_control
from oled_display import init_display, display_text

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
oled = init_display(sda_pin=12, scl_pin=13)

def set_motor_speed(duty_cycle):
    # Clamp the duty cycle between the min and max allowed values
    duty_cycle = max(MIN_DUTY, min(MAX_DUTY, duty_cycle))
    print(f"Setting PWM pulse width: {duty_cycle}")  # Debug print
    pwm.duty_u16(duty_cycle)

def read_potentiometer():
    """
    Continuously read the potentiometer, map the value to -50 to 50, adjust duty cycle.
    If the motor_speed is greater than 0, increase the duty cycle and map color range accordingly.
    """
    while True:
        # Read the potentiometer value (0 - 65535)
        pot_value = potentiometer.read_u16()  # Read ADC value
        
        # Map the value from 0-65535 to -50 to 50
        motor_speed = int(((pot_value / 65535) * 100) - 50)
        
        # Check if the button is pressed (button is active-low, meaning it reads 0 when pressed)
        if button.value() == 0:
            # Double the motor speed
            motor_speed = motor_speed * 2
            # Ensure the motor_speed does not exceed 100 or -100
            motor_speed = max(-100, min(100, motor_speed))
            
        if button2.value() == 0:
            # Double the motor speed
            motor_speed = motor_speed * 4
            # Ensure the motor_speed does not exceed 100 or -100
            motor_speed = max(-200, min(200, motor_speed))
            
        # Check if both buttons are pressed
        if button.value() == 0 and button2.value() == 0:
            # If both buttons are pressed, apply the combined effect
            motor_speed = motor_speed * 8
            # Ensure the motor_speed does not exceed -200 to 200 range
            motor_speed = max(-400, min(400, motor_speed))

    
        # Update the OLED display with motor speed (using the same initialized OLED object)
        display_text(oled, f"Motor Speed: {motor_speed}")

        # Only map the color range if motor_speed is greater than 0
        if motor_speed > 0:
            # Map motor_speed (0 to 50) to color_range (0 to 255)
            color_range = int((motor_speed / 50) * 255)
        else:
            # Map motor_speed (-50 to 0) to color_range (0 to 255, using the green channel)
            color_range = int(((motor_speed *-1) / 50) * 255)

        # If the button is pressed, divide the color range by 2
        if button.value() == 0:
            color_range = int(color_range / 2)
            
        # Log the motor speed and color range to the console
        print(f"Motor speed: {motor_speed}, Pot Value: {pot_value}, Color Range: {color_range}")
        
        if button.value() == 0 and button2.value() == 0:
            color_range = int(color_range / 8)
            
        # Adjust the duty cycle based on the potentiometer position
        if motor_speed == 0:
            duty_cycle = NEUTRAL_DUTY
        elif motor_speed > 0:
            # Increase duty cycle for positive motor speeds
            duty_cycle = NEUTRAL_DUTY + motor_speed
            
            # Turn the NeoPixel on with a red color based on speed
            neopixel_control.color(color_range, 0, 0)  # Set NeoPixel to red
        else:
            # Decrease duty cycle for negative motor speeds
            duty_cycle = NEUTRAL_DUTY + motor_speed  # Use negative motor_speed to reduce duty cycle
            
            # Turn the NeoPixel on with a green color based on reverse speed
            neopixel_control.color(0, color_range, 0)  # Set NeoPixel to green
        
        # Set the motor speed with the new duty cycle
        set_motor_speed(duty_cycle)

        # Small delay to prevent flooding the console with too many prints
        sleep(0.1)

# Start reading the potentiometer and controlling the motor
read_potentiometer()

