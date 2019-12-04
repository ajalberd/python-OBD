import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import sys
# Setting some variables for our reset pin etc.
RESET_PIN = digitalio.DigitalInOut(board.D4)

# Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
i2c = board.I2C()
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3c, reset=RESET_PIN)

# Clear display.
display.fill(0)
display.show()

# Load a font in 2 different sizes.
font = ImageFont.truetype('/home/pi/python-OBD/b.ttf', 28)




#display.text('olleh123',0,34,0xFFFFF, font_name=font, size=2)
#display.show()

#display.fill(0)
#display.show()



x = sys.argv[1]
# Draw the text
# draw.text((34, 0), 'Hello!', font=font, fill=255)
#draw.text("Hello",34,0,color=0xFF0000,font_name=font)
display.text(x,0,34,0xFFFFF, font_name=font, size=2)

# Display image
display.show()

