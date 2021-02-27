#screen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ST7789

import adafruit_dht

#ADC
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#pm sensor
from pms5003 import PMS5003, ReadTimeoutError

import gpiozero

#functions for the ADC sensors
def CO2_function(voltage):
    #calculates value based on formula
    resistance = (5-voltage)/(voltage/200000)
    value = 6.46932/(resistance**1.09) - 0.683384
    value = round(value, 1)
    return (str(value)+" ppm")

def GasLevels_function(voltage):
    #calculates value based on formula
    resistance = (5-voltage)/(voltage/200000)
    value= (22000000/resistance)*100
    value = round(value, 1)
    #turns LED on if CO2 values above a certain value
    if value>120:
        Led.on()
    else:
        Led.off()
    return (str(value)+" %")

def Ozone_function(voltage):
    #calculates value based on formula
    resistance = (5-voltage)/(voltage/200000)
    value=(0.170803 * (resistance**0.543866)) + 0.500254
    value = round(value, 1)
    return (str(value)+" ppm")

#random message
MESSAGE = "HELLO WORLD"

#turn on the MOSFET
MOSFET = gpiozero.LED(4)
MOSFET.on()

Led = gpiozero.LED(21)

#initialise the particulate matter sensor
pms5003 = PMS5003()

#initialise the DHT11
DhtDevice = adafruit_dht.DHT11(board.D17, use_pulseio=False)

# Create ST7735 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,  # BG_SPI_CSB_BACK or BG_SPI_CS_FRONT
    dc=9,
    backlight=19,               # 18 for back BG slot, 19 for front BG slot.
    rotation=90,
    spi_speed_hz=10000000
)

# Initialize display.
disp.begin()
WIDTH = disp.width
HEIGHT = disp.height
img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))
draw = ImageDraw.Draw(img)
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
size_x, size_y = draw.textsize(MESSAGE, font)
text_x = 0
text_y = 0
t_start = time.time()

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

#created singe ended inputs on channels 0, 1, 2 for each sensor
sensor0 = AnalogIn(ads, ADS.P0)
sensor1 = AnalogIn(ads, ADS.P1)
sensor2 = AnalogIn(ads, ADS.P2)

#declares values for DHT11
oldTemp = "Not measured"
oldHum = "Not measured"
old = time.time()

#enters into loop
lottieIsCool = True
while lottieIsCool:#aka forever
    #runs functions to convert readings into part per million values
    CarbonDioxide = CO2_function(sensor0.voltage)
    GasLevels= GasLevels_function(sensor1.voltage)
    Ozone= Ozone_function(sensor2.voltage)
    #adds adc sensor values to the data
    Data = ["Carbon Dioxide",CarbonDioxide,"Gas Levels:",GasLevels,"Ozone:",Ozone] 
    #adds particulate matter readings to data, resets sensor if time out error
    try:
        pm_values = pms5003.read()
        Data.append("PM1.0 ug/m3: "+str(pm_values.pm_ug_per_m3(1)))
        Data.append("PM2.5 ug/m3: "+str(pm_values.pm_ug_per_m3(2.5)))
        Data.append("PM10 ug/m3: "+str(pm_values.pm_ug_per_m3(10)))
        
    except ReadTimeoutError:
        pms5003.reset()
        pm_values = pms5003.read() 
        Data.append("PM1.0 ug/m3: "+str(pm_values.pm_ug_per_m3(1)))
        Data.append("PM2.5 ug/m3: "+str(pm_values.pm_ug_per_m3(2.5)))
        Data.append("PM10 ug/m3: "+str(pm_values.pm_ug_per_m3(10)))

    #adds temperature and humidity to data, adds previous values if it errors
    try:
        Data.append("Temperature:")
        oldTemp = str(DhtDevice.temperature)
        Data.append(oldTemp+" 'C")
        oldHum = str(DhtDevice.humidity)
        Data.append("Humidity "+oldHum+" %")
        old = time.time()
            
    except:
        Data.append(oldTemp+" 'C")
        Data.append("Humidity "+oldHum+" %")

    

    #outputs data to the screen
    draw.rectangle((0,0, 200, 240), (0, 0, 0))
    
    for i in range(0,len(Data)):
        draw.text((text_x, text_y+i*20), Data[i], font=font, fill=(255, 255, 255))
        print(Data[i])
    disp.display(img)
    time.sleep(0.2)
