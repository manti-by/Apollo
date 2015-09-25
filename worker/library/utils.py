import Image
import ImageDraw
import ImageFont

from library.ssd1306 import SSD1306_128_64
from library.buzzer import buzzer_short_low, buzzer_long_low, buzzer_double_short_low, \
    buzzer_double_long_low, buzzer_alert_long_low


def check_rules(data, buzzer_id):
    if data['term_01'] >= 60:
        buzzer_short_low(buzzer_id)
    if data['term_01'] >= 80:
        buzzer_long_low(buzzer_id)

    if data['term_02'] >= 40:
        buzzer_double_short_low(buzzer_id)
    if data['term_02'] >= 70:
        buzzer_double_long_low(buzzer_id)
    if data['term_01'] >= 80:
        buzzer_short_low(buzzer_id)

    if data['term_03'] >= 30 or data['term_04'] >= 30 or data['term_05'] >= 30:
        buzzer_alert_long_low(buzzer_id)

    if data['water_sensor']:
        buzzer_alert_long_low(buzzer_id)


def draw_display(data, id):
    # Initialize library
    display = SSD1306_128_64(rst=id)
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
    first_line = 'T1: {}, T2: {}, T3: {}, T4: {}, T5: {}*C'.format(data['term_01'], data['term_02'], data['term_03'],
                                                                   data['term_04'], data['term_05'])

    second_line = 'Water level not reached' if data['water_sensor'] else 'Warning! Change the container'

    draw.text((2, 2), first_line,  font=font, fill=255)
    draw.text((2, 22), second_line, font=font, fill=255)

    # Display image
    display.image(image)
    display.display()
