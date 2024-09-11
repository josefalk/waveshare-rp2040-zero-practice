# neopixel_control.py

import machine
import neopixel
import time

# Define the pin where the NeoPixel is connected and the number of NeoPixels
NEO_PIN = 16  # Change this if the NeoPixel is on another pin
NUM_PIXELS = 1  # Adjust this if there are more NeoPixels

# Initialize NeoPixel object
np = neopixel.NeoPixel(machine.Pin(NEO_PIN), NUM_PIXELS)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition of red - green - blue.
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)

def color_change(speed=10):
    # Loops through colors and gradually changes the NeoPixel color
    while True:
        for i in range(255):
            np[0] = wheel(i)
            np.write()
            time.sleep_ms(speed)

def turn_off():
    # Function to turn off the NeoPixel
    np[0] = (0, 0, 0)
    np.write()

