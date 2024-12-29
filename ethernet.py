import subprocess
import re as regex
import netifaces

ETH0 = 'eth0'
WLAN0 = 'wlan0'


def get_speed():
    result = subprocess.check_output(['sudo', 'ethtool', ETH0])
    speed = regex.search(r"Speed:\s([\w\s!]+)\\n", str(result)).group(1)
    if speed is None or "0" not in speed:
        return ""
    return str(speed.strip())


def get_ipv4_address():
    try:
        return netifaces.ifaddresses(ETH0)[netifaces.AF_INET][0]['addr']
    except KeyError:
        return ""


def get_ipv6_address():
    try:
        return netifaces.ifaddresses(ETH0)[netifaces.AF_INET6][0]['addr']
    except KeyError:
        return ""


def get_wifi_ipv4_address():
    try:
        return netifaces.ifaddresses(WLAN0)[netifaces.AF_INET][0]['addr']
    except KeyError:
        return ""
