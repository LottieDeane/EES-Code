import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

#created singe ended inputs on channels 0, 1, 2 for each sensor
sensor0 = AnalogIn(ads, ADS.P0)
sensor1 = AnalogIn(ads, ADS.P1)
sensor2 = AnalogIn(ads, ADS.P2)

print("{:>5}\t{:>5}".format("raw", "v"))

while True:
    print("{:>5}\t{:>5.3f}".format(sensor0.value,sensor0.voltage))
    print("{:>5}\t{:>5.3f}".format(sensor1.value,sensor1.voltage))
    print("{:>5}\t{:>5.3f}".format(sensor2.value,sensor2.voltage))
    time.sleep(0.5)
