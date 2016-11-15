import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont


# Clear display via I2C wire
def clear(channel):
    # Initialize library
    display = Adafruit_SSD1306.SSD1306_128_64(rst=channel)
    display.begin()

    # Clear display
    display.clear()
    display.display()


# Display data via I2C wire
def draw(data, channel):
    # Initialize library
    display = Adafruit_SSD1306.SSD1306_128_64(rst=channel)
    display.begin()

    # Clear display
    display.clear()
    display.display()

    # Create blank image for drawing
    # Make sure to create image with mode '1' for 1-bit color
    image = Image.new('1', (display.width, display.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    # Write two lines of text
    line_01 = ' T1: {} T2: {}'.format(data['term_01'], data['term_02'])
    line_02 = ' T3: {} T4: {}'.format(data['term_03'], data['term_04'])
    line_03 = ' T5: {}'.format(data['term_05'])
    line_04 = ' Water level low' if data['water_sensor'] else ' Warning! Change the container'

    draw.text((2,  2), line_01, font=font, fill=255)
    draw.text((2, 18), line_02, font=font, fill=255)
    draw.text((2, 34), line_03, font=font, fill=255)
    draw.text((2, 50), line_04, font=font, fill=255)

    # Display image
    display.image(image)
    display.display()
