# oled_display.py

from machine import Pin, I2C
import ssd1306

# Initialize the display once
def init_display(w, h, i2c):
    # Set up I2C with GPIO 12 (SDA) and GPIO 13 (SCL)
    #i2c = I2C(1, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=i2c_freq)
    #i2c = I2C(1, sda=Pin(6), scl=Pin(7), freq=400000)


    # Initialize the display
    oled = ssd1306.SSD1306_I2C(w, h, i2c)
    
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