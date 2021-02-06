from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import time

import ST7789

import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create ST7735 LCD display class.
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT, 
    dc=9,
    backlight=19,
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

print("{:>5}\t{:>5}".format("raw", "v"))

while True:
    draw.rectangle((0,0, 200, 240), (0, 0, 0))
    Data = ["Carbon Dioxide","Value: "+str(sensor0.value),"Gas Levels:","Value: "+str(sensor1.value),"Ozone:","Value: "+str(sensor2.value)]
    for i in range(0,len(Data)):
        draw.text((text_x, text_y+i*20), Data[i], font=font, fill=(255, 255, 255))
     
    time.sleep(0.2)
    disp.display(img)
