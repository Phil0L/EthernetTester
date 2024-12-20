import netifaces

# ethtool eth0 | grep Speed


def get_ipv4_address():
    try:
        return netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
    except KeyError:
        return ""


def get_ipv6_address():
    try:
        return netifaces.ifaddresses('eth0')[netifaces.AF_INET6][0]['addr']
    except KeyError:
        return ""
