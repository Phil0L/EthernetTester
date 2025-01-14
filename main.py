#!/usr/bin/env python
import copy
import os
import datetime
import sys
import time

import cable
import charge
import display
import ethernet
import touch
import update
from data import Data
from update import KW_DO_UPDATE, KW_NO_UPDATE_CHECK

VERSION = "0.2.11"
KW_LOGFILE = "logfile"
LOGFILE = "log.txt"
current_data = Data()


def pre_update():
    print("Ethernet tester.")
    print(f"Version: {VERSION}")
    print(f"Current directory is {os.getcwd()}")
    print(f"Main file is in {os.path.dirname(os.path.realpath(__file__))}")


def start(): # after update
    print("Started. Ctrl+C to quit.")
    current_data.version = VERSION
    current_data.frame_start = time.time_ns()
    display.initialize()
    display.on_update_clicked(lambda: update.update())
    display.on_console_clicked(lambda: None)
    touch.initialize()


def loop():
    last_data = copy.deepcopy(current_data)
    current_data.frame_start = time.time_ns()
    current_data.frames_per_second = 1 / ((current_data.frame_start - last_data.frame_start) / 1e9)
    current_data.frame_count += 1
    current_data.charge_data.charge = charge.get_charge_percentage()
    current_data.charge_data.charging = charge.is_charging()
    current_data.ip_data.ipv4 = ethernet.get_ipv4_address()
    current_data.ip_data.ipv6 = ethernet.get_ipv6_address()
    current_data.ip_data.wlan = ethernet.get_wifi_ipv4_address()
    current_data.ip_data.speed = ethernet.get_speed()
    touch.check_touch(current_data)
    update.check_update(current_data)
    pin, read = cable.test(current_data.frame_count)
    current_data.cable_data[pin] = read
    current_data.cable_data.pin = pin
    display.draw(current_data, last_data)
    sys.stdout.flush()
    sys.stderr.flush()


if __name__ == "__main__":
    if KW_LOGFILE in sys.argv:
        filemode = 'a' if os.path.getsize(LOGFILE) < 3 * 1024 * 1024 else 'w' # max 3 GB
        sys.stdout = open(LOGFILE, filemode)
        sys.stderr = sys.stdout
        if filemode == 'w':
            print("LOGFILE CLEARED due to max size")
        print(f"APPLICATION STARTED AT {datetime.datetime.now().strftime('%I:%M  %B %d, %Y')}")
    pre_update()
    if KW_DO_UPDATE in sys.argv:
        update.update()
    elif KW_NO_UPDATE_CHECK not in sys.argv:
        current_data.update_count = update.status()
        if current_data.update_count > 0:
            print(f"{current_data.update_count} updates available. Run 'python main.py update' to update")
    start()
    while True:
        loop()
