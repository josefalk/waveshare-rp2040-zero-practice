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

