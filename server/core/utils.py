import re
import logging
import logging.config
from subprocess import Popen, PIPE, call

from core.conf import settings

logger = logging.getLogger()
mac_pattern = re.compile("(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", re.I)


def get_logger():
    logging.basicConfig(level=logging.DEBUG)
    logging.config.dictConfig(settings['logging'])
    return logger


def node_is_live(ip):
    return call(['ping', '-c1', '-w2', ip]) == 0


def get_mac_by_ip(ip):
    pid = Popen(['sudo', 'nmap', '-sn', ip], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, errors = pid.communicate()
    if output is not None:
        return mac_pattern.search(output.decode()).groups()[0]


def sensor_name_by_mac(mac):
    return settings['sensors'][mac]['name']
