#screen
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ST7789

#ADC
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

#pm sensor
from pms5003 import PMS5003, ReadTimeoutError

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

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

#creates the PM sensor object
pms5003 = PMS5003()

#created singe ended inputs on channels 0, 1, 2 for each sensor
sensor0 = AnalogIn(ads, ADS.P0)
sensor1 = AnalogIn(ads, ADS.P1)
sensor2 = AnalogIn(ads, ADS.P2)

while True:
    Data = ["Carbon Dioxide","Value: "+str(sensor0.value),"Gas Levels:","Value: "+str(sensor1.value),"Ozone:","Value: "+str(sensor2.value)] 
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
    draw.rectangle((0,0, 200, 240), (0, 0, 0))
    
    for i in range(0,len(Data)):
        draw.text((text_x, text_y+i*20), Data[i], font=font, fill=(255, 255, 255))
        print(Data[i])
    disp.display(img)
    time.sleep(0.2)

