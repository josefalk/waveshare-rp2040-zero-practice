#main.py
import motor_control
import neopixel_control

# Run the motor test sequence
motor_control.test_motor()


try:
    # Start the color change function with a specified speed
    neopixel_control.color_change(speed=20)
except KeyboardInterrupt:
    # Turn off NeoPixel when the program is interrupted
    neopixel_control.turn_off()
