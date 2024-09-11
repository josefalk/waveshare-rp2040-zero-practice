#motor_control.py
from machine import Pin, PWM
from time import sleep

# Set up PWM on GPIO 0
pwm_pin = Pin(0)
pwm = PWM(pwm_pin)

# Set the PWM frequency (50Hz for controlling ESCs)
pwm.freq(50)

def set_motor_speed(duty_cycle):
    print(f"Setting PWM pulse width: {duty_cycle}")  # Debug print
    pwm.duty_u16(duty_cycle)

def test_motor():
    """
    Simple test sequence for the motor.
    """
    print("Setting motor to neutral (1.5ms pulse)")
    set_motor_speed(4935)  # Neutral position
    sleep(5)
    
