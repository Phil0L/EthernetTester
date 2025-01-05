#!/usr/bin/env python
import os
import datetime
import sys

import cable
import charge
import display
import ethernet
import touch
import update
from data import Data
from update import KW_DO_UPDATE, KW_NO_UPDATE_CHECK

VERSION = "0.2.10"
KW_LOGFILE = "logfile"
LOGFILE = "log.txt"
data = Data()


def pre_update():
    print("Ethernet tester.")
    print(f"Version: {VERSION}")
    print(f"Current directory is {os.getcwd()}")
    print(f"Main file is in {os.path.dirname(os.path.realpath(__file__))}")


def update_clicked():
    update.update()


def console_clicked():
    pass


def updates_counted(update_count):
    data.update_count = update_count


def start():
    print("Started. Ctrl+C to quit.")
    data.version = VERSION
    display.initialize()
    display.on_update_clicked(lambda: update_clicked())
    display.on_console_clicked(lambda: console_clicked())
    touch.initialize()
    update.start_update_loop(lambda update_count: updates_counted(update_count))
    touch.start_touch_loop(data.touch_data)


def loop():
    data.frame_count += 1
    data.charge = charge.get_charge_percentage()
    data.charging = charge.is_charging()
    data.ipv4 = ethernet.get_ipv4_address()
    data.ipv6 = ethernet.get_ipv6_address()
    data.wlan = ethernet.get_wifi_ipv4_address()
    data.speed = ethernet.get_speed()
    pin, read = cable.test(data.frame_count)
    data.cable[pin] = read
    data.pin = pin
    display.draw(data)
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
        data.update_count = update.update_check()
        if data.update_count > 0:
            print(f"{data.update_count} updates available. Run 'python main.py update' to update")
    start()
    while True:
        loop()
