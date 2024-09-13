# i2cscan.py
# Scanner i2c en MicroPython | MicroPython i2c scanner

from oled_display import display_text
import machine
i2c = machine.I2C(0, scl=machine.Pin(13), sda=machine.Pin(12))

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
    
