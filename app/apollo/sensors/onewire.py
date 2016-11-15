import time
import subprocess


def read_channel(channel):
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
