# Scanner i2c en MicroPython | MicroPython i2c scanner
from machine import Pin, I2C

i2c = I2C(1, scl=Pin(7), sda=Pin(6), freq=100000)

print('Scan i2c bus...')
devices = i2c.scan()

if len(devices) == 0:
  print("No i2c device !")
else:
    
  print('i2c devices found:',len(devices))

  for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
    