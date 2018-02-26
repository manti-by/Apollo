import re
import logging
import logging.config
import subprocess

from app.conf import settings

logger = logging.getLogger()


def get_logger():
    logging.basicConfig(level=logging.DEBUG)
    logging.config.dictConfig(settings['logging'])
    return logger


def node_is_live(ip):
    return subprocess.call(["ping", "-c1", "-w2", ip]) == 0


def get_mac_by_ip(ip):
    pid = subprocess.Popen(["arp", "-n", ip])
    output, errors = pid.communicate()[0]
    if output is not None:
        return re.search(r"(([a-f\d]{1,2}\:){5}[a-f\d]{1,2})", re.S).groups()[0]


def sensor_name_by_mac(mac):
    return settings['sensors'][mac]['name']
