import neopixel
import machine

# Define the pin and number of NeoPixels
pixel_pin = 16
num_pixels = 1

# Initialize the NeoPixel
pixel = neopixel.NeoPixel(machine.Pin(pixel_pin), num_pixels)

def color(r, g, b):
    """Set the NeoPixel to the specified RGB color."""
    pixel[0] = (r, g, b)
    pixel.write()
