from machine import Pin, PWM
import time
import utime
import neopixel

# Define the pin and number of NeoPixels
pixel_pin = 16
num_pixels = 1

# Initialize the NeoPixel
pixel = neopixel.NeoPixel(machine.Pin(pixel_pin), num_pixels)

while True:
    # Turn the NeoPixel on (Red color)
    pixel[0] = (255, 0, 0)
    pixel.write()
    utime.sleep(1)  # Delay for 1 second

    # Turn the NeoPixel off
    pixel[0] = (0, 0, 0)
    pixel.write()
    utime.sleep(1)  # Delay for 1 second

# Define pins
AIN1 = Pin(2, Pin.OUT)
AIN2 = Pin(3, Pin.OUT)
PWMA = PWM(Pin(4))
PWMA.freq(1000)  # Set frequency to 1 kHz

# Function to control motor direction and speed
def motor_control(direction, speed):
    if direction == 'forward':
        AIN1.value(1)
        AIN2.value(0)
    elif direction == 'backward':
        AIN1.value(0)
        AIN2.value(1)
    else:
        AIN1.value(0)
        AIN2.value(0)
    
    PWMA.duty_u16(int(speed * 65535))  # Set speed (0.0 to 1.0)

# Main loop
try:
    while True:
        motor_control('forward', 0.5)  # Run motor forward at 50% speed
        time.sleep(2)
        motor_control('backward', 0.5)  # Run motor backward at 50% speed
        time.sleep(2)
        motor_control('stop', 0)  # Stop the motor
        time.sleep(2)
except KeyboardInterrupt:
    motor_control('stop', 0)  # Stop the motor when exiting

