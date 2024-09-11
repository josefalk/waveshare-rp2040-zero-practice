from machine import Pin, PWM, ADC
from time import sleep

# Set up PWM on GPIO 0
pwm_pin = Pin(0)
pwm = PWM(pwm_pin)

# Set the PWM frequency (50Hz for controlling ESCs)
pwm.freq(50)

# Define the neutral duty cycle value
NEUTRAL_DUTY = 4935
MIN_DUTY = 3278  # Minimum allowed duty cycle
MAX_DUTY = 6556  # Maximum allowed duty cycle

def set_motor_speed(duty_cycle):
    # Clamp the duty cycle between the min and max allowed values
    duty_cycle = max(MIN_DUTY, min(MAX_DUTY, duty_cycle))
    print(f"Setting PWM pulse width: {duty_cycle}")  # Debug print
    pwm.duty_u16(duty_cycle)

# Set up ADC on GPIO 26 to read the potentiometer value
potentiometer = ADC(Pin(26))

def read_potentiometer():
    """
    Continuously read the potentiometer, map the value to 0-100, adjust duty cycle.
    If the motor_speed is above 50, increase the duty cycle.
    If the motor_speed is below 50, decrease the duty cycle.
    """
    while True:
        # Read the potentiometer value (0 - 65535)
        pot_value = potentiometer.read_u16()  # Read ADC value
        
        # Map the value from 0-65535 to 0-100
        motor_speed = int((pot_value / 65535) * 100)
        
        # Log the mapped motor speed to the console
        print(f"Motor speed: {motor_speed}")

        # Adjust the duty cycle based on the potentiometer position
        if motor_speed == 50:
            duty_cycle = NEUTRAL_DUTY
        elif motor_speed > 50:
            # Increase duty cycle by 1 for each value above 50
            duty_cycle = NEUTRAL_DUTY + (motor_speed - 50)
        else:
            # Decrease duty cycle by 1 for each value below 50
            duty_cycle = NEUTRAL_DUTY - (50 - motor_speed)
        
        # Set the motor speed with the new duty cycle
        set_motor_speed(duty_cycle)

        # Small delay to prevent flooding the console with too many prints
        sleep(0.1)

# Start reading the potentiometer and controlling the motor
read_potentiometer()

