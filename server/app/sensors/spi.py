import spidev
import logging

logger = logging.getLogger('sensors')


def read_channel(channel):
    try:
        spi = spidev.SpiDev()
        spi.open(0, 0)
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        result = ((adc[1] & 3) << 8) + adc[2]
        return result
    except Exception as e:
        logger.error(e.message)
        return False
