#!/usr/bin/env python
import datetime
import sys
from time import sleep

import display
from data import Data
from update import update_check, KW_DO_UPDATE, update, KW_NO_UPDATE_CHECK

VERSION = "0.2.3"
KW_LOGFILE = "logfile"
data = Data()


def pre_update():
    print("Ethernet tester.")
    print(f"Version: {VERSION}")


def start():
    print("Started. Ctrl+C to quit.")
    data.version = VERSION
    display.initialize()


def loop():
    display.draw(data)
    display.check_touch(data.touch, lambda x, y: touched(x, y))


def touched(x, y):
    print(f"Touch at: {x}|{y}")


if __name__ == "__main__":
    pre_update()
    if KW_DO_UPDATE in sys.argv:
        update()
    elif KW_NO_UPDATE_CHECK not in sys.argv:
        update_count = update_check()
    if KW_LOGFILE in sys.argv:
        print(f"APPLICATION STARTED AT {datetime.datetime.now().strftime('%I:%M  %B %d, %Y')}")
    start()
    while True:
        loop()
