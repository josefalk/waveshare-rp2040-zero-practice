# oled_display.py

from machine import Pin, I2C
import ssd1306

# Initialize the display once
def init_display(sda_pin=12, scl_pin=13, i2c_freq=400000, i2c_addr=0x3C, width=128, height=64):
    # Set up I2C with GPIO 12 (SDA) and GPIO 13 (SCL)
    i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=i2c_freq)

    # Initialize the display
    oled = ssd1306.SSD1306_I2C(width, height, i2c, addr=i2c_addr)
    
    # Clear the display once during initialization
    oled.fill(0)
    oled.show()
    
    return oled

# Function to update the display text
def display_text(oled, text):
    # Clear the display
    oled.fill(0)

    # Display the provided text
    oled.text(text, 0, 0)

    # Show the updated display
    oled.show()

