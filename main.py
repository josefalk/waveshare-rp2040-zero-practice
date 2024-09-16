#main.py
import motor_control
import oled_display
from machine import I2C, Pin
from ina219_user import read_ina219_data
from oled_display import init_display, display_text


i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)

current, voltage = read_ina219_data(i2c)
print("{} mA  {} V".format(current, voltage))


oled = init_display(128, 64, i2c)


oled.fill_rect(0, 10, oled.width, 10, 0)  # Clear the 10-20 pixel range (second line)
oled.text(f"tesssssssssssssttttttt", 0, 10)
oled.show()
