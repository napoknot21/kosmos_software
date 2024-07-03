
from smbus import SMBus
import time
import sys
bus = SMBus(1)
address = 0x04              # Arduino I2C Address

state = 1
number_of_revolutions = 10
max_speed = 150
max_accel = 150
pause_time = 5
step_mode = 4

def main():
    i2cData = [state+1, number_of_revolutions, max_speed, max_accel, pause_time, step_mode]             # 1 octet de donnée (soit un entier de 0 à 255)
    bus.write_i2c_block_data(address, 0x00, i2cData)
    time.sleep(1)
    # request data
    while not bus.read_byte(address) :
        time.sleep(0.5)
        print ("Arduino answer to RPi:", bus.read_byte(address))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        gpio.cleanup()
        sys.exit(0)
