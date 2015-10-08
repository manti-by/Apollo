import time
import subprocess
import spidev
import Adafruit_SSD1306
import RPi.GPIO as GPIO

from PIL import Image, ImageDraw, ImageFont


# Check rules and allert via buzzer if needed
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


# Buzzer functions
def buzzer_short_low(id):
    buzzer = GPIO.PWM(id, 400)
    buzzer.start()
    time.sleep(0.1)
    buzzer.stop()

def buzzer_double_short_low(id):
    buzzer_short_low(id)
    time.sleep(5)
    buzzer_short_low(id)

def buzzer_long_low(id):
    buzzer = GPIO.PWM(id, 400)
    buzzer.start()
    time.sleep(0.5)
    buzzer.stop()

def buzzer_double_long_low(id):
    buzzer_long_low(id)
    time.sleep(1)
    buzzer_long_low(id)

def buzzer_alert_long_low(id):
    for i in range(5):
        buzzer_long_low(id)
        time.sleep(1)


# Read data from one wire device
def read_onewire_channel(channel):
    crc_ok = False
    tries = 0
    temp = None

    while not crc_ok and tries < 20:
        # Bitbang the 1-wire interface.
        s = subprocess.check_output('cat /sys/bus/w1/devices/28-{}/w1_slave'.format(channel), shell=True).strip()
        lines = s.split('\n')
        line0 = lines[0].split()
        if line0[-1] == 'YES':  # CRC check was good.
            crc_ok = True
            line1 = lines[1].split()
            temp = float(line1[-1][2:])/1000

        # Sleep approx 20ms between attempts.
        time.sleep(0.02)
        tries += 1
    return temp


# Read SPI data from MCP3008
def read_spi_channel(channel):
    spi = spidev.SpiDev()
    spi.open(0, 0)
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    result = ((adc[1] & 3) << 8) + adc[2]
    return result


# Clear display via I2C wire
def clear_display(channel):
    # Initialize library
    display = Adafruit_SSD1306.SSD1306_128_64(rst=channel)
    display.begin()

    # Clear display
    display.clear()
    display.display()


# Display data via I2C wire
def draw_display(data, channel):
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
