import spidev


class MCP3002:
    def __init__(self, spi_port=0, spi_device=0, max_speed_hz=1200000, v_ref=3.3):
        self.v_ref = v_ref

        # Enable SPI
        self.spi = spidev.SpiDev(spi_port, spi_device)
        self.spi.max_speed_hz = max_speed_hz

    def read_adc(self, adc_ch):

        # Make sure ADC channel is 0 or 1
        if adc_ch != 0:
            adc_ch = 1

        # Construct SPI message
        #  First bit (Start): Logic high (1)
        #  Second bit (SGL/DIFF): 1 to select single mode
        #  Third bit (ODD/SIGN): Select channel (0 or 1)
        #  Fourth bit (MSFB): 0 for LSB first
        #  Next 12 bits: 0 (don't care)
        msg = 0b11
        msg = ((msg << 1) + adc_ch) << 5
        msg = [msg, 0b00000000]
        reply = self.spi.xfer2(msg)

        # Construct single integer out of the reply (2 bytes)
        adc = 0
        for n in reply:
            adc = (adc << 8) + n

        # Last bit (0) is not part of ADC value, shift to remove it
        adc = adc >> 1

        # Calculate voltage form ADC value
        voltage = (self.v_ref * adc) / 1024

        return voltage
