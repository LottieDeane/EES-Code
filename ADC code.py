import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
#ads = ADS.ADS1115(i2c, address=0x48)

# Create single-ended input on channel 0
sensor0 = AnalogIn(ads, ADS.P0)
sensor1 = AnalogIn(ads, ADS.P1)
sensor2 = AnalogIn(ads, ADS.P2)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format("raw", "v"))

while True:
    print("{:>5}\t{:>5.3f}".format(sensor0.value,sensor0.voltage))
    print("{:>5}\t{:>5.3f}".format(sensor1.value,sensor1.voltage))
    print("{:>5}\t{:>5.3f}".format(sensor2.value,sensor2.voltage))
    time.sleep(0.5)
